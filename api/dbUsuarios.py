#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime
import subprocess
import sqlite3
import json

from bottle import route, run, response, request, abort, error, static_file, template
from utils import utilidades

@route('/user/login', method='OPTIONS') 
def enable_CORS_USR():
    utilidades.permitir_CORS()
    return json.dumps({'status': 200, 'mensaje': 'OK'})
@route('/user/info', method='OPTIONS') 
def enable_CORS_USR():
    utilidades.permitir_CORS()
    return json.dumps({'status': 200, 'mensaje': 'OK'})
@route('/user/logout', method='OPTIONS') 
def enable_CORS_USR():
    utilidades.permitir_CORS()
    return json.dumps({'status': 200, 'mensaje': 'OK'})



#===============================================================================
# Aquí controlaríamos el inicio de sessión del usuario. De momento devolvemos
# información estática para la aplicación de ejemplo.
#===============================================================================
@route('/user/login', method='POST')
def post_user_login():
    utilidades.permitir_CORS()
    return json.dumps({'code':20000,'data':{'token':'admin'}})



#===============================================================================
# Aquí controlamos el cierre de sesión del usuario. De momento, devolvemos
# información estática para la aplicación de ejemplo.
#===============================================================================
@route('/user/logout', method='POST')
def post_user_logout():
    utilidades.permitir_CORS()
    return json.dumps({'code':20000,'data':{'token':'admin'}})



#===============================================================================
# Consulta de todos los roles
# curl -i http://localhost:6789/OT/ -H "Content-type: application/json" -X GET
#===============================================================================
@route('/user/info', method='GET')
def get_user_roles():
    utilidades.permitir_CORS()
    registros = []

    for fila in cursor.execute("SELECT rol FROM roles WHERE usuario = ?", (request.query.token, )):
        registros.append(fila[0])

    if registros:
       return json.dumps({"code":20000, "data":{"name": request.query.token, "avatar": "", "role": registros}})
    else:
       abort(404, 'No esixte el recurso')



#===============================================================================
# Creamos la base de datos y la tabla, si procede.
#===============================================================================
conexion = sqlite3.connect('ordenes.db')
cursor   = conexion.cursor()
SQL      = """
           CREATE TABLE IF NOT EXISTS roles (
                  usuario  VARCHAR NOT NULL,
                  rol      VARCHAR NOT NULL,
                  PRIMARY KEY(usuario, rol)
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