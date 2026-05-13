# 1. Imagen base oficial de Python
FROM python:3.11-slim

# 2. Evitar que Python genere archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 4. Instalar dependencias del sistema necesarias para OpenCV y PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    g++ \
    libgl1 \
    libglib2.0-0 \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
# 5. Instalar las dependencias de Python desde tu archivo
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copiar todo el código del proyecto a la imagen
COPY . /app/

# 7. Informar que el contenedor usará el puerto 8000
EXPOSE 8000

# 8. Comando para iniciar la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]