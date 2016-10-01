#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Interfaz gr�fica para la tarea
# Pablo Pizarro, 2015

# Importacion de librerias
try: from Tkinter import *
except: raise Exception("Se requiere la libreria Tkinter")
try: import tkMessageBox
except: raise Exception("Se requiere la libreria tkMessageBox")
from lib import *
import main

# Definicion de constantes
DEFAULT_FONT_TITLE = "Arial", 11
WINDOW_SIZE = [240, 240]

# Clase principal
class Gui:

    def __init__(self):  # Constructor
        self.root = Tk()

        # Configuracion de la ventana
        self.root.focus_force()
        self.root.geometry('%dx%d+%d+%d' % (WINDOW_SIZE[0], WINDOW_SIZE[1], (self.root.winfo_screenwidth() - WINDOW_SIZE[0]) / 2, \
                                                 (self.root.winfo_screenheight() - WINDOW_SIZE[1]) / 2))
        self.root.title("GUI - T1")
        try: self.root.iconbitmap("res/icon.ico")
        except: pass
        self.root.minsize(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.root.resizable(False, False)

        # Eventos
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        self.root.bind("<Escape>", self.exit)

        # Se agreegan los botones
        f = Frame(self.root)
        f.pack(padx=10, pady=10)
        f1 = Frame(f)
        f1.pack(pady=4)
        Label(f1, text="Discretizacion H", anchor=E, width=14).pack(side=LEFT)
        self.entry_h = Entry(f1, relief=GROOVE, width=14)
        self.entry_h.pack(padx=10)
        self.entry_h.insert(0, str(H))
        f6 = Frame(f)
        f6.pack(pady=4)
        Label(f6, text="Division temporal", anchor=E, width=14).pack(side=LEFT)
        self.entry_dt = Entry(f6, relief=GROOVE, width=14)
        self.entry_dt.pack(padx=10)
        self.entry_dt.insert(0, str(DT))
        f4 = Frame(f)
        f4.pack(pady=4)
        Label(f4, text="Escalones", anchor=E, width=14).pack(side=LEFT)
        self.entry_escalones = Entry(f4, relief=GROOVE, width=14)
        self.entry_escalones.insert(0, str(ESCALONES))
        self.entry_escalones.pack(padx=10)
        f5 = Frame(f)
        f5.pack(pady=4)
        Label(f5, text="Maxima altura", anchor=E, width=14).pack(side=LEFT)
        self.entry_maxaltura = Entry(f5, relief=GROOVE, width=14)
        self.entry_maxaltura.insert(0, str(MAX_ALTURA))
        self.entry_maxaltura.pack(padx=10)
        f2 = Frame(f)
        f2.pack(pady=4)
        Label(f2, text="Tiempo inicial ti", anchor=E, width=14).pack(side=LEFT)
        self.entry_ti = Entry(f2, relief=GROOVE, width=14)
        self.entry_ti.insert(0, str(TI))
        self.entry_ti.pack(padx=10)
        f3 = Frame(f)
        f3.pack(pady=4)
        Label(f3, text="Tiempo final tf", anchor=E, width=14).pack(side=LEFT)
        self.entry_tf = Entry(f3, relief=GROOVE, width=14)
        self.entry_tf.insert(0, str(TF))
        self.entry_tf.pack(padx=10)
        fbt = Frame(f)
        fbt.pack(pady=10)
        Button(f, text="Correr", width=10, relief=GROOVE, command=self.run, font=DEFAULT_FONT_TITLE).pack(side=LEFT, padx=5)
        Button(f, text="Cerrar", width=10, relief=GROOVE, command=self.exit, font=DEFAULT_FONT_TITLE).pack()

    def run(self, event=None):  # Funcion que corre la aplicacion
        # Se obtienen los datos
        a = self.entry_maxaltura.get()
        dt = self.entry_dt.get()
        e = self.entry_escalones.get()
        h = self.entry_h.get()
        tf = self.entry_tf.get()
        ti = self.entry_ti.get()

        # Se comprueba que los datos esten ingresados de forma correcta
        try: h = float(h)
        except: tkMessageBox.showerror("Error", "La discretizacion no es correcta, debe ser un numero"); return
        if e.isdigit(): e = int(e)
        else: tkMessageBox.showerror("Error", "El numero de escalones no es correcto, debe ser un numero"); return
        if isValid(h, e):  # Si h y e son validos
            if a.isdigit():
                a = int(a)
                if a >= 2450:
                    if ti.isdigit():
                        ti = int(ti)
                        if ti >= 0:
                            if tf.isdigit():
                                tf = int(tf)
                                if tf > 0 and tf > ti:
                                    if tf <= 50:
                                        if dt.isdigit():
                                            dt = int(dt)
                                            if dt >= 1:
                                                self.exit()
                                                main.run(h, e, a, ti, tf, dt)
                                            else: tkMessageBox.showerror("Error", "La division temporal debe ser mayor o igual a uno"); return
                                        else: tkMessageBox.showerror("Error", "La division temporal debe ser un digito"); return
                                    else: tkMessageBox.showerror("Error", "El tiempo final no puede ser mayor que 50"); return
                                else: tkMessageBox.showerror("Error", "El tiempo final debe ser mayor al tiempo inicial"); return
                            else: tkMessageBox.showerror("Error", "El tiempo final es incorrecto, debe ser un numero"); return
                        else: tkMessageBox.showerror("Error", "El tiempo inicial debe ser mayor a cero"); return
                    else: tkMessageBox.showerror("Error", "El tiempo inicial es incorrecto, debe ser un numero"); return
                else: tkMessageBox.showerror("Error", "La altura minima es de 2450m"); return
            else: tkMessageBox.showerror("Error", "La altura no es correcta, debe ser un numero"); return
        else: tkMessageBox.showerror("Error", "El numero de escalones definido no permite el h actual"); return

    def launch(self):  # Lanza la aplicacion
        self.root.mainloop(0)

    def exit(self, event=None):  # Termina la aplicacion
        self.root.destroy()

if __name__ == "__main__":
    window = Gui()
    window.launch()
