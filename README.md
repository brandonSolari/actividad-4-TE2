# Tablón de anuncios (Flask)

Actividad N° 4 · TEM-742 Tecnologías Emergentes II

Aplicación web para gestionar un tablón de anuncios con Flask, base de datos
relacional (SQLite por defecto, MySQL opcional), patrón Application Factory,
Blueprints y Bootstrap 5.

## Ejecutar

```bash
python -m venv venv
venv\Scripts\activate        # Windows  (Linux/Mac: source venv/bin/activate)
pip install -r requirements.txt
python run.py
```

Abrir http://127.0.0.1:5000

Usuario inicial (se crea solo la primera vez):

- Correo: `admin@correo.com`
- Contraseña: `admin123`

## Estructura

```
tablon_anuncios/
├── run.py                  # arranca la aplicación
├── config.py               # configuración (base de datos, clave, institución)
├── requirements.txt
└── app/
    ├── __init__.py         # create_app() — Application Factory
    ├── extensions.py       # db y login_manager
    ├── models.py           # tablas: usuarios, categorias, anuncios
    ├── seed.py             # datos iniciales (admin y categorías de ejemplo)
    ├── main/               # Blueprint: página principal pública
    ├── auth/               # Blueprint: inicio y cierre de sesión
    ├── usuarios/           # Blueprint: CRUD de usuarios
    ├── categorias/         # Blueprint: CRUD de categorías
    ├── anuncios/           # Blueprint: CRUD de anuncios
    ├── templates/          # base.html + una carpeta por módulo
    └── static/css/
```

## Base de datos `bd_anuncios`

**usuarios**: id (PK), nombre, email (único), password_hash, fecha_registro

**categorias**: id (PK), nombre (único), descripcion

**anuncios**: id (PK), titulo, contenido, fecha_publicacion,
usuario_id (FK → usuarios.id), categoria_id (FK → categorias.id)

Relaciones: un usuario publica muchos anuncios (1:N) y una categoría agrupa
muchos anuncios (1:N).

## Usar MySQL (XAMPP) en lugar de SQLite

1. `pip install pymysql cryptography`
2. En phpMyAdmin: `CREATE DATABASE bd_anuncios CHARACTER SET utf8mb4;`
3. En `config.py`, cambiar `SQLALCHEMY_DATABASE_URI` a
   `mysql+pymysql://root:@localhost/bd_anuncios`
