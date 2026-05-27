from flask import Flask, render_template, request, redirect, url_for, flash, session
import os

from config import Config
from models import db, Usuarios

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.getenv("SECRET_KEY", "dev-secret")

# Inicializar la extensión de base de datos
db.init_app(app)


def get_current_user():
    user_id = session.get('user_id')
    return Usuarios.query.get(user_id) if user_id else None


@app.route("/", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        usuario = request.form.get("usuario")
        contraseña = request.form.get("contraseña")

        user = Usuarios.query.filter_by(nombre=usuario).first()
        if not user:
            user = Usuarios.query.filter_by(email=usuario).first()

        if user and user.password == contraseña:
            session['user_id'] = user.id_usuario
            session['user_name'] = user.nombre
            return redirect(url_for("inicio"))
        else:
            error = "Usuario o contraseña incorrectos"

    return render_template("base.html", error=error)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/inicio", methods=["GET", "POST"])
def inicio():
    # Manejar envío de cuestionario (PRG: Post/Redirect/Get)
    if request.method == "POST":
        # Aquí puedes procesar los datos recibidos: request.form
        datos = request.form.to_dict()
        # ejemplo de logging; en producción guarda en BD
        app.logger.info("Cuestionario enviado: %s", datos)
        # redirigir para evitar que el formulario se vuelva a mostrar al recargar
        return redirect(url_for("inicio", submitted=1))

    submitted = request.args.get("submitted")

    # Cargar deportes desde la BD
    from models import Deportes, Sponsors, ProductosCantina
    deportes = Deportes.query.order_by(Deportes.id_deporte).all()
    sponsors = Sponsors.query.order_by(Sponsors.id_sponsor).all()
    productos = ProductosCantina.query.order_by(ProductosCantina.id_producto).all()

    # Mapear nombre de deporte a imagen estática (fallback a imagen por nombre simple)
    def deporte_to_img(nombre):
        slug = nombre.lower()
        slug = slug.replace('ú','u').replace('é','e').replace('í','i').replace('ó','o').replace('á','a')
        slug = ''.join(c for c in slug if c.isalnum())
        return f"img/{slug}.png"

    deportes_data = []
    for d in deportes:
        deportes_data.append({
            'id': d.id_deporte,
            'nombre': d.nombre,
            'descripcion': d.descripcion,
            'imagen': deporte_to_img(d.nombre)
        })

    return render_template("inicio_dynamic.html", submitted=submitted, deportes=deportes_data, sponsors=sponsors, productos=productos)


@app.route("/cantina")
def cantina():
    from models import ProductosCantina
    productos = ProductosCantina.query.order_by(ProductosCantina.id_producto).all()
    user = get_current_user()
    return render_template("cantina_dynamic.html", productos=productos, user=user)


@app.route('/cantina/producto/<int:product_id>', methods=['GET', 'POST'])
def cantina_producto(product_id):
    from models import ProductosCantina, PedidosCantina

    user = get_current_user()
    if not user:
        flash('Debes iniciar sesión para hacer un pedido.')
        return redirect(url_for('login'))

    producto = ProductosCantina.query.get(product_id)
    if not producto:
        return "Producto no encontrado", 404

    if request.method == 'POST':
        nombre_contacto = request.form.get('nombre_contacto', user.nombre).strip()
        email_contacto = request.form.get('email_contacto', user.email).strip()
        telefono_contacto = request.form.get('telefono_contacto', '').strip()
        direccion = request.form.get('direccion', '').strip()
        notas = request.form.get('notas', '').strip()
        cantidad = max(1, int(request.form.get('cantidad', 1)))

        total = producto.precio * cantidad

        pedido = PedidosCantina(
            id_usuario=user.id_usuario,
            id_producto=producto.id_producto,
            cantidad=cantidad,
            precio_unitario=producto.precio,
            total=total,
            estado='pendiente',
            nombre_contacto=nombre_contacto,
            email_contacto=email_contacto,
            telefono=telefono_contacto,
            direccion=direccion,
            notas=notas,
        )

        db.session.add(pedido)
        db.session.commit()

        return redirect(url_for('pedido_confirmacion', pedido_id=pedido.id_pedido))

    return render_template('cantina_producto.html', producto=producto, user=user)


@app.route('/cantina/pedido/<int:pedido_id>')
def pedido_confirmacion(pedido_id):
    from models import PedidosCantina, ProductosCantina

    user = get_current_user()
    if not user:
        flash('Debes iniciar sesión para ver tu pedido.')
        return redirect(url_for('login'))

    pedido = PedidosCantina.query.get(pedido_id)
    if not pedido or pedido.id_usuario != user.id_usuario:
        return "Pedido no encontrado", 404

    producto = ProductosCantina.query.get(pedido.id_producto)
    return render_template('cantina_confirmacion.html', pedido=pedido, producto=producto, user=user)


@app.route('/cantina/mis-pedidos')
def mis_pedidos():
    from models import PedidosCantina, ProductosCantina

    user = get_current_user()
    if not user:
        flash('Debes iniciar sesión para ver tus pedidos.')
        return redirect(url_for('login'))

    pedidos = PedidosCantina.query.filter_by(id_usuario=user.id_usuario).order_by(PedidosCantina.fecha_pedido.desc()).all()
    producto_ids = {pedido.id_producto for pedido in pedidos}
    productos = ProductosCantina.query.filter(ProductosCantina.id_producto.in_(producto_ids)).all()
    producto_map = {p.id_producto: p for p in productos}

    return render_template('mis_pedidos.html', pedidos=pedidos, producto_map=producto_map, user=user)


@app.route("/sponsors")
def sponsors():
    from models import Sponsors
    sponsors = Sponsors.query.order_by(Sponsors.id_sponsor).all()
    return render_template("sponsors_dynamic.html", sponsors=sponsors)


@app.route('/deporte/<int:deporte_id>')
def deporte_page(deporte_id):
    from models import Deportes, Divisiones, Equipos, Jugadores

    deporte = Deportes.query.filter_by(id_deporte=deporte_id).first()
    if not deporte:
        return "Deporte no encontrado", 404

    # Obtener divisiones del deporte
    divisiones = Divisiones.query.filter_by(id_deporte=deporte_id).all()

    # Obtener equipos asociados a las divisiones
    division_ids = [d.id_division for d in divisiones]
    equipos = []
    if division_ids:
        equipos = Equipos.query.filter(Equipos.id_division.in_(division_ids)).all()

    # Obtener jugadores asociados a esos equipos
    equipo_ids = [e.id_equipo for e in equipos]
    jugadores = []
    if equipo_ids:
        jugadores = Jugadores.query.filter(Jugadores.id_equipo.in_(equipo_ids)).all()

    # Árbitros del deporte
    from models import Arbitros, Reglamento, Partidos
    arbitros = Arbitros.query.filter_by(id_deporte=deporte_id).all()

    # Reglamentos del deporte
    reglamentos = Reglamento.query.filter_by(id_deporte=deporte_id).order_by(Reglamento.orden).all()

    # Partidos relacionados a las divisiones de este deporte
    partidos = []
    if division_ids:
        partidos = Partidos.query.filter(Partidos.id_division.in_(division_ids)).order_by(Partidos.fecha_partido, Partidos.hora_partido).all()

    # Enriquecer partidos con nombres de equipos y arbitro
    partidos_data = []
    for p in partidos:
        local = Equipos.query.get(p.id_equipo_local)
        visitante = Equipos.query.get(p.id_equipo_visitante)
        arbitro = Arbitros.query.get(p.id_arbitro)
        partidos_data.append({
            'id': p.id_partido,
            'fecha': p.fecha_partido,
            'hora': p.hora_partido,
            'local': local.nombre if local else 'N/A',
            'visitante': visitante.nombre if visitante else 'N/A',
            'estado': p.estado,
            'resultado_local': p.resultado_local,
            'resultado_visitante': p.resultado_visitante,
            'ubicacion': p.ubicacion,
            'arbitro': arbitro.nombre if arbitro else None,
        })

    # Imagen derivada del nombre (misma lógica que en inicio)
    def deporte_to_img(nombre):
        slug = nombre.lower()
        for a,b in [('ú','u'),('é','e'),('í','i'),('ó','o'),('á','a')]:
            slug = slug.replace(a,b)
        slug = ''.join(c for c in slug if c.isalnum())
        return f"img/{slug}.png"

    imagen = deporte_to_img(deporte.nombre)

    return render_template('deporte.html', deporte=deporte, divisiones=divisiones, equipos=equipos, jugadores=jugadores, imagen=imagen, arbitros=arbitros, reglamentos=reglamentos, partidos=partidos_data)


@app.route('/equipo/<int:equipo_id>')
def equipo_page(equipo_id):
    from models import Equipos, Jugadores

    equipo = Equipos.query.get(equipo_id)
    if not equipo:
        return "Equipo no encontrado", 404

    jugadores = Jugadores.query.filter_by(id_equipo=equipo_id).all()

    # obtener la división y deporte asociado para el botón volver
    from models import Divisiones
    division = Divisiones.query.get(equipo.id_division) if equipo.id_division else None
    deporte_id = division.id_deporte if division else None

    return render_template('equipo.html', equipo=equipo, jugadores=jugadores, deporte_id=deporte_id)


if __name__ == "__main__":
    app.run(debug=True)