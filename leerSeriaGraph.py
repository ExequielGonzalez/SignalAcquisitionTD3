from tkinter import *    # Carga módulo tk (widgets estándar)
from tkinter.ttk import *  # para el comboBox
# from tkinter.ttk import Progressbar
import sys
import glob
import serial
import time
import csv

# TODO: Pedir n cantidad de datos, o setear un tiempo

#!Pedir puertos serie


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


def getTime(tiempoCero):
    return tiempoCero-time.time()


def readQuantity(cantidad, arduino):
    tiempo = 0
    archivo_temp = []
    tiempoCero = time.time()
    for i in range(cantidad):
        try:
            rawString = arduino.readline().decode('utf-8')
        except UnicodeDecodeError:  # Si no se puede decodificar el primer dato por un error de sincronización se saltea
            continue

        tiempo = getTime(tiempoCero)
        rawString = rawString[0:-2]  # se elimina el /r/n
        print(rawString)
        # el dato byte se convierte a string
        archivo_temp.append([tiempo, int(rawString)])
        # tiempo += 0.000392
        # se guarda en un txt
        # bar['value'] = int(i*100/cantidad)
    arduino.write(b'8')  # termina la transmision de arduino
    arduino.close()  # se cierra el puerto serie

    return archivo_temp


def enviarInformacionSerie(puerto, opcion, parametro):
    archivo_temp = []
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
        if opcion == False:
            archivo_temp = readQuantity(parametro, arduino)

        # arduino.write(b'8')  # termina la transmision de arduino
        archivo_texto = open("pruebas.csv", "w")  # apertura en modo escritura
        with archivo_texto:  # se escriben los datos leidos en el archivo .csv
            writer = csv.writer(archivo_texto)
            writer.writerow(['Tiempo', 'Valor'])
            for row in archivo_temp:
                writer.writerow(row)
    else:
        print('puerto serie no disponible')
    archivo_texto.close()  # se cierra el archivo
    # arduino.close()  # se cierra el puerto serie

#!ACA EMPIEZA TKINTER


def btnComenzarClicked():
    # lblPrueba.configure(text="Ha Finalizado!!")
    if(opcionSeleccionada.get() == 1):
        cantidad = txtCantidad.get()
        print(cantidad)
        cantidad = 1 if cantidad == 0 else cantidad
        # enviarInformacionSerie(int(cantidad), 'COM3')
        enviarInformacionSerie(combo.get(), False, int(cantidad))
    if(opcionSeleccionada.get() == 2):
        tiempo = txtDuracion.get()

        print(tiempo)
        tiempo = 1 if tiempo == 0 else tiempo
        enviarInformacionSerie(int(tiempo), combo.get())


def tiempoClicked():
    txtDuracion.config(state='enabled')
    txtCantidad.config(state='disabled')
    print(opcionSeleccionada.get())


def cantidadClicked():
    txtCantidad.config(state='enabled')
    txtDuracion.config(state='disabled')
    print(opcionSeleccionada.get())

    # Define la ventana principal de la aplicación
raiz = Tk()

raiz.geometry('450x160')  # anchura x altura

combo = Combobox(raiz)  # aca deberian mostrarse los puertos COM
try:
    combo['values'] = serial_ports()
    combo.current(0)  # set the selected item

except:
    combo['values'] = ['ERROR', 'Puerto no detectado']


combo.grid(column=0, row=1)

# Asigna un color de fondo a la ventana. Si se omite
# esta línea el fondo será gris

raiz.configure(bg='beige')

# Asigna un título a la ventana

raiz.title('Técnicas Digitales III')

# titulo de la app
lblPrueba = Label(
    raiz, text="Sistema de adquisición de señales", font=("Arial Bold", 20))
lblPrueba.grid(column=0, row=0, columnspan=3)

# Radiobuttons
opcionSeleccionada = IntVar()
rad1 = Radiobutton(raiz, text='Cantidad', value=1,
                   variable=opcionSeleccionada, command=cantidadClicked)
rad2 = Radiobutton(raiz, text='Tiempo', value=2,
                   variable=opcionSeleccionada, command=tiempoClicked)
rad1.grid(column=0, row=2, sticky=W)
rad2.grid(column=0, row=3, sticky=W)


lblCantidad = Label(raiz, text="Cantidad de Lecturas", font=("Arial", 10))
lblCantidad.grid(column=1, row=2)

txtCantidad = Entry(raiz, width=10, state='disabled')
txtCantidad.grid(column=2, row=2)
txtCantidad.focus()

lblDuracion = Label(raiz, text="Duración (segundos)",
                    font=("Arial", 10))
lblDuracion.grid(column=1, row=3)

txtDuracion = Entry(raiz, width=10, state='disabled')
txtDuracion.grid(column=2, row=3)
rad1.invoke()  # Clikea sobre el primer radButton

# txtDuracion.focus()

# bar = Progressbar(raiz, length=200)
# bar['value'] = 0
# bar.grid(column=1, row=3)

btnComenzar = Button(raiz, text='Comenzar', command=btnComenzarClicked)
btnComenzar.grid(column=1, row=4)

# btnSalir = Button(raiz, text='Salir', command=quit, bg="orange")
btnSalir = Button(raiz, text='Salir', command=quit)
btnSalir.grid(column=1, row=5)


raiz.mainloop()
#!ACA TERMINA TKINTER
