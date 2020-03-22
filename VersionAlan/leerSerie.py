import serial
import time
from io import open
import csv
import sys
import select
import os

# escritura(si no existe lo crea)
archivo_texto = open("prueba.csv", "w")  # apertura en modo escritura
archivo_temp = []
tiempo = 0
arduino = serial.Serial('COM3', 9600)  # se abre el puerto serie
time.sleep(1)
while True:
    try:
        rawString = arduino.readline().decode('utf-8')
    except UnicodeDecodeError:  # Si no se puede decodificar el primer dato por un error de sincronización se saltea
        continue
    rawString = rawString[0:-2]  # se elimina el /r/n
    print(rawString)  # se muestra el valor leido por pantalla
    # el dato byte se convierte a string y se almacena temporalmente
    archivo_temp.append([tiempo, int(rawString)])
    tiempo += 0.000392
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        break
    # if keyboard.is_pressed('s'):  # se apreta 's' para salir
    #     break

with archivo_texto:  # se escriben los datos leidos en el archivo .csv
    writer = csv.writer(archivo_texto)
    writer.writerow(['Tiempo', 'Valor'])
    for row in archivo_temp:
        writer.writerow(row)
archivo_texto.close()  # se cierra el archivo

arduino.close()  # se cierra el puerto serie
