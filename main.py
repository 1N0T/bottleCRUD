#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from bottle import route, run, request, abort, error, static_file, template, hook
from api import dbOrdenes
from api import dbUsuarios

#===============================================================================
# Definimos el formato de las salidas para las páginas de error.
#===============================================================================
@error(400)
def status_error_400(mensaje_error):
   codigo = 400
   return json.dumps({'status': codigo, 'mensaje': 'KO'})

@error(401)
def status_error_401(mensaje_error):
   codigo = 401
   return json.dumps({'status': codigo, 'mensaje': 'KO, cliente no autorizado'})

@error(404)
def status_error_404(mensaje_error):
   codigo = 404
   return json.dumps({'status': codigo, 'mensaje': 'KO, no existe el registro'})


#===============================================================================
# Mapeamos el contenido estático.
#===============================================================================
@route('/recursos/html/:fichero')
def recursos(fichero):
    return static_file(fichero, root='./recursos/html')

@route('/recursos/js/:fichero')
def recursos(fichero):
    return static_file(fichero, root='./recursos/js')

@route('/recursos/css/:fichero')
def recursos(fichero):
    return static_file(fichero, root='./recursos/css')

@route('/recursos/css/images/:fichero')
def recursos(fichero):
    return static_file(fichero, root='./recursos/css/images')


#===============================================================================
# Iniciamos el servidor web que expone las funciones en todas sus direcciones
# de red.
#===============================================================================
run(reloader=True, debug=True, host="0.0.0.0", port=6789)
dbOrdenes.end()
dbUsuarios.end()