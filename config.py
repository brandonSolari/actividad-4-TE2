import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave-secreta-provisional")

    # SQLite (por defecto): crea el archivo instance/bd_anuncios.db
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///bd_anuncios.db")
    # MySQL (XAMPP): instala "pip install pymysql cryptography" y usa
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/bd_anuncios"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Aparece en la cabecera institucional y en el título de cada página
    INSTITUCION = "Universidad Publica de el Alto "
