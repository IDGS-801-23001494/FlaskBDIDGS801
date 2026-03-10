from . import cursos

from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from flask_migrate import Migrate
from cursos.routes import cursos
from models import db
from models import Alumnos, Maestros, Curso, Inscripcion

@cursos.route("/cursos", methods=['GET'])
def listado():
    create_form = forms.UserForm2(request.form)
    cursos = Curso.query.all()
    return render_template("cursos/listado.html",form=create_form,cursos=cursos)

@cursos.route("/cursos/crear", methods=["GET", "POST"])
def create():
    create_form = forms.CursoForm(request.form)
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula, f"{m.nombre} {m.apellidos}") for m in maestros]

    if request.method == 'POST':
        curso = Curso(
            nombre = str.rstrip(create_form.nombre.data),
            descripcion = create_form.descripcion.data,
            maestro_id = create_form.maestro_id.data
        )

        db.session.add(curso)
        db.session.commit()
        return redirect(url_for("cursos.listado"))
    return render_template("cursos/crear.html", form=create_form)

@cursos.route("/cursos/detalles", methods=["GET", "POST"])
def detalles():
    create_form = forms.CursoForm(request.form)
    if request.method == "GET":
        curso_id = request.args.get("id")

        curso = (db.session.query(Curso).filter(Curso.id == curso_id).first())
        
        if curso:
            curso_id = request.args.get("id")
            nombre = curso.nombre
            descripcion = curso.descripcion
            
            maestro = db.session.query(Maestros).filter(Maestros.matricula == curso.maestro_id).first()

            alumnos=curso.alumnos

    return render_template(
        "cursos/detalles.html",
        id=curso_id,
        nombre=nombre,
        descripcion=descripcion,
        maestro=maestro,
        alumnos=alumnos
    )



@cursos.route("/cursos/editar", methods=['GET','POST'])
def editar():
    create_form = forms.CursoForm(request.form)
    maestros = Maestros.query.all()
    create_form.maestro_id.choices = [(m.matricula,f"{m.nombre} {m.apellidos}") for m in maestros]

    if request.method == 'GET':
        curso_id = request.args.get("id")
        curso = db.session.query(Curso).filter(Curso.id == curso_id).first()

        if curso:
            create_form.id.data = request.args.get("id")
            create_form.nombre.data = str.rstrip(curso.nombre)
            create_form.descripcion.data = curso.descripcion
            create_form.maestro_id.data = curso.maestro_id
    
    if request.method == 'POST':
        curso_id = request.args.get("id")
        curso = db.session.query(Curso).filter(Curso.id == curso_id).first()

        curso.id = curso.id
        curso.nombre = str.rstrip(create_form.nombre.data)
        curso.descripcion = create_form.descripcion.data
        curso.maestro_id = create_form.maestro_id.data

        db.session.add(curso)
        db.session.commit()
        return redirect(url_for("cursos.listado"))
    
    return render_template("cursos/editar.html", form=create_form)

@cursos.route("/cursos/inscribir", methods=["GET", "POST"])
def inscribir():
    create_form = forms.CursoInscripcionForm(request.form)

    alumnos = Alumnos.query.all()
    create_form.alumno_id.choices = [(a.id, f"{a.nombre} {a.apellidos}") for a in alumnos]

    if request.method == "GET":
        curso_id = request.args.get("id")
        curso = db.session.query(Curso).filter(Curso.id == curso_id).first()

        return render_template("cursos/inscribir.html", form=create_form, curso=curso)

    if request.method == "POST":
        curso_id = request.args.get("id")
        curso = db.session.query(Curso).filter(Curso.id == curso_id).first()

        alumno_id = create_form.alumno_id.data
        alumno = db.session.query(Alumnos).filter(Alumnos.id == alumno_id).first()

        if alumno in curso.alumnos:
            flash("Ese alumno ya está inscrito en este curso.", "info")
            return redirect(url_for("cursos.inscribir", id=curso_id))

        curso.alumnos.append(alumno)
        db.session.commit()

        return redirect(url_for("cursos.listado", id=curso_id))

    return render_template("cursos/inscribir.html", form=create_form)
        


@cursos.route("/cursos/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.CursoForm(request.form)

    if request.method == "GET":
        curso_id = request.args.get("id")
        curso = db.session.query(Curso).filter(Curso.id == curso_id).first()

        if curso:
            curso_id = request.args.get("id")
            nombre = curso.nombre
            descripcion = curso.descripcion

            maestro = db.session.query(Maestros).filter(
                Maestros.matricula == curso.maestro_id
            ).first()

            create_form.id.data = curso.id
            create_form.nombre.data = curso.nombre
            create_form.descripcion.data = curso.descripcion
            create_form.maestro_id.data = curso.maestro_id

            return render_template(
                "cursos/eliminar.html",
                id=curso_id,
                nombre=nombre,
                descripcion=descripcion,
                maestro=maestro,
                form=create_form
            )

    if request.method == "POST":
        curso_id = create_form.id.data
        curso = db.session.query(Curso).filter(Curso.id == curso_id).first()

        if curso:
            Inscripcion.query.filter(Inscripcion.curso_id == curso.id).delete()
            db.session.delete(curso)
            db.session.commit()

        return redirect(url_for("cursos.listado"))

