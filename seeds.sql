-- Seeds para copa_renault

USE copa_renault;

-- Usuarios
INSERT INTO usuarios (nombre, email, password, tipo_usuario) VALUES
('admin', 'admin@example.com', '1234', 'administrador'),
('profesor1', 'prof1@example.com', 'pass1', 'usuario'),
('alumno1', 'alumno1@example.com', 'alumno123', 'usuario');

-- Deportes
INSERT INTO deportes (nombre, descripcion) VALUES
('Fútbol', 'Deporte rey'),
('Vóley', 'Vóley escolar'),
('Básquet', 'Básquet 3x3');

-- Divisiones
INSERT INTO divisiones (id_deporte, nombre, descripcion, nivel) VALUES
(1, 'Primera', 'División principal', 'mayor'),
(1, 'Juvenil', 'División juvenil', 'media'),
(2, 'Primera Vóley', 'División escolar vóley', 'mayor');

-- Equipos
INSERT INTO equipos (id_division, nombre, ciudad, logo_url, fecha_fundacion) VALUES
(1, 'Tiburones FC', 'Ciudad A', 'img/logo_tiburones.png', '2001-05-10'),
(1, 'Leones FC', 'Ciudad B', 'img/logo_leones.png', '1998-03-20'),
(2, 'Colegio ITR', 'Ciudad C', 'img/logo_itr.png', '2010-09-01');

-- Jugadores
INSERT INTO jugadores (id_equipo, nombre, numero_camiseta, posicion, edad, foto_url) VALUES
(1, 'Juan Perez', 9, 'Delantero', 17, 'img/jugador1.png'),
(1, 'Lucas Gómez', 10, 'Mediocampista', 18, 'img/jugador2.png'),
(2, 'Carlos Ruiz', 4, 'Defensor', 19, 'img/jugador3.png');

-- Arbitros
INSERT INTO arbitros (id_deporte, nombre, email, telefono, experiencia_años) VALUES
(1, 'Roberto Díaz', 'rob@arbitros.com', '123456789', 5),
(2, 'María López', 'maria@arbitros.com', '987654321', 3);

-- Sponsors
INSERT INTO sponsors (nombre, email, telefono, logo_url, slogan, descripcion_breve, sitio_web, fecha_contrato) VALUES
('Renault Local', 'contacto@renault.com', '111222333', 'img/logo1.png', 'Pasión por la ruta', 'Concesionario local', 'https://renault.example', '2024-01-01'),
('Cafetería Central', 'cafecito@example.com', '444555666', 'img/logo2.png', 'Energía para el juego', 'Cafetería local', 'https://cafe.example', '2024-02-01');

-- Sponsor ubicacion
INSERT INTO sponsor_ubicacion (id_sponsor, ubicacion, tipo_ubicacion) VALUES
(1, 'home_banner', 'banner_principal'),
(2, 'sidebar', 'barra_lateral');

-- Reglamento
INSERT INTO reglamento (id_deporte, titulo, contenido, orden) VALUES
(1, 'Regla 1', 'Sin entradas violentas', 1),
(2, 'Regla Vóley', 'Toques permitidos', 1);

-- Partidos
INSERT INTO partidos (id_division, id_arbitro, id_equipo_local, id_equipo_visitante, fecha_partido, hora_partido, estado, ubicacion) VALUES
(1, 1, 1, 2, '2024-06-01', '15:30:00', 'programado', 'Estadio Municipal');

-- Jugador favorito
INSERT INTO jugador_favorito (id_usuario, id_jugador) VALUES
(3, 1);

-- Logs_acciones (ejemplo)
INSERT INTO logs_acciones (id_usuario, tipo_accion, tabla_afectada, descripcion) VALUES
(1, 'crear', 'usuarios', 'Creación usuario admin');

-- Tabla opcional productos_cantina
CREATE TABLE IF NOT EXISTS productos_cantina (
    id_producto INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    descripcion TEXT,
    imagen_url TEXT,
    PRIMARY KEY (id_producto)
);

INSERT INTO productos_cantina (nombre, precio, descripcion, imagen_url) VALUES
('Hamburguesa', 3500, 'Con papas fritas', 'img/hamburguesa.png'),
('Pizza', 5200, 'Muzzarella', 'img/pizza.png'),
('Gaseosa', 1800, '500ml', 'img/gaseosa.png'),
('Panchos', 2500, 'Doble cheddar', 'img/panchos.png'),
('Café', 1200, 'Con leche', 'img/cafe.png'),
('Tostado', 2900, 'Jamón y queso', 'img/tostado.png');

COMMIT;
