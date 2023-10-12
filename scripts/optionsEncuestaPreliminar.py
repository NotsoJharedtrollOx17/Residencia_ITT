def getIndicesIncidenciasInteres():
    incidencias_interes = [
        # * pregunta 3
        [3,4,5],
        [3,12,13],
        [3,22,23],
        [3,24,25],
        
        # * pregunta 4 y 5
        [4,5,20],
        [4,5,24],
        [4,5,25],
        
        # * pregunta 6
        [6,12,13],
        
        # * pregunta 12 y 13
        [12,13,14],
        [12,13,22],
        [12,13,23],
        [12,13,25],
        
        # * pregunta 14
        [14,20,21],
        [14,22,23],
        
        # * pregunta 17
        [17,18,22],
        [17,18,23],
        [17,18,24],
        
        # * pregunta 18
        [18,19,22],
    ]

    return incidencias_interes
    
def getOpcionesPregunta3():
    return ["17", "18", "19", "20", "21 o más"]

def getOpcionesPregunta4(abreviar=False):

    if abreviar:
        return [
            "C. Alta",
            "C. Media Alta",
            "C. Media",
            "C. Media Baja",
            "C. Baja",
        ]
    else:
        return [
            "Clase Alta",
            "Clase Media Alta",
            "Clase Media",
            "Clase Media Baja",
            "Clase Baja",
        ]

def getOpcionesPregunta5_6(abreviar=False):

    if abreviar:
        return ['Pri tt', 'Sec tt', 'Prepa/Bach tt', 'Lic tt', 'Posgrados']
    else:
        return [ # * pregunta 5 Y 6
            "Primaria terminada o trunca",
            "Secundaria terminada o trunca",
            "Prepatoria/Bachillerato Técnico terminado o trunco",
            "Licenciatura terminada o trunca",
            "Posgrados (Maestría, Doctorado, etc.)",
        ]

def getOpcionesPregunta7():
    return ["Sí", "No"]

def getOpcionesPregunta13_1622_24():
    return ['nunca', 'casi nunca', 'a veces', 'casi siempre', 'siempre']

def getOpcionesPregunta15_23():
    return ['muy malo', 'malo', 'regular', 'bueno', 'muy bueno']

def getOpcionesPregunta14():
    return ['menos de 5', '5 a 6', '7 a 8', '9 a 10', 'más de 10']

def getOpcionesPregunta25():
    return ['nula', 'muy poca', 'baja', 'moderada', 'bastante']

def getOpcionesPregunta26():
    return ['muy malo', 'malo', 'ni bueno ni malo', 'bueno', 'muy bueno']

def getOpcionesPregunta27():
    return ["Mujer", "Hombre", "No binario", "Prefiero no decir"]