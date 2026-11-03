from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required
from . import bp
from ..extensions import db
from ..models import Categoria


@bp.route("/")
@login_required
def lista():
    categorias = Categoria.query.order_by(Categoria.nombre).all()
    return render_template("categorias/lista.html", categorias=categorias)


@bp.route("/nueva", methods=["GET", "POST"])
@login_required
def nueva():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        existe = Categoria.query.filter(
            db.func.lower(Categoria.nombre) == nombre.lower()
        ).first()

        if not nombre:
            flash("El nombre de la categoría es obligatorio.", "danger")
        elif existe:
            flash("Ya existe una categoría con ese nombre.", "danger")
        else:
            db.session.add(Categoria(nombre=nombre, descripcion=descripcion))
            db.session.commit()
            flash("Categoría registrada correctamente.", "success")
            return redirect(url_for("categorias.lista"))

    return render_template("categorias/form.html", categoria=None)


@bp.route("/<int:categoria_id>/editar", methods=["GET", "POST"])
@login_required
def editar(categoria_id):
    categoria = db.get_or_404(Categoria, categoria_id)

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        descripcion = request.form.get("descripcion", "").strip()

        repetida = Categoria.query.filter(
            db.func.lower(Categoria.nombre) == nombre.lower(),
            Categoria.id != categoria.id,
        ).first()

        if not nombre:
            flash("El nombre de la categoría es obligatorio.", "danger")
        elif repetida:
            flash("Ya existe otra categoría con ese nombre.", "danger")
        else:
            categoria.nombre = nombre
            categoria.descripcion = descripcion
            db.session.commit()
            flash("Categoría actualizada correctamente.", "success")
            return redirect(url_for("categorias.lista"))

    return render_template("categorias/form.html", categoria=categoria)


@bp.route("/<int:categoria_id>/eliminar", methods=["POST"])
@login_required
def eliminar(categoria_id):
    categoria = db.get_or_404(Categoria, categoria_id)

    if categoria.anuncios:
        flash("No se puede eliminar: la categoría tiene anuncios asociados.", "danger")
    else:
        db.session.delete(categoria)
        db.session.commit()
        flash("Categoría eliminada correctamente.", "success")

    return redirect(url_for("categorias.lista"))
