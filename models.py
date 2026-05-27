from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import INTEGER, VARCHAR, TEXT, TINYINT, ENUM
from datetime import datetime

db = SQLAlchemy()


class Usuarios(db.Model):
    __tablename__ = "usuarios"
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    tipo_usuario = db.Column(db.Enum('administrador', 'usuario'), nullable=False, default='usuario')
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.Boolean, default=True)


class Deportes(db.Model):
    __tablename__ = "deportes"
    id_deporte = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)


class Divisiones(db.Model):
    __tablename__ = "divisiones"
    id_division = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_deporte = db.Column(db.Integer, db.ForeignKey('deportes.id_deporte'), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text)
    nivel = db.Column(db.Enum('menor', 'media', 'mayor'), nullable=False)


class Equipos(db.Model):
    __tablename__ = "equipos"
    id_equipo = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_division = db.Column(db.Integer, db.ForeignKey('divisiones.id_division'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    ciudad = db.Column(db.String(100))
    logo_url = db.Column(db.Text)
    fecha_fundacion = db.Column(db.Date)


class Jugadores(db.Model):
    __tablename__ = "jugadores"
    id_jugador = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id_equipo'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    numero_camiseta = db.Column(db.Integer)
    posicion = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    foto_url = db.Column(db.Text)


class Arbitros(db.Model):
    __tablename__ = "arbitros"
    id_arbitro = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_deporte = db.Column(db.Integer, db.ForeignKey('deportes.id_deporte'), nullable=False)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    experiencia_años = db.Column(db.Integer, default=0)


class Partidos(db.Model):
    __tablename__ = "partidos"
    id_partido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_division = db.Column(db.Integer, db.ForeignKey('divisiones.id_division'), nullable=False)
    id_arbitro = db.Column(db.Integer, db.ForeignKey('arbitros.id_arbitro'), nullable=False)
    id_equipo_local = db.Column(db.Integer, db.ForeignKey('equipos.id_equipo'), nullable=False)
    id_equipo_visitante = db.Column(db.Integer, db.ForeignKey('equipos.id_equipo'), nullable=False)
    fecha_partido = db.Column(db.Date, nullable=False)
    hora_partido = db.Column(db.Time, nullable=False)
    estado = db.Column(db.Enum('programado', 'en_curso', 'finalizado', 'postergado'), default='programado')
    resultado_local = db.Column(db.Integer, default=0)
    resultado_visitante = db.Column(db.Integer, default=0)
    ubicacion = db.Column(db.String(200))


class JugadorFavorito(db.Model):
    __tablename__ = "jugador_favorito"
    id_voto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_jugador = db.Column(db.Integer, db.ForeignKey('jugadores.id_jugador'), nullable=False)
    fecha_voto = db.Column(db.DateTime, default=datetime.utcnow)


class Sponsors(db.Model):
    __tablename__ = "sponsors"
    id_sponsor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    telefono = db.Column(db.String(20))
    logo_url = db.Column(db.Text)
    slogan = db.Column(db.Text)
    descripcion_breve = db.Column(db.Text)
    sitio_web = db.Column(db.String(255))
    fecha_contrato = db.Column(db.Date)
    estado = db.Column(db.Boolean, default=True)


class SponsorUbicacion(db.Model):
    __tablename__ = "sponsor_ubicacion"
    id_ubicacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_sponsor = db.Column(db.Integer, db.ForeignKey('sponsors.id_sponsor'), nullable=False)
    ubicacion = db.Column(db.String(100))
    tipo_ubicacion = db.Column(db.Enum('banner_principal', 'barra_lateral', 'footer', 'popup', 'pagina_equipo', 'pagina_deporte'))


class Reglamento(db.Model):
    __tablename__ = "reglamento"
    id_reglamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_deporte = db.Column(db.Integer, db.ForeignKey('deportes.id_deporte'), nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    contenido = db.Column(db.Text)
    orden = db.Column(db.Integer, default=0)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)


class LogsAcciones(db.Model):
    __tablename__ = "logs_acciones"
    id_log = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    tipo_accion = db.Column(db.String(100), nullable=False)
    tabla_afectada = db.Column(db.String(100))
    id_registro_afectado = db.Column(db.Integer)
    descripcion = db.Column(db.Text)
    fecha_accion = db.Column(db.DateTime, default=datetime.utcnow)


class ProductosCantina(db.Model):
    __tablename__ = "productos_cantina"
    id_producto = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Numeric(10,2), nullable=False)
    descripcion = db.Column(db.Text)
    imagen_url = db.Column(db.Text)


class PedidosCantina(db.Model):
    __tablename__ = "pedidos_cantina"
    id_pedido = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'), nullable=False)
    id_producto = db.Column(db.Integer, db.ForeignKey('productos_cantina.id_producto'), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Numeric(10,2), nullable=False)
    total = db.Column(db.Numeric(10,2), nullable=False)
    estado = db.Column(db.Enum('pendiente', 'procesando', 'entregado', 'cancelado'), nullable=False, default='pendiente')
    nombre_contacto = db.Column(db.String(100), nullable=False)
    email_contacto = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50))
    direccion = db.Column(db.String(255))
    notas = db.Column(db.Text)
    fecha_pedido = db.Column(db.DateTime, default=datetime.utcnow)

    usuario = db.relationship('Usuarios', backref='pedidos_cantina')
    producto = db.relationship('ProductosCantina')
