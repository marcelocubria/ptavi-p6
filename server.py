#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read().decode('utf-8')
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break
            datos = line.split(" ")
            if datos[0] == 'INVITE':
                print("Llega " + line)
                receptor = datos[1].split(':')[1].split('@')[0]
                ip_ua = datos[1].split('@')[1]
                if line[:-4] == (datos[0] + " sip:" + receptor + "@" + ip_ua +
                                 " SIP/2.0"):
                    respuesta_invite = "SIP/2.0 100 Trying\r\n\r\n"
                    respuesta_invite += "SIP/2.0 180 Ringing\r\n\r\n"
                    respuesta_invite += "SIP/2.0 200 OK\r\n\r\n"
                    self.wfile.write(bytes(respuesta_invite, 'utf-8'))
                else:
                    self.wfile.write(b"SIP/2.0 400 Bad request\r\n\r\n")
            elif datos[0] == 'ACK':
                print("llega " + line)
                aEjecutar = ('mp32rtp -i 127.0.0.1 -p 23032 < ' + FICH_AUDIO)
                print("ejecutando " + aEjecutar)
                os.system(aEjecutar)
            elif datos[0] == 'BYE':
                print("llega " + line)
                receptor = datos[1].split(':')[1].split('@')[0]
                ip_ua = datos[1].split('@')[1]
                if line[:-4] == (datos[0] + " sip:" + receptor + "@" + ip_ua +
                                 " SIP/2.0"):
                    self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
                else:
                    self.wfile.write(b"SIP/2.0 400 Bad request\r\n\r\n")
            else:
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed")


if __name__ == "__main__":
    try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        FICH_AUDIO = sys.argv[3]
    except (IndexError, ValueError):
        sys.exit("Usage: python3 server.py IP port audio_file")

    serv = socketserver.UDPServer((IP, PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
