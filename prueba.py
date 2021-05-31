import sqlite3

campos = ('Nombre', 'Apellidos', 'Matematicas', 'Lengua', 'Naturales', 'Sociales')
notas = [('Pedro', 'Jimenez', 10, 9, 8, 9), ('Juana', 'Rodriguez', 9, 4, 9, 8), ('Andres', 'Stevensson', 6, 7, 9, 5)]

@app.route('/EjercicioMayo23')
def ejercicio():
    boletines = []
    for valor in notas:
        d = {}
        for posicion, i in enumerate(valor):
            d[campos[posicion]] = i
        d['media'] = (int(valor[2])+int(valor[3])+int(valor[4])+int(valor[5]))/int(len(valor)-2)
        d['grafico'] = int(d['media']*2)*'x'
        boletines.append(d)
    return json.dumps(boletines)


@app.route('/acumulado')
def acumulado():
    conexion = sqlite3.connect("movimientos.db")
    cur = conexion.cursor()
    
    cur.execute("Select T1.id, T1.fecha, T1.concepto, T1.categoria,T1.esGasto, T1.cantidad, T1.importe, \
                    Sum(T2.importe) as Acumulado from movimientos T1 \
                    join movimientos T2 on (T1.id >= T2.id) \
                    Group By T1.id, T1.fecha, T1.concepto, T1.categoria,T1.esGasto, T1.cantidad, T1.importe \
                    Order by T1. id;")
    
    claves = cur.description
    filas = cur.fetchall()
    
    movimientos = []
    for fila in filas:
        d = {}
        for tclave, valor in zip(claves, fila):
            d[tclave[0]] = valor   
        movimientos.append(d)
                    
    conexion.close()

    #return jsonify(movimientos)
    return render_template('movimientos.html', datos = movimientos)
