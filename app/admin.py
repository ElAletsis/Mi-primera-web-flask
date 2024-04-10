
from app import app, db, models
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import  current_user, login_required
from werkzeug.security import generate_password_hash


class UsuarioAdminView(ModelView):
    #apunta a los campos name y password del formulario
    form_columns = ['name', 'password', 'email']

    def on_model_change(self, form, model, is_created):
        if 'password' in form:
            hashed_password = generate_password_hash(form.password.data)
            model.password = hashed_password

# Creamos la clase myadminindexview que hereda de clase adminindexview
class MyAdminIndexView(AdminIndexView):
    #Usando el decorador @login_required sera necesario haber hecho log_in para ingresar a cualquier apartado del panel de administracion
    #incluido el ingreso manual desde la url del navegador
    @login_required
    def is_accessible(self):
        if current_user.is_authenticated:
        # si el login se realizo de manera correcta, usuario_name queda guardado en la sesion y permite ingresar al 
        # panel de admin
            return True

admin = Admin(app, index_view=MyAdminIndexView() ,name='My Admin Panel', template_mode='bootstrap4')
# Agregar los campos de los objetos Articulo y Usuario al panel admin
admin.add_view(ModelView(models.Articulo, db.session))
admin.add_view(UsuarioAdminView(models.Usuario, db.session))
admin.add_view(ModelView(models.Categorias, db.session))