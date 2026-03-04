from . import alumnos

from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from flask_migrate import Migrate
from alumnos.routes import alumnos
from models import db
from models import Alumnos, Maestros


@alumnos.route("/alumnos")
def listado():
    create_form = forms.UserForm2(request.form)
    alumno = Alumnos.query.all()
    return render_template("alumnos/listado.html", form=create_form, alumno=alumno)


@alumnos.route("/alumnos/alumnosCreate", methods=["GET", "POST"])
def Alumnos2():
    create_form = forms.UserForm2(request.form)
    if request.method == "POST":
        alum = Alumnos(
            nombre=create_form.nombre.data,
            apellidos=create_form.apellidos.data,
            email=create_form.email.data,
            telefono = create_form.telefono.data,
        )
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for("alumnos.listado"))
    return render_template("alumnos/Alumnos.html", form=create_form)


@alumnos.route("/alumnos/detalles", methods=["GET", "POST"])
def detalles():
    create_form = forms.UserForm2(request.form)
    if request.method == "GET":
        id = request.args.get("id")
        # select * from alumnos where id == id
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        id = request.args.get("id")
        nombre = alum1.nombre
        apellidos = alum1.apellidos
        email = alum1.email
        telefono = alum1.telefono
    return render_template(
        "alumnos/detalles.html", id=id, nombre=nombre, apellidos=apellidos, email=email, telefono=telefono
    )


@alumnos.route("/alumnos/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.UserForm2(request.form)
    if request.method == "GET":
        id = request.args.get("id")
        # select * from alumnos where id == id
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        create_form.id.data = request.args.get("id")
        create_form.nombre.data = str.rstrip(alum1.nombre)
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono
    if request.method == "POST":
        id = create_form.id.data
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        alum1.id = id
        alum1.nombre = str.rstrip(create_form.nombre.data)
        alum1.apellidos = create_form.apellidos.data
        alum1.email = create_form.email.data
        alum1.telefono = create_form.telefono.data
        db.session.add(alum1)
        db.session.commit()
        return redirect(url_for("alumnos.listado"))
    return render_template("alumnos/modificar.html", form=create_form)


@alumnos.route("/alumnos/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.UserForm2(request.form)
    if request.method == "GET":
        id = request.args.get("id")
        alum1 = db.session.query(Alumnos).filter(Alumnos.id == id).first()

        if alum1:
            create_form.id.data = alum1.id
            create_form.nombre.data = alum1.nombre
            create_form.apellidos.data = alum1.apellidos
            create_form.email.data = alum1.email
            create_form.telefono.data = alum1.telefono
            return render_template("alumnos/eliminar.html", form=create_form)

    if request.method == "POST":
        id = create_form.id.data
        alum = db.session.query(Alumnos).filter(Alumnos.id == id).first()
        if alum:
            db.session.delete(alum)
            db.session.commit()
        return redirect(url_for("alumnos.listado"))

    return render_template("alumnos/eliminar.html", form=create_form)
