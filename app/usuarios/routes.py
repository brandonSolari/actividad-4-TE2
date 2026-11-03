from flask import render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from . import bp
from ..extensions import db
from ..models import Usuario


@bp.route("/")
@login_required
def lista():
    usuarios = Usuario.query.order_by(Usuario.nombre).all()
    return render_template("usuarios/lista.html", usuarios=usuarios)


@bp.route("/nuevo", methods=["GET", "POST"])
@login_required
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not nombre or not email or not password:
            flash("Nombre, correo y contraseña son obligatorios.", "danger")
        elif Usuario.query.filter_by(email=email).first():
            flash("Ya existe un usuario con ese correo.", "danger")
        else:
            usuario = Usuario(nombre=nombre, email=email)
            usuario.set_password(password)
            db.session.add(usuario)
            db.session.commit()
            flash("Usuario registrado correctamente.", "success")
            return redirect(url_for("usuarios.lista"))

    return render_template("usuarios/form.html", usuario=None)


@bp.route("/<int:usuario_id>/editar", methods=["GET", "POST"])
@login_required
def editar(usuario_id):
    usuario = db.get_or_404(Usuario, usuario_id)

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        repetido = Usuario.query.filter(
            Usuario.email == email, Usuario.id != usuario.id
        ).first()

        if not nombre or not email:
            flash("Nombre y correo son obligatorios.", "danger")
        elif repetido:
            flash("Ya existe otro usuario con ese correo.", "danger")
        else:
            usuario.nombre = nombre
            usuario.email = email
            if password:  # si se deja vacío, se conserva la contraseña actual
                usuario.set_password(password)
            db.session.commit()
            flash("Usuario actualizado correctamente.", "success")
            return redirect(url_for("usuarios.lista"))

    return render_template("usuarios/form.html", usuario=usuario)


@bp.route("/<int:usuario_id>/eliminar", methods=["POST"])
@login_required
def eliminar(usuario_id):
    usuario = db.get_or_404(Usuario, usuario_id)

    if usuario.id == current_user.id:
        flash("No puedes eliminar tu propio usuario.", "danger")
    elif usuario.anuncios:
        flash("No se puede eliminar: el usuario tiene anuncios publicados.", "danger")
    else:
        db.session.delete(usuario)
        db.session.commit()
        flash("Usuario eliminado correctamente.", "success")

    return redirect(url_for("usuarios.lista"))
