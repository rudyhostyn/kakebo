campos = ('Nombre', 'Apellidos', 'Matematicas', 'Lengua', 'Naturales', 'Sociales')
notas = [('Pedro', 'Jimenez', 10, 9, 8, 9), ('Juana', 'Rodriguez', 9, 4, 9, 8), ('Andres', 'Stevensson', 6, 7, 9, 5)]

boletines = []
for valor in notas:
    d = {}
    for posicion, campo in enumerate(valor):
        d[campos[posicion]] = campo
    d['media'] = (int(valor[2])+int(valor[3])+int(valor[4])+int(valor[5]))/int(len(valor)-2)
    d['grafico'] = int(d['media']*2)*'x'
    boletines.append(d)
print(boletines)

'''
#usando ZIP
bolet = []
for alumno in notas:
    d ={}
    for clave, valor in zip(campos, alumno):
        d[clave] = valor
    bolet.append(d)
print(bolet)
'''


