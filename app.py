# python.exe -m venv .venv
# cd .venv/Scripts
# activate.bat
# py -m ensurepip --upgrade
# pip install -r requirements.txt

from flask import Flask

from flask import render_template
from flask import request
from flask import jsonify, make_response

import mysql.connector

import datetime
import pytz

from flask_cors import CORS, cross_origin

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_23005256_bd",
    user="u760464709_23005256_usr",
    password="~6ru!MMJZzX"
)

app = Flask(__name__)
CORS(app)

def pusherProductos():
    import pusher
    
    pusher_client = pusher.Pusher(
      app_id='2046097',
      key='1007852abe277cd3e121',
      secret='7c6cff8082dfcc0b42a9',
      cluster='us2',
      ssl=True
    )
    
    pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
    return make_response(jsonify({}))

@app.route("/")
def index():
    if not con.is_connected():
        con.reconnect()

    con.close()

    return render_template("index.html")

@app.route("/app")
def app2():
    if not con.is_connected():
        con.reconnect()

    con.close()

    return render_template("login.html")
    # return "<h5>Hola, soy la view app</h5>"

@app.route("/iniciarSesion", methods=["POST"])
# Usar cuando solo se quiera usar CORS en rutas específicas
# @cross_origin()
def iniciarSesion():
    if not con.is_connected():
        con.reconnect()

    usuario    = request.form["txtUsuario"]
    contrasena = request.form["txtContrasena"]

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT Id_Usuario
    FROM usuarios

    WHERE Nombre_Usuario = %s
    AND Contrasena = %s
    """
    val    = (usuario, contrasena)

    cursor.execute(sql, val)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/trajes")
def trajes():
    return render_template("trajes.html")

@app.route("/tbodyTrajes")
def tbodyProductos():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql    = """
    SELECT IdTraje,
           nombreTraje,
           descripcion

    FROM trajes

    ORDER BY IdTraje DESC

    LIMIT 10 OFFSET 0
    """

    cursor.execute(sql)
    registros = cursor.fetchall()

    # Si manejas fechas y horas
    """
    for registro in registros:
        fecha_hora = registro["Fecha_Hora"]

        registro["Fecha_Hora"] = fecha_hora.strftime("%Y-%m-%d %H:%M:%S")
        registro["Fecha"]      = fecha_hora.strftime("%d/%m/%Y")
        registro["Hora"]       = fecha_hora.strftime("%H:%M:%S")
    """

    return render_template("tbodyTrajes.html", productos=registros)

# Usar cuando solo se quiera usar CORS en rutas específicas
# @cross_origin()
@app.route("/traje", methods=["POST"])
def guardarTraje():
    if not con.is_connected():
        con.reconnect()

    nombre = request.form["txtNombre"]
    descripcion = request.form["txtDescripcion"]

    cursor = con.cursor()
    sql = """
    INSERT INTO trajes (nombreTraje, descripcion)
    VALUES (%s, %s)
    """
    val = (nombre, descripcion)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({"mensaje": "Traje guardado correctamente"}))

@app.route("/trajes", methods=["GET"])
def listarTrajes():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    sql = """
    SELECT Id_Traje, nombreTraje, descripcion
    FROM trajes
    ORDER BY IdTraje DESC
    """
    cursor.execute(sql)
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))


