#!python3
# -*- coding: utf-8 -*-

from Commande import CommandeRapide, CommandeComplete
from Db import Db
import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)

def main():
    db = Db()
    base = CommandeRapide(ip=getIp(), db=db)
    print("IP : "+str(getIp()))
    base.start()
    print("Analyse rapide terminee. Lancement de l'analyse complete")
    comp = CommandeComplete(ip=getIp(), db=db)
    comp.start()


def getIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ret = s.getsockname()[0]
    s.close()
    return ret

if __name__ == "__main__" : main()
