from kakebo import app
from flask import jsonify, render_template, request, redirect, url_for, flash
from kakebo.forms import MovimientosForm
from datetime import date

import sqlite3


def consultaSQL(query, parametros=[]):
    # Abrimos la conexion
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()
    # Ejecutamos la consulta
    cur.execute(query, parametros)
    # Obtenemos los datos de la consulta
    claves = cur.description
    filas = cur.fetchall()
    # Procesar los datos para devolver una lista de diccionarios. Un diccionario por fila
    resultado = []
    for fila in filas:
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor
        resultado.append(d)
    conexion.close()
    return resultado

def modificaTablaSQL(query, parametros):
    # Abrimos la conexion
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()
    # Ejecutamos la consulta
    cur.execute(query,parametros)
    # Obtenemos los datos de la consulta
    conexion.commit()
    conexion.close()


@app.route('/')
def index():
    movimientos = consultaSQL("Select T1.id, T1.fecha, T1.concepto, T1.categoria,T1.esGasto, T1.cantidad, T1.importe, \
                    Sum(T2.importe) as Acumulado from movimientos T1 \
                    join movimientos T2 on (T1.id >= T2.id) \
                    Group By T1.id, T1.fecha, T1.concepto, T1.categoria,T1.esGasto, T1.cantidad, T1.importe \
                    Order by T1. id;")
    return render_template('movimientos.html', datos = movimientos)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo():
    formulario = MovimientosForm()

    if request.method == 'GET':
        return render_template('alta.html', form = formulario)
    else:

        if formulario.validate():
            query = "INSERT INTO movimientos (fecha, concepto, categoria, esGasto, cantidad) VALUES (?, ?, ?, ?, ?)"
            try:
                modificaTablaSQL(query, [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                formulario.esGasto.data, formulario.cantidad.data])

            except sqlite3.Error as el_error:
                print("Error en SQL INSERT", el_error)
                flash("Se ha producido un error en la base de datos. Pruebe en unos minutos", "error")
                return render_template('alta.html', form=formulario)

            return redirect(url_for("index"))

            #Redirect a la ruta /
        else:
            return render_template('alta.html', form = formulario)



@app.route('/borrar/<int:id>', methods=['GET', 'POST'])
def borrar(id):
    if request.method == 'GET':
        filas = consultaSQL("SELECT * from movimientos WHERE id=?", [id])
        
        if len(filas) == 0:
            flash("El registro no existe", "error")
            return render_template('borrar.html', )

        return render_template ('borrar.html', movimiento=filas[0])
    else:
        try:
            modificaTablaSQL("DELETE FROM movimientos WHERE id =?;", [id])
        except sqlite3.Error as e:
            flash("Se haproducido un error de base de datos. Vuelve a intentarlo", 'error') #ponemos error para crear categoria y hacer mensaje
            return redirect(url_for('index'))
        flash("Borrado realizado con éxito", 'aviso')#ponemos aviso para crear categoria y hacer mensaje
        return redirect(url_for('index'))

@app.route('/modificar/<int:id>', methods=['GET', 'POST'])
def modificar(id):
    if request.method == 'GET':
        filas = consultaSQL("SELECT * FROM movimientos WHERE id=?", [id])
        if len(filas) == 0:
            flash("El registro no existe", "error")
            return render_template('modificar.html', )
        registro = filas[0]
        registro['fecha'] = date.fromisoformat(registro['fecha'])

        formulario = MovimientosForm(data=registro)
        
        return render_template('modificar.html', form=formulario)
    else:
        modificaTablaSQL("UPDATE movimientos SET fecha =?, \
            concepto =?,  categoria =?, esGasto =?, cantidad =? \
                WHERE ID =?;", [formulario.fecha.data, formulario.concepto.data, formulario.categoria.data,
                                formulario.esGasto.data, formulario.cantidad.data, formulario.id.data])    
        return redirect(url_for('index'))   

 
    