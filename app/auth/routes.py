from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import bp
from ..models import Usuario


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.inicio"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario and usuario.check_password(password):
            login_user(usuario)
            siguiente = request.args.get("next", "")
            if siguiente.startswith("/") and not siguiente.startswith("//"):
                return redirect(siguiente)
            return redirect(url_for("main.inicio"))

        flash("Correo o contraseña incorrectos.", "danger")

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Cerraste sesión correctamente.", "info")
    return redirect(url_for("auth.login"))
