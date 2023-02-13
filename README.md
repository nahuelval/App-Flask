# CRUD

## Requerimientos

asgiref==3.5.2
cffi==1.15.1
click==8.1.3
colorama==0.4.6
cryptography==38.0.4
Flask==2.2.2
Flask-MySQL==1.5.2
Flask-MySQLdb==1.0.1
Flask-SQLAlchemy==3.0.2
greenlet==2.0.1
itsdangerous==2.1.2
Jinja2==3.1.2
MarkupSafe==2.1.1
mysqlclient==2.1.1
pycparser==2.21
PyMySQL==1.0.2
python-decouple==3.7
python-dotenv==0.21.1
SQLAlchemy==1.4.45
sqlparse==0.4.3
tzdata==2022.6
Werkzeug==2.2.2

## Instalación

- Descargar Python version 3.11.1 y luego instalar las dependencias listadas en el archivo "requirements.txt" con el comando *pip install -r requirement.txt* (se puede realizar en un entorno virtual).
- Crear archivo *.env* en la carpeta *./src* con las variables de entorno usadas en el *app.config* del archivo *app.py*.
- Descargar MySql y XAMPP para conectar la base de datos a la aplicación (antes de correr la aplicación, iniciar los servicios de apache y mysql desde el panel de control de xampp).
- Correr el archivo *app.py* en la carpeta *./src*.