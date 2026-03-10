from . import maestros

from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from flask_migrate import Migrate
from maestros.routes import maestros, maestros
from models import db
from models import Alumnos, Maestros


@maestros.route("/maestros", methods=["GET", "POST"])
def listado():
    create_form = forms.MaestroForm(request.form)
    maes = Maestros.query.all()
    return render_template("maestros/listadoMaes.html", form=create_form, maestros=maes)


@maestros.route("/maestros/maestrosCreate", methods=["GET", "POST"])
def maestrosCreate():
    create_form = forms.MaestroForm(request.form)
    if request.method == "POST":
        maes = Maestros(
            matricula=create_form.matricula.data,
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            especialidad=create_form.especialidad.data,
            email=create_form.email.data,
        )
        db.session.add(maes)
        db.session.commit()
        return redirect(url_for("maestros.listado"))
    return render_template("maestros/crearMaes.html", form=create_form)


@maestros.route("/maestros/detallesMaes", methods=["GET", "POST"])
def detallesMaes():
    create_form = forms.MaestroForm(request.form)
    if request.method == "GET":
        matricula = request.args.get("matricula")

        maes = (
            db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        )
        matricula = request.args.get("matricula")
        nombre = maes.nombre
        apellidos = maes.apellidos
        especialidad = maes.especialidad
        email = maes.email
        cursos = maes.cursos
    return render_template(
        "maestros/detallesMaes.html",
        matricula=matricula,
        nombre=nombre,
        apellidos=apellidos,
        especialidad=especialidad,
        email=email,
        cursos=cursos
    )

@maestros.route("/maestros/modificarMaes", methods=["GET", "POST"])
def modificarMaes():
    create_form = forms.MaestroForm(request.form)
    if request.method == "GET":
        matricula = request.args.get("matricula")
        maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        create_form.matricula.data = request.args.get("matricula")
        create_form.nombre.data = str.rstrip(maes.nombre)
        create_form.apellidos.data = maes.apellidos
        create_form.especialidad.data = maes.especialidad
        create_form.email.data = maes.email
    if request.method == "POST":
        matricula = create_form.matricula.data
        maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        maes.matricula = matricula
        maes.nombre = str.rstrip(create_form.nombre.data)
        maes.apellidos = create_form.apellidos.data
        maes.especialidad = create_form.especialidad.data
        maes.email = create_form.email.data
        db.session.add(maes)
        db.session.commit()
        return redirect(url_for("maestros.listado"))
    return render_template("maestros/editarMaes.html", form=create_form)

@maestros.route("/maestros/eliminarMaes", methods=["GET", "POST"])
def eliminar():
    create_form = forms.MaestroForm(request.form)
    if request.method == "GET":
        matricula = request.args.get("matricula")
        maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()

        if maes:
            create_form.matricula.data = maes.matricula
            create_form.nombre.data = maes.nombre
            create_form.apellidos.data = maes.apellidos
            create_form.especialidad.data = maes.especialidad
            create_form.email.data = maes.email
            return render_template("/maestros/eliminarMaes.html", form=create_form)

    if request.method == "POST":
        matricula = create_form.matricula.data
        maes = db.session.query(Maestros).filter(Maestros.matricula == matricula).first()
        if maes:
            db.session.delete(maes)
            db.session.commit()
        return redirect(url_for("maestros.listado"))

    return render_template("/maestros/eliminarMaes.html", form=create_form)



@maestros.route("/maestros/perfil/<nombre>")
def perfil(nombre):
    return f"Perfil de {nombre}"
