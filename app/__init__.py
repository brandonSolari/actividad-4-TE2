from flask import Flask
from .extensions import db, login_manager


def create_app(config_class="config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from .main import bp as main_bp
    from .auth import bp as auth_bp
    from .usuarios import bp as usuarios_bp
    from .categorias import bp as categorias_bp
    from .anuncios import bp as anuncios_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
    app.register_blueprint(categorias_bp, url_prefix="/categorias")
    app.register_blueprint(anuncios_bp, url_prefix="/anuncios")

    @app.context_processor
    def inyectar_globales():
        return {"institucion": app.config["INSTITUCION"]}

    with app.app_context():
        from . import models
        from .seed import sembrar_datos
        db.create_all()
        sembrar_datos()

    return app
