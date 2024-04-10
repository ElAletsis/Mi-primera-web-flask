
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'secret_key'
#configura la sesion para que las cookies solo sean enviadas a traves de conexiones https seguras
SESSION_COOKIE_SECURE = True 
UPLOAD_FOLDER = 'static'

#Configuracion SMTP para el envio del correo de 'reset password'
MAIL_SERVER = 'smtp-relay.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'Correodeprueba'
MAIL_PASSWORD = 'Passworddeprueba2024'
