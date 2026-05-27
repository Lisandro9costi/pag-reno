# Pag-Reno (Flask + MySQL)

Instrucciones rápidas para conectar la app Flask con la base de datos MySQL (copa_renault).

1. Crear un entorno virtual e instalar dependencias:

```bash
python -m venv .venv
source .venv/bin/activate   # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Variables de entorno (opcional)

Crear un fichero `.env` en la raíz con al menos:

```
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=copa_renault
SECRET_KEY=clave_secreta
```

3. Ejecutar la aplicación:

```bash
python index.py
```

Notas:
- La app usa `models.py` y `config.py` para la conexión con la base de datos.
- El login usa la tabla `usuarios` (contraseñas en texto plano por ahora).
