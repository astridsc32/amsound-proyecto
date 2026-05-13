from django.db import models

class Empleado(models.Model):
    carnet = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    rol = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True) 
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('finalizada', 'Finalizada'),
    ]
    
    usuario = models.ForeignKey(Empleado, on_delete=models.CASCADE) 
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    fecha_renta = models.DateField()
    comentarios = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reserva de {self.producto.nombre} - {self.usuario.nombre}"