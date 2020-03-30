from tkinter import *    # Carga módulo tk (widgets estándar)
from tkinter.ttk import *  # para el comboBox
import sys
import glob
import serial

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


#!ACA EMPIEZA TKINTER


def btnComenzarClicked():
    lblPrueba.configure(text="Ha comenzado!!")
    cantidad = txtCantidad.get()
    print(cantidad)


# Define la ventana principal de la aplicación
raiz = Tk()

raiz.geometry('400x200')  # anchura x altura

combo = Combobox(raiz)  # aca deberian mostrarse los puertos COM
try:
    combo['values'] = serial_ports()
    combo.current(0)  # set the selected item

except:
    combo['values'] = ['ERROR', 'Puerto no detectado']


combo.grid(column=0, row=0)

# Asigna un color de fondo a la ventana. Si se omite
# esta línea el fondo será gris

raiz.configure(bg='beige')

# Asigna un título a la ventana

raiz.title('Aplicación')

lblPrueba = Label(raiz, text="asdas", font=("Arial Bold", 20))
lblPrueba.grid(column=1, row=0)

opcionSeleccionada = IntVar()
rad1 = Radiobutton(raiz, text='Cantidad', value=1, variable=opcionSeleccionada)
rad2 = Radiobutton(raiz, text='Tiempo', value=2, variable=opcionSeleccionada)
rad1.grid(column=0, row=1)
rad2.grid(column=0, row=2)

print(opcionSeleccionada.get())


lblCantidad = Label(raiz, text="Cantidad de Lecturas", font=("Arial", 10))
lblCantidad.grid(column=1, row=1)

txtCantidad = Entry(raiz, width=10)
txtCantidad.grid(column=2, row=1)
txtCantidad.focus()

btnComenzar = Button(raiz, text='Comenzar', command=btnComenzarClicked)
btnComenzar.grid(column=1, row=2)

# btnSalir = Button(raiz, text='Salir', command=quit, bg="orange")
btnSalir = Button(raiz, text='Salir', command=quit)
btnSalir.grid(column=1, row=3)


raiz.mainloop()
#!ACA TERMINA TKINTER
