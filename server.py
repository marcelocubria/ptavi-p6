#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read().decode('utf-8')
            datos = line.split(" ")
            if datos[0] == 'INVITE':
                receptor = datos[1].split(':')[1].split('@')[0]
                ip_ua = datos[1].split('@')[1]
                if line == (datos[0] + " sip:" + receptor + "@" + ip_ua + "SIP/2.0"):
                    self.wfile.write(b"llega bien")
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        FICHERO_AUDIO = sys.argv[3]
    except (IndexError, ValueError):
        sys.exit("Usage: python3 server.py IP port audio_file")
    
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', 6001), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
