#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import subprocess
import sqlite3
import json

from bottle import route, run, response, request, abort, error, static_file, template
from utils import utilidades

@route('/OT/', method='OPTIONS') 
def enable_CORS_OT():
    utilidades.permitir_CORS()
    return json.dumps({'status': 200, 'mensaje': 'OK'})

@route('/OT/:ot', method='OPTIONS')
def enable_CORS_OT(ot):
    utilidades.permitir_CORS()
    return json.dumps({'status': 200, 'mensaje': 'OK'})

@route('/OT/QRY/:qry', method='OPTIONS')
def enable_CORS_OT(ot):
    utilidades.permitir_CORS()
    return json.dumps({'status': 200, 'mensaje': 'OK'})



#===============================================================================
# Añadimos el registro.
# curl -i http://localhost:6789/OT/ -H "Content-type: application/json" -X POST -d '{"ot": "GMIK231", "descripcion": "Reg: 1", "tipo": "w", "orden": 10, "ultimo_transporte": "2018-01-05T12:23:15.000Z"}'
#===============================================================================
@route('/OT/', method='POST') 
def post_OT():
    utilidades.permitir_CORS()
    datos_json = request.body.read()
    if not datos_json:
        abort(400, 'NO se recibieron datos')
    else:
        objeto_datos = json.loads(datos_json.decode("utf-8"))
        if not 'ot'          in objeto_datos          or \
           not 'descripcion' in objeto_datos          or \
           not 'tipo'        in objeto_datos          or \
           not 'orden'       in objeto_datos:
           abort(400, 'NO se especificaron todos los datos')
        else:
            try:
                if not 'ultimo_transporte' in objeto_datos or objeto_datos['ultimo_transporte'] == '':
                    cursor.execute("INSERT INTO ordenes (ot, descripcion, tipo, orden) VALUES (?, ?, ?, ?)", \
                                (objeto_datos['ot'],          \
                                objeto_datos['descripcion'], \
                                objeto_datos['tipo'],        \
                                objeto_datos['orden']))
                else:
                    cursor.execute("INSERT INTO ordenes (ot, descripcion, tipo, orden, ultimo_transporte) VALUES (?, ?, ?, ?, ?)", \
                                (objeto_datos['ot'],          \
                                objeto_datos['descripcion'], \
                                objeto_datos['tipo'],        \
                                objeto_datos['orden'],
                                datetime.datetime.fromtimestamp(time.mktime(time.strptime(objeto_datos['ultimo_transporte'], "%Y-%m-%dT%H:%M:%S.%fZ")))
                                ))
                conexion.commit()

            except sqlite3.Error as err:
                abort(400, 'ERROR al insertar datos')

        return json.dumps({'status': 200, 'mensaje': 'OK'})



#===============================================================================
# Consulta de todos los registros
# curl -i http://localhost:6789/OT/ -H "Content-type: application/json" -X GET
#===============================================================================
@route('/OT/', method='GET')
def get_OTs():
    utilidades.permitir_CORS()
    registros = []
    for fila in cursor.execute("SELECT * FROM ordenes"):
        columnas = ("ot", "descripcion", "tipo", "orden", "ultimo_transporte")
        registros.append(utilidades.fila_a_diccionario(columnas, fila))

    if registros:
       return json.dumps(registros)
    else:
       abort(404, 'No esixte el recurso')



#===============================================================================
# Consulta de un registro concreto.
# curl -i http://localhost:6789/OT/GMIK231 -H "Content-type: application/json" -X GET
#===============================================================================
@route('/OT/:ot', method='GET')
def get_OT(ot):
    utilidades.permitir_CORS()
    SQL = """
          SELECT ot,
                 descripcion,
                 tipo,
                 orden,
                 ultimo_transporte
            FROM ordenes
           WHERE ot = ?
        ORDER BY ot,
                 descripcion
          """

    cursor.execute(SQL, (ot,))
    fila = cursor.fetchone()
    columnas = ("ot", "descripcion", "tipo", "orden", "ultimo_transporte")
    if fila:
       return json.dumps(utilidades.fila_a_diccionario(columnas, fila))
    else:
       abort(404, 'No esixte el recurso')



