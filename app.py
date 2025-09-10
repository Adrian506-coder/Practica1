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
    
    pusher_client.trigger("canalTrajes", "eventoTrajes", {"message": "Hola Mundo!"})
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

@app.route("/iniciarSesion", methods=["POST"])
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
    cursor.execute(sql, (usuario, contrasena))
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/trajes")
def trajes():
    return render_template("trajes.html")

@app.route("/tbodyTrajes")
def tbodyTrajes():
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

    return render_template("tbodyTrajes.html", trajes=registros)

@app.route("/trajes/guardar", methods=["POST", "GET"])
def guardarTraje():
    if not con.is_connected():
        con.reconnect()

    if request.method == "POST":
        data = request.get_json() or request.form
        nombre = data.get("txtNombre")
        descripcion = data.get("txtDescripcion")
    else: 
        nombre = request.args.get("nombre")
        descripcion = request.args.get("descripcion")
    if not nombre or not descripcion:
        return jsonify({"error": "Faltan parámetros"}), 400
        
    cursor = con.cursor()
    sql = """
    INSERT INTO trajes (nombreTraje, descripcion)
    VALUES (%s, %s)
    """
    cursor.execute(sql, (nombre, descripcion))
    con.commit()
    con.close()

    pusherProductos()

    return make_response(jsonify({"mensaje": "Traje guardado correctamente"}))

@app.route("/trajes/eliminar", methods=["POST", "GET"])
def eliminartraje():
    if not con.is_connected():
        con.reconnect()

    if request.method == "POST":
        IdTraje = request.form.get("id")
    else:
        IdTraje = request.args.get("id")

    cursor = con.cursor()
    sql = "DELETE FROM trajes WHERE IdTraje = %s"
    val = (IdTraje,)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    pusherProductos()

    return make_response(jsonify({"status": "ok"}))


##if __name__ == "__main__":
##    app.run(port=5001, debug=True)



