from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from . import bp
from ..extensions import db
from ..models import Anuncio, Categoria, Usuario


def _opciones():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    return categorias, usuarios


def _leer_formulario():
    return {
        "titulo": request.form.get("titulo", "").strip(),
        "contenido": request.form.get("contenido", "").strip(),
        "categoria_id": request.form.get("categoria_id", type=int),
        "usuario_id": request.form.get("usuario_id", type=int),
    }


def _validar(datos):
    if not datos["titulo"] or not datos["contenido"]:
        return "El título y el contenido son obligatorios."
    if not db.session.get(Categoria, datos["categoria_id"] or 0):
        return "Selecciona una categoría válida."
    if not db.session.get(Usuario, datos["usuario_id"] or 0):
        return "Selecciona un usuario válido."
    return None


@bp.route("/")
@login_required
def lista():
    anuncios = Anuncio.query.order_by(Anuncio.fecha_publicacion.desc()).all()
    return render_template("anuncios/lista.html", anuncios=anuncios)


@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        datos = _leer_formulario()
        error = _validar(datos)
        if error:
            flash(error, "danger")
        else:
            db.session.add(Anuncio(**datos))
            db.session.commit()
            flash("Anuncio publicado correctamente.", "success")
            return redirect(url_for("anuncios.lista"))

    categorias, usuarios = _opciones()
    return render_template(
        "anuncios/form.html", anuncio=None, categorias=categorias, usuarios=usuarios
    )


@bp.route("/<int:anuncio_id>/editar", methods=["GET", "POST"])
@login_required
def editar(anuncio_id):
    anuncio = db.get_or_404(Anuncio, anuncio_id)

    if request.method == "POST":
        datos = _leer_formulario()
        error = _validar(datos)
        if error:
            flash(error, "danger")
        else:
            anuncio.titulo = datos["titulo"]
            anuncio.contenido = datos["contenido"]
            anuncio.categoria_id = datos["categoria_id"]
            anuncio.usuario_id = datos["usuario_id"]
            db.session.commit()
            flash("Anuncio actualizado correctamente.", "success")
            return redirect(url_for("anuncios.lista"))

    categorias, usuarios = _opciones()
    return render_template(
        "anuncios/form.html", anuncio=anuncio, categorias=categorias, usuarios=usuarios
    )


@bp.route("/<int:anuncio_id>/eliminar", methods=["POST"])
@login_required
def eliminar(anuncio_id):
    anuncio = db.get_or_404(Anuncio, anuncio_id)
    db.session.delete(anuncio)
    db.session.commit()
    flash("Anuncio eliminado correctamente.", "success")
    return redirect(url_for("anuncios.lista"))