#===============================================================================
# Consulta de registros que cumplen las condiciones recibidas como parametro.
# curl -i http://localhost:6789/OT/QRY/'\{"descripcionLike":"Reg"\}' -H "Content-type: application/json" -X GET
#===============================================================================
@route('/OT/QRY/:qry', method='GET')
def get_qry(qry):
    utilidades.permitir_CORS()
    SQL = """
          SELECT ot,
                 descripcion,
                 tipo,
                 orden,
                 ultimo_transporte
            FROM ordenes
           WHERE 1 = 1
          """

    datos_json = qry
    objeto_datos = json.loads(datos_json.decode("utf-8"))
    if 'descripcionLike' in objeto_datos:
        SQL = SQL + " AND descripcion LIKE '%" + objeto_datos['descripcionLike'] + "%' "    
    if 'tipoEq' in objeto_datos:
        SQL = SQL + " AND tipo = '" + objeto_datos['tipoEq'] + "' "    

    registros = []
    for fila in cursor.execute(SQL):
        columnas = ("ot", "descripcion", "tipo", "orden", "ultimo_transporte")
        registros.append(utilidades.fila_a_diccionario(columnas, fila))

    if registros:
       return json.dumps(registros)
    else:
       abort(404, 'No esixte el recurso')



#===============================================================================
# Borramos un registro. 
# curl -i http://localhost:6789/OT/GMIK231 -H "Content-type: application/json" -X DELETE
#===============================================================================
@route('/OT/:ot', method='DELETE') 
def delete_OT(ot):
    utilidades.permitir_CORS()
    try:
       cursor.execute("DELETE FROM ordenes WHERE ot = ?", (ot, ))
       conexion.commit()
       if cursor.rowcount == 0:
          abort(404, 'ERROR al borrar registro')

    except sqlite3.Error as err:
       abort(400, 'ERROR al borrar registro')

    return json.dumps({'status': 200, 'mensaje': 'OK'})



#===============================================================================
# Actualizamos la información del registro 
# curl -i http://localhost:6789/OT/ -H "Content-type: application/json" -X PUT -d '{"ot": "GMIK231", "descripcion": "Reg: 1 modificado", "tipo": "c", "orden": 11, "ultimo_transporte": "2018-01-05T12:28:15.000Z"}'
#===============================================================================
@route('/OT/', method='PUT') 
def put_OT():
    utilidades.permitir_CORS()
    datos_json = request.body.read()
    if not datos_json:
       abort(400, 'NO se recibieron datos')
    else:
       objeto_datos = json.loads(datos_json.decode("utf-8"))
       if not 'ot'      in objeto_datos:
          abort(400, 'NO se especificaron todos los datos')
       else:
           campos      = []
           valores     = []
           campo_clave = 'ot'
           campo_fecha = 'ultimo_transporte'
           for atributo in objeto_datos:
               if atributo != campo_clave:
                   if atributo == campo_fecha:
                       valores.append(datetime.datetime.fromtimestamp(time.mktime(time.strptime(objeto_datos['ultimo_transporte'], "%Y-%m-%dT%H:%M:%S.%fZ"))))
                   else:    
                       valores.append(objeto_datos[atributo])
                   campos.append(atributo + ' = ?')

           if len(campos):
               valores.append(objeto_datos[campo_clave])
               lista_campos = "SET " + ', '.join(campos)    
               SQL = " UPDATE ordenes " + lista_campos + " WHERE ot = ?"
               try:
                   cursor.execute(SQL, tuple(valores))
                   conexion.commit()
                   if cursor.rowcount == 0:
                       abort(400, 'ERROR al actualizar datos')
            
               except sqlite3.Error as err:
                   abort(400, 'ERROR al actualizar datos')
           else:
               abort(400, 'ERROR al actualizar datos')

    return json.dumps({'status': 200, 'mensaje': 'OK'})



#===============================================================================
# Creamos la base de datos y la tabla, si procede.
#===============================================================================
conexion = sqlite3.connect('ordenes.db')
cursor   = conexion.cursor()
SQL      = """
           CREATE TABLE IF NOT EXISTS ordenes (
                  ot                    VARCHAR PRIMARY KEY NOT NULL UNIQUE,
                  descripcion           VARCHAR             NOT NULL,
                  tipo                  VARCHAR             NOT NULL DEFAULT 'custo',
                  orden                 INTEGER             NOT NULL DEFAULT 0,
                  ultimo_transporte     DATETIME            NOT NULL DEFAULT (datetime('now','localtime'))
           )
           """

cursor.execute(SQL)
conexion.commit()



#===============================================================================
# Cerramos las conexiones.
#===============================================================================
def end():
    cursor.close()
    conexion.close()