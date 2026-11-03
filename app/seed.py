from .extensions import db
from .models import Usuario, Categoria


def sembrar_datos():
    """Crea un usuario administrador y categorías de ejemplo si la base está vacía."""
    if Usuario.query.count() == 0:
        admin = Usuario(nombre="Administrador", email="admin@correo.com")
        admin.set_password("admin123")
        db.session.add(admin)

    if Categoria.query.count() == 0:
        ejemplos = [
            ("Avisos generales", "Comunicados para toda la comunidad"),
            ("Eventos", "Charlas, talleres y actividades"),
            ("Compra y venta", "Artículos, libros y servicios"),
        ]
        for nombre, descripcion in ejemplos:
            db.session.add(Categoria(nombre=nombre, descripcion=descripcion))

    db.session.commit()
