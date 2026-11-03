from flask import render_template, request
from . import bp
from ..models import Anuncio, Categoria


@bp.route("/")
def inicio():
    categoria_id = request.args.get("categoria", type=int)
    consulta = Anuncio.query.order_by(Anuncio.fecha_publicacion.desc())
    if categoria_id:
        consulta = consulta.filter_by(categoria_id=categoria_id)
    anuncios = consulta.all()
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template(
        "index.html",
        anuncios=anuncios,
        categorias=categorias,
        categoria_activa=categoria_id,
    )
