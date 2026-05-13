from django.shortcuts import render, redirect, get_object_or_404
from .models import Empleado, Producto, Reserva
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password 
from django.core.mail import send_mail 
from django.conf import settings 
import re
import random
from .utils import detectar_rostro

# --- VISTAS DE AUTENTICACIÓN ---

def registro(request):
    if request.method == 'POST':
        carnet = request.POST.get('carnet')
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        rol = request.POST.get('rol')
        token_ingresado = request.POST.get('admin_token') 

        LLAVE_MAESTRA = "AM_SOUND_2026" 

        if rol == 'admin' and token_ingresado != LLAVE_MAESTRA:
            messages.error(request, "Código de autorización incorrecto para crear un Administrador.")
            return redirect('registro')
      
        if len(password) < 12 or not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password) or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messages.error(request, "La contraseña debe tener 12 caracteres, Mayúscula, Número y Símbolo.")
        else:
            try:
                Empleado.objects.create(
                    carnet=carnet,
                    nombre=nombre,
                    correo=correo,
                    password=make_password(password), 
                    rol=rol
                )
                
                try:
                    asunto = 'Bienvenido a AM Sound - Registro Exitoso'
                    mensaje = f'Hola {nombre},\n\nTu cuenta ha sido creada exitosamente.\nRol: {rol}.'
                    send_mail(asunto, mensaje, settings.EMAIL_HOST_USER, [correo])
                except:
                    pass

                messages.success(request, "Registro exitoso. Ya puedes iniciar sesión.")
                return redirect('login')
            except:
                messages.error(request, "Error: El carnet o correo ya existen.")

    return render(request, 'registro.html')

def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        clave = request.POST.get('password')
        try:
            user = Empleado.objects.get(correo=correo)
            if check_password(clave, user.password):
                request.session['user_id'] = user.carnet
                request.session['rol'] = user.rol
                request.session['user_nombre'] = user.nombre
                return redirect('dashboard')
            else:
                messages.error(request, "Contraseña incorrecta.")
        except Empleado.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
    return render(request, 'login.html')

# --- GESTIÓN DE PRODUCTOS Y DASHBOARD ---

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('login')
    
    if request.method == 'POST' and 'btn_agregar' in request.POST:
        if request.session.get('rol') == 'admin':
            precio = float(request.POST.get('precio', 0))
            stock = int(request.POST.get('stock', 0))
            foto = request.FILES.get('imagen') # CAPTURA DE IMAGEN

            if precio < 0 or stock < 0:
                messages.error(request, "Valores no pueden ser negativos.")
            else:
                Producto.objects.create(
                    nombre=request.POST.get('nombre'),
                    descripcion=request.POST.get('descripcion'),
                    precio=precio,
                    stock=stock,
                    imagen=foto # GUARDADO DE IMAGEN
                )
                messages.success(request, "Equipo agregado exitosamente.")
        else:
            messages.error(request, "No tienes permiso para esta acción.")
        return redirect('dashboard')

    productos = Producto.objects.all()
    reservas_list = Reserva.objects.all().order_by('-id') if request.session.get('rol') == 'admin' else []
    
    return render(request, 'dashboard.html', {
        'productos': productos, 
        'reservas_list': reservas_list
    })

def editar_producto(request, id):
    if request.session.get('rol') != 'admin':
        messages.error(request, "Acceso restringido.")
        return redirect('dashboard')

    producto = get_object_or_404(Producto, id_producto=id)
    
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')
        
        # Actualizar imagen solo si se sube una nueva
        nueva_imagen = request.FILES.get('imagen')
        if nueva_imagen:
            producto.imagen = nueva_imagen
            
        producto.save()
        messages.success(request, "Producto actualizado correctamente.")
        return redirect('dashboard')
        
    return render(request, 'editar_producto.html', {'producto': producto})

def eliminar_producto(request, id):
    if request.session.get('rol') != 'admin':
        return redirect('dashboard')
    try:
        Producto.objects.get(id_producto=id).delete()
        messages.success(request, "Producto eliminado.")
    except:
        messages.error(request, "Error al eliminar.")
    return redirect('dashboard')

# --- GESTIÓN DE RESERVAS Y BIOMETRÍA ---

def crear_reserva(request, producto_id):
    if 'user_id' not in request.session: 
        return redirect('login')
    
    if request.method == 'POST':
        try:
            user = Empleado.objects.get(carnet=request.session['user_id'])
            prod = Producto.objects.get(id_producto=producto_id)
            
            Reserva.objects.create(
                usuario=user,
                producto=prod,
                fecha_renta=request.POST.get('fecha_renta'),
                comentarios=request.POST.get('comentarios')
            )
            
            # Enviar correo de notificación
            try:
                send_mail(
                    'Nueva Solicitud de Renta', 
                    f'Hola {user.nombre}, tu solicitud para {prod.nombre} ha sido recibida.', 
                    settings.EMAIL_HOST_USER, 
                    [user.correo]
                )
            except:
                pass
                
            messages.success(request, "Solicitud enviada correctamente.")
        except Exception as e:
            messages.error(request, f"Error al procesar la solicitud: {e}")
            
        return redirect('dashboard')

def login_facial(request):
    resultado = detectar_rostro()
    if resultado:
        admin_user = Empleado.objects.filter(rol='admin').first()
        if admin_user:
            request.session['user_id'] = admin_user.carnet
            request.session['rol'] = admin_user.rol
            request.session['user_nombre'] = admin_user.nombre
            messages.success(request, f"Rostro reconocido. Bienvenido {admin_user.nombre}")
            return redirect('dashboard')
        else:
            messages.error(request, "No hay administradores configurados.")
    else:
        messages.error(request, "No se detectó un rostro.")
    return redirect('login')

# --- RECUPERACIÓN DE CONTRASEÑA ---

def recuperar_password(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        try:
            user = Empleado.objects.get(correo=correo)
            codigo = str(random.randint(100000, 999999))
            request.session['recovery_code'] = codigo
            request.session['recovery_email'] = correo
            
            send_mail("Código de Recuperación", f"Tu código es: {codigo}", settings.EMAIL_HOST_USER, [correo])
            messages.info(request, "Código enviado a tu correo.")
            return render(request, 'reset_password.html')
        except Empleado.DoesNotExist:
            messages.error(request, "Correo no registrado.")
            
    return render(request, 'recuperar_form.html')

def cambiar_password(request):
    if request.method == 'POST':
        codigo_ing = request.POST.get('codigo')
        nueva_clave = request.POST.get('password')
        codigo_real = request.session.get('recovery_code')
        correo = request.session.get('recovery_email')

        if codigo_ing == codigo_real:
            user = Empleado.objects.get(correo=correo)
            user.password = make_password(nueva_clave)
            user.save()
            
            # Limpiar sesión de recuperación
            request.session.pop('recovery_code', None)
            request.session.pop('recovery_email', None)
            
            messages.success(request, "Contraseña actualizada exitosamente.")
            return redirect('login')
        else:
            messages.error(request, "Código incorrecto.")
            
    return render(request, 'reset_password.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')