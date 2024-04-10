from app import app, db, login_manager, mail, Message
from flask import render_template, url_for, redirect, flash
from flask_login import  current_user, login_user, login_required, logout_user
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, StatementError
from flask_login import current_user
from app import models, forms
import os
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(usuario_id):
    return models.Usuario.query.filter_by(id=int(usuario_id)).first()

@app.route('/') 
def index():
    if current_user.is_authenticated:
        usuario = models.Usuario.query.get(current_user.id)
        usuario_name = usuario.name
        return render_template('index.html', usuario_name = usuario_name)
    return render_template('index.html')


def send_email(user):
    token=user.get_token()
    try:
        msg = Message('Password Reset Request', recipients=user.email, sender=app.config['MAIL_USERNAME'])
        msg.body = f'''Para cambiar tu contraseña. Da click en el siguiente enlace
        {url_for('reset_token', token=token, _external=True)}
        '''
        print(msg.body)
    except Exception as e:
        print (e)

@app.route('/reset_password/', methods=['GET', 'POST'])
def reset_request():
    form = forms.ResetPasswordForm()
    if form.validate_on_submit():
        user = models.Usuario.query.filter_by(email=form.email.data).first()
        if user:
            send_email(user)
        else:
            return 'El correo ingresado no existe en la base de datos'
    return render_template('reset_password.html', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user = models.Usuario.verify_token(token)
    if user is None:
        print("Token expirado o invalido, por favor intenta de nuevo")
        return url_for('reset_request')
    form = forms.CambiarContraseña()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password1.data)
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('cambiar_contraseña.html', form=form)


@app.route('/crear-articulo', methods=['GET', 'POST'])
@login_required
def articulo_nuevo():
        # Al llamar a la funcion va a crear el formulario dentro de la vista
    form = forms.ArticuloForm()
    form.categorias_articulo.choices = [(categoria.id, categoria.name) for categoria in models.Categorias.query.all()]
    #validar los datos ingresados en el formulario
    if form.validate_on_submit():
        try:
            # la sintaxis form.nombre,precio,imagen_articulo.data hace referencia a la informacion recuperada 
            # de sus respectivos campos dentro del formulario 
            name = form.nombre_articulo.data
            price = form.precio_articulo.data
            file = form.imagen_articulo.data
            description = form.descripcion_articulo.data
            categoria_id = form.categorias_articulo.data
            #Usa esta variable para guardar el id de la categoria seleccionada en el formulario
            nombre_categoria = models.Categorias.query.filter(models.Categorias.id==categoria_id).first()
            #Ruta donde se va a guardar la imagen subida en el formulario "static/'nombre de la categoria'/'nombre de la imagen'"
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], nombre_categoria.name, secure_filename(file.filename)))
            #crea la instancia de articulo
            articulo_creado = models.Articulo(name=name, price=price, image_name=file.filename, description=description, categoria_id=categoria_id)
            #ejecuta el query y crea el objeto en la base de datos
            db.session.add(articulo_creado)
            
            db.session.commit()
            db.session.close()
            
            flash("El articulo ha sido creado exitosamente")
            return redirect(url_for('articulo_nuevo'))
        except IntegrityError:
            db.session.rollback()
            flash("Error al crear el artículo: El nombre del articulo o de la imagen ya existe")
        except (ValueError, StatementError):
            flash("No puedes ingresar letras en el campo de precio")


    return render_template('crear_productos.html', form=form)

@app.route('/crear-categoria', methods=['GET', 'POST'])
@login_required
def crear_categoria():
    form = forms.CategoriaForm()
    categorias_existentes = models.Categorias.query.all()
    if form.validate_on_submit():
        try:
            name = form.nombre_categoria.data
            file = form.imagen_categoria.data
            directorio_categoria = os.path.join(os.path.dirname(__file__),'static', name)
            print(Path.cwd())
            nombre_imagen = secure_filename(file.filename)
            os.mkdir(directorio_categoria)
            file.save(os.path.join(directorio_categoria, secure_filename(file.filename)))
            categoria_nueva = models.Categorias(name=name, image_category=nombre_imagen)
            db.session.add(categoria_nueva)
            db.session.commit()
            db.session.close()
            flash('La categoria ha sido creada correctamente','success')
            return redirect(url_for('crear_categoria'))
        except SQLAlchemyError :
            db.session.rollback()
            flash("La categoria que intentas crear ya existe")
    
    return render_template('crear_categoria.html', form=form, categorias=categorias_existentes)

@app.route('/actualizar/<int:id>', methods=['GET', 'POST'])
@login_required
def actualizar_articulo(id):
    articulo = models.Articulo.query.get_or_404(id)
    categoria = models.Categorias.query.filter_by(id=articulo.categoria_id).first()
    form = forms.ActualizarArticuloForm(obj=articulo)
    if form.validate_on_submit():
        if form.nombre_articulo.data:
            try:
                articulo.name = form.nombre_articulo.data
                db.session.commit()
                return 'Nombre del articulo actualizado exitosamente'
            except Exception as e :
                print('a')
                db.session.rollback()
        if form.precio_articulo.data:
            try:
                articulo.price = int(form.precio_articulo.data)
                db.session.commit()
                return 'Precio del articulo actualizado exitosamente'
            except Exception as e:
                print('b')
                db.session.rollback()
        if form.descripcion_articulo.data:
            try:
                articulo.description = form.descripcion_articulo.data
                db.session.commit()
                return 'Descripcion del articulo actualizado exitosamente'
            except:
                print('c')
                db.session.rollback()
        if form.imagen_articulo.data:
            try:
                path_imagen = Path('app/') / app.config['UPLOAD_FOLDER'] / categoria.name / articulo.image_name
                Path.unlink(path_imagen)
                file = form.imagen_articulo.data
                file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'], categoria.name, secure_filename(file.filename)))
                articulo.image_name = file.filename
                db.session.commit()
                return 'Imagen del articulo actualizada exitosamente'
            except Exception:  
                print('d')

    return render_template('actualizar_producto.html', form=form, articulo=articulo)

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/eliminar-articulos')
@login_required
def eliminar_articulos():
    articulos = models.Articulo.query.all()
    categorias = {}
    for articulo in articulos:
        categoria = models.Categorias.query.filter_by(id=articulo.categoria_id).first()
        if categoria:
            categorias[articulo.id] = categoria
    print(categorias)
    return render_template('eliminar_productos.html', categorias=categorias, articulos=articulos)

@app.route('/nuestros-productos/')
def nuestros_productos():
    return render_template('nuestros_productos.html', categorias=todas_categorias())

@app.route('/nuestros-productos/<int:categoria_id>')
def productos_categoria(categoria_id):
    categoria = models.Categorias.query.get_or_404(categoria_id)
    articulos = models.Articulo.query.filter_by(categoria_id=categoria_id).all()
    return render_template('productos_categoria.html', categoria=categoria, articulos=articulos)

def todos_articulos():
    articulos = models.Articulo.query.filter_by(categoria_id=models.Categorias.id).all()
    return articulos

def todas_categorias():
    categorias = models.Categorias.query.all()
    return categorias

@app.route('/eliminar/<int:articulo_id>')
@login_required
def eliminar_articulo(articulo_id):
    articulo_a_eliminar = models.Articulo.query.get_or_404(articulo_id)
    imagen_a_eliminar = articulo_a_eliminar.image_name 
    categoria = models.Categorias.query.filter_by(id=articulo_a_eliminar.categoria_id).first()
    
    path_imagen = Path('app/') / app.config['UPLOAD_FOLDER'] / categoria.name / imagen_a_eliminar
    print(path_imagen)

    try:
        Path.unlink(path_imagen)    
        db.session.delete(articulo_a_eliminar)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "No se pudo eliminar el articulo seleccionado"

@app.route('/registrarse', methods=['GET', 'POST'])
def registro():
    form = forms.RegistroForm()
    
    if form.validate_on_submit():
        name = form.user_name.data
        email = form.email.data
        hashed_password = generate_password_hash(form.password.data)
        usuario = models.Usuario(name=name, password=hashed_password, email=email)
        try:
            db.session.add(usuario)
            db.session.commit()
            db.session.close()
            return redirect(url_for('registrarse'))
        except SQLAlchemyError :
            db.session.rollback()
            flash('Los datos ingresados ya existen en la base de datos')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm() 
    if form.validate_on_submit():
        #valida el formulario con los datos name, password ingresados en el formulario
        name = form.user_name.data
        password = form.password.data
        #devuelve el primer resultado de usuario filtrado por el campo name, password
        usuario = models.Usuario.query.filter_by(name=name).first()
        
        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario, remember=False)
            return redirect(url_for('index'))
        else:
            print('no existe')

    if current_user.is_authenticated and current_user.is_active:
        return redirect(url_for('index'))
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))