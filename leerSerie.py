import serial
import time
from io import open
import keyboard
import csv
import sys
import select
import os


def getTime(tiempoCero):
    return tiempoCero-time.time()


def enviarInformacionSerie(cantidad, puerto='COM3'):
    archivo_temp = []
    tiempo = 0
    arduino = serial.Serial(puerto, 9600)  # se abre el puerto serie
    time.sleep(2)
    arduino.write(b'9')  # empieza la transimision de arduino
    try:  # para chequear si el arduino responde los mensajes
        lectura = arduino.readline().decode('utf-8')
        lectura = lectura[0:-2]
    except:
        lectura = 6
    if lectura != 6:
        print(lectura)
        time.sleep(0.6)
        tiempoCero = time.time()
        for i in range(cantidad):
            try:
                rawString = arduino.readline().decode('utf-8')
            except UnicodeDecodeError:  # Si no se puede decodificar el primer dato por un error de sincronización se saltea
                continue
            tiempo = getTime(tiempoCero)
            rawString = rawString[0:-2]
            print(rawString)  # se elimina el /r/n
            # el dato byte se convierte a string
            archivo_temp.append([tiempo, int(rawString)])
            # tiempo += 0.000392
            # se guarda en un txt
            if keyboard.is_pressed('s'):  # se apreta 's' para salir
                break
        arduino.write(b'8')  # termina la transmision de arduino
        archivo_texto = open("pruebas.csv", "w")  # apertura en modo escritura
        with archivo_texto:  # se escriben los datos leidos en el archivo .csv
            writer = csv.writer(archivo_texto)
            writer.writerow(['Tiempo', 'Valor'])
            for row in archivo_temp:
                writer.writerow(row)
    else:
        print('puerto serie no disponible')
    archivo_texto.close()  # se cierra el archivo
    arduino.close()  # se cierra el puerto serie


enviarInformacionSerie(200, 'COM3')
