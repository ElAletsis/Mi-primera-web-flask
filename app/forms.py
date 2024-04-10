from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo

# Formulario de registro
class RegistroForm(FlaskForm):
    user_name = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    email = EmailField('Correo electronico', validators=[DataRequired()])
    submit = SubmitField('Registrar')

# Formulario de login
class LoginForm(FlaskForm):
    user_name = StringField('Nombre de usuario',validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')

# Formulario Password Reset
class ResetPasswordForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Enviar correo")

# Formulario Cambiar Contraseña
class CambiarContraseña(FlaskForm):
    password1 = PasswordField(validators=[DataRequired()])
    password2 = PasswordField(validators=[DataRequired(), EqualTo('password1')] ) 
    submit = SubmitField("Cambiar contraseña")

# Formulario crear articulo
class ArticuloForm(FlaskForm):
    nombre_articulo = StringField('Nombre de articulo', validators=[DataRequired()])
    precio_articulo  = StringField('Precio de articulo', validators=[DataRequired(message="Ingrese un precio válido.")])
    imagen_articulo = FileField('Imagen de articulo', validators=[DataRequired()])
    descripcion_articulo = StringField('Descripcion del articulo', validators=[DataRequired()])
    categorias_articulo = SelectField('Categorias', choices=[])
    submit = SubmitField('Crear articulo')

# Formulario crear categoria
class CategoriaForm(FlaskForm):
    nombre_categoria = StringField('Nombre de articulo', validators=[DataRequired()])
    imagen_categoria = FileField('Imagen de Categoria',validators=[DataRequired()])
    submit = SubmitField('Crear categoria')

# Formulario actualizar articulo
class ActualizarArticuloForm(FlaskForm):

    '''Formulario para crear categorias'''
    nombre_articulo = StringField('Nombre de articulo')
    precio_articulo  = StringField('Precio de articulo')
    imagen_articulo = FileField('Imagen de articulo')
    descripcion_articulo = StringField('Descripcion del articulo')
    submit = SubmitField('Actualizar articulo')