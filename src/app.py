from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS
from config import config

app = Flask(__name__)

# Habilitar CORS para las rutas de alumnos y maestros desde Angular
CORS(app, resources={
    r"/alumnos*": {"origins": "http://localhost:4200"},
    r"/maestros*": {"origins": "http://localhost:4200"}
})

conexion = MySQL(app)

#   SECCIÓN ALUMNOS-------------------------------------------------------------------------------

def leer_alumno_bd(matricula):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM alumnos WHERE matricula = %s"
        cursor.execute(sql, (matricula,))
        datos = cursor.fetchone()
        cursor.close()

        if datos is not None:
            return {
                "matricula": datos[0],
                "nombre": datos[1],
                "apaterno": datos[2],
                "amaterno": datos[3],
                "correo": datos[4]
            }
        return None
    except Exception as ex:
        raise ex

@app.route("/alumnos", methods=['GET'])
def lista_alumnos():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM alumnos"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursor.close()

        alumnos = []
        for fila in datos:
            alumno = {
                "matricula": fila[0],
                "nombre": fila[1],
                "apaterno": fila[2],
                "amaterno": fila[3],
                "correo": fila[4]
            }
            alumnos.append(alumno)
        return jsonify({'alumnos': alumnos, 'mensaje': 'Lista de alumnos', 'exito': True})
    except Exception as ex:
        return jsonify({"message": f"error {ex}", 'exito': False}), 500

@app.route("/alumnos/<mat>", methods=['GET'])
def leer_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno is not None:
            return jsonify({'alumno': alumno, 'mensaje': 'alumno encontrado', 'exito': True})
        else:
            return jsonify({'alumno': None, 'mensaje': 'alumno no encontrado', 'exito': False}), 404
    except Exception as ex:
        return jsonify({"message": f"error {ex}", 'exito': False}), 500

@app.route("/alumnos", methods=['POST'])
def registra_alumno():
    try:
        data = request.json
        alumno = leer_alumno_bd(data['matricula'])
        if alumno is not None:
            return jsonify({"mensaje": "Alumno ya existe", "exito": False})
        
        cursor = conexion.connection.cursor()
        sql = """INSERT INTO alumnos (matricula, nombre, apaterno, amaterno, correo) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            data['matricula'],
            data['nombre'],
            data['apaterno'],
            data['amaterno'],
            data['correo']
        ))
        conexion.connection.commit()
        cursor.close()
        return jsonify({'mensaje': "Alumno registrado", "exito": True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}", 'exito': False}), 500

@app.route("/alumnos/<mat>", methods=['PUT'])
def actualizar_alumno(mat):
    try:
        data = request.json
        alumno = leer_alumno_bd(mat)
        if alumno is not None:
            cursor = conexion.connection.cursor()
            sql = """UPDATE alumnos SET nombre=%s, apaterno=%s, amaterno=%s, correo=%s 
                     WHERE matricula=%s"""
            cursor.execute(sql, (
                data['nombre'],
                data['apaterno'],
                data['amaterno'],
                data['correo'],
                mat
            ))
            conexion.connection.commit()
            cursor.close()
            return jsonify({'mensaje': "Alumno actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado", 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}", 'exito': False}), 500

@app.route("/alumnos/<int:mat>", methods=['DELETE'])
def eliminar_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)
        if alumno is not None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM alumnos WHERE matricula = %s"
            cursor.execute(sql, (mat,))
            conexion.connection.commit()
            cursor.close()
            return jsonify({'mensaje': "Alumno eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Alumno no encontrado.", 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}", 'exito': False}), 500


#  SECCIÓN MAESTROS---------------------------------------------------

def leer_maestro_bd(id_maestro):
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM maestros WHERE Idmaestro = %s"
        cursor.execute(sql, (id_maestro,))
        datos = cursor.fetchone()
        cursor.close()

        if datos is not None:
            return {
                "Idmaestro": datos[0],
                "nombre": datos[1],
                "apaterno": datos[2],
                "amaterno": datos[3],
                "correo": datos[4]
            }
        return None
    except Exception as ex:
        raise ex

@app.route("/maestros", methods=['GET'])
def lista_maestros():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM maestros"
        cursor.execute(sql)
        datos = cursor.fetchall()
        cursor.close()

        maestros = []
        for fila in datos:
            maestro = {
                "Idmaestro": fila[0],
                "nombre": fila[1],
                "apaterno": fila[2],
                "amaterno": fila[3],
                "correo": fila[4]
            }
            maestros.append(maestro)
        return jsonify({'maestros': maestros, 'mensaje': 'Lista de maestros', 'exito': True})
    except Exception as ex:
        return jsonify({"message": f"error {ex}", 'exito': False}), 500

@app.route("/maestros/<int:id>", methods=['GET'])
def leer_maestro(id):
    try:
        maestro = leer_maestro_bd(id)
        if maestro is not None:
            return jsonify({'maestro': maestro, 'mensaje': 'maestro encontrado', 'exito': True})
        else:
            return jsonify({'maestro': None, 'mensaje': 'maestro no encontrado', 'exito': False}), 404
    except Exception as ex:
        return jsonify({"message": f"error {ex}", 'exito': False}), 500

@app.route("/maestros", methods=['POST'])
def registra_maestro():
    try:
        data = request.json
        maestro = leer_maestro_bd(data['Idmaestro'])
        if maestro is not None:
            return jsonify({"mensaje": "El maestro ya existe", "exito": False})

        cursor = conexion.connection.cursor()
        sql = """INSERT INTO maestros (Idmaestro, nombre, apaterno, amaterno, correo) 
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (
            data['Idmaestro'],
            data['nombre'],
            data['apaterno'],
            data['amaterno'],
            data['correo']
        ))
        conexion.connection.commit()
        cursor.close()
        return jsonify({'mensaje': "Maestro registrado", "exito": True})
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}", 'exito': False}), 500

@app.route("/maestros/<int:id>", methods=['PUT'])
def actualizar_maestro(id):
    try:
        data = request.json
        maestro = leer_maestro_bd(id)
        if maestro is not None:
            cursor = conexion.connection.cursor()
            sql = """UPDATE maestros SET nombre=%s, apaterno=%s, amaterno=%s, correo=%s 
                     WHERE Idmaestro=%s"""
            cursor.execute(sql, (
                data['nombre'],
                data['apaterno'],
                data['amaterno'],
                data['correo'],
                id
            ))
            conexion.connection.commit()
            cursor.close()
            return jsonify({'mensaje': "Maestro actualizado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Maestro no encontrado", 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}", 'exito': False}), 500

@app.route("/maestros/<int:id>", methods=['DELETE'])
def eliminar_maestro(id):
    try:
        maestro = leer_maestro_bd(id)
        if maestro is not None:
            cursor = conexion.connection.cursor()
            sql = "DELETE FROM maestros WHERE Idmaestro = %s"
            cursor.execute(sql, (id,))
            conexion.connection.commit()
            cursor.close()
            return jsonify({'mensaje': "Maestro eliminado.", 'exito': True})
        else:
            return jsonify({'mensaje': "Maestro no encontrado.", 'exito': False}), 404
    except Exception as ex:
        return jsonify({'mensaje': f"Error: {ex}", 'exito': False}), 500


# ====================================================================
#                       MANEJADOR DE ERRORES Y RUN
# ====================================================================

def pagina_no_encontrada(error):
    return "<h1>Pagina no encontrada</h1>", 404

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000, debug=True)