# Usa una imagen base oficial de Python
FROM python:3.10

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos y la aplicación
COPY requirements.txt requirements.txt
COPY . /app

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando para ejecutar la aplicación Flask
CMD ["python3", "app.py"]
