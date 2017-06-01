# coding: utf-8
"""
This script runs the application using a development server.
"""

import bottle
import os
import sys

# routes contains the HTTP handlers for our server and must be imported.
import routes
import socket;

if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    bottle.debug(True)

def wsgi_app():
    """Returns the application to make available through wfastcgi. This is used
    when the site is published to Microsoft Azure."""
    return bottle.default_app()

if __name__ == '__main__':
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    # PORT de lancement du serveur
    ADRESS = '127.0.0.1'
    PORT = 1854
    sock = socket.socket()
    try:
        sock.bind((ADRESS,PORT))
        if PORT == sock.getsockname()[1]:
            print "The PORT %s for the address %s is not in use: %s" % (PORT,ADRESS, e)
        else:
            print "The PORT %s for the address %s is already in use: %s" % (PORT,ADRESS, e)
            raise ValueError('[ERROR]: SERVER PORT ALREADY IN USE !')
    except socket.error, e:
        print "Binding to %s on port %s failed: %s" % (ADRESS, PORT, e)
        raise ValueError('[ERROR]: SERVER BIND IMPOSSIBLE !')
    finally:
        sock.close()

    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        """Handler for static files, used with the development server.
        When running under a production server such as IIS or Apache,
        the server should be configured to serve the static files."""
        return bottle.static_file(filepath, root=STATIC_ROOT)

    # Starts a local test server.
    bottle.run(reloader = True, server = 'wsgiref', host = HOST, port = PORT)
