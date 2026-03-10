from wtforms import Form
from wtforms import StringField, IntegerField, SelectField
from wtforms import EmailField
from wtforms import validators


class UserForm2(Form):
    id = IntegerField(
        "id", [validators.number_range(min=1, max=20, message="valor no valido")]
    )
    nombre = StringField(
        "nombre",
        [
            validators.DataRequired(message="El nombre es requerido"),
            validators.length(min=4, max=20, message="requiere min=4 max=20"),
        ],
    )
    apellidos = StringField(
        "apellidos", [validators.DataRequired(message="Los apellidos son requeridos")]
    )
    email = EmailField(
        "email",
        [
            validators.DataRequired(message="El correo es requerido"),
            validators.Email(message="Ingrese un correo valido"),
        ],
    )
    telefono = StringField(
        "telefono",
        [
            validators.DataRequired(message="El telefono es requerido"),
            validators.length(min=10, max=10, message="Deben ser 10 digitos"),
        ],
    )


class MaestroForm(Form):
    matricula = IntegerField(
        "matricula", [validators.number_range(min=1, max=10, message="valor no valido")]
    )
    nombre = StringField(
        "nombre",
        [
            validators.DataRequired(message="El nombre es requerido"),
            validators.length(min=4, max=20, message="requiere min=4 max=20"),
        ],
    )
    apellidos = StringField(
        "apellidos", [validators.DataRequired(message="Los apellidos son requeridos")]
    )
    especialidad = StringField(
        "especialidad",
        [
            validators.DataRequired(message="El correo es requerido"),
        ],
    )
    email = EmailField(
        "email",
        [
            validators.DataRequired(message="El correo es requerido"),
            validators.Email(message="Ingrese un correo valido"),
        ],
    )


class CursoForm(Form):
    id = IntegerField(
        "Curso", [validators.number_range(min=1, max=20, message="valor no valido")]
    )
    nombre = StringField(
        "Nombre", [validators.DataRequired(message="El nombre es requerido")]
    )
    descripcion = StringField("Descripción", [validators.DataRequired(message="La descripcion es requerido")])
    maestro_id = SelectField(
        "Maestro",
        coerce=int,
        validators=[validators.DataRequired(message="El maestro es requerido")],
    )


class CursoInscripcionForm(Form):
    alumno_id = SelectField(
        "Alumno",
        coerce=int,
        validators=[
            validators.DataRequired(message="El alumno es requerido"),
        ],
    )
    curso_id = IntegerField(
        "Curso",
        [
            validators.DataRequired(message="El alumno es requerido"),
            validators.number_range(min=1, max=20, message="valor no valido"),
        ],
    )
