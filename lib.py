#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Funciones auxiliares de la tarea
# Pablo Pizarro, 2015

# Importacion de librerías
try:
    from numpy import NAN
    import numpy as np
except: raise Exception("Se requiere la libreria numpy")
import math
try:
    import matplotlib as mpl
    import matplotlib.pylab as pl
    import matplotlib.pyplot as plt
except: raise Exception("Se requiere la libreria matplotlib")
import sys
import os
import time

# Definicion de constantes
ESCALONES = 30
FACTOR = 0.004
DT = 6
H = 0.3
MAX_ALTURA = 6000
TF = 50
TI = 0

# Funcion que determina si el h ingresado es valido
def isValid(h, escalones):
    d = int(((2450 / escalones) / h) * FACTOR)
    if d > 0: return True
    else: return False

# Funcion que crea una matriz de dimensiones ponderadas por h y un factor dado
def createDimensionArray(h, *dimensiones, **options):
    dim = list(dimensiones)
    for i in range(len(dim)):
        dim[i] = (dim[i] * FACTOR / h)
    if options.get("type") == "int":
        for i in range(len(dim)):
            dim[i] = int(dim[i])
    return dim

# Funcion que crea el coeficiente de relajación de una matriz de dimensiones nxm
def createW(n, m):
    return 4 / (2 + (math.sqrt(4 - (math.cos(math.pi / (n - 1)) + math.cos(math.pi / (m - 1))) ** 2)))

# Funcion que crea un rectangulo desde las posiciones (xi,yi) a (xf,yf) en la matriz
def createRect(matrix, xi, yi, xf, yf, num):
    for i in range(xf - xi):
        for j in range(yf - yi):
            matrix[yi + j][xi + i] = num

# Funcion para imprimir la matriz en un instante de tiempo t
def plot(matrix, t, h, w, **kwargs):

    # Si se define el color de fondo como negro
    if kwargs.get("black"):
        mpl.rcParams['axes.facecolor'] = '000000'

    # Se imprime el grafico
    fig = pl.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(matrix)
    cfg = pl.gcf()
    fig.colorbar(cax)

    # Experimental: se modifican las etiquetas de los ejes
    xnum = len(ax.get_xticks()) - 2
    ynum = len(ax.get_yticks()) - 2
    xlabel = []
    ylabel = []
    for i in range(xnum): xlabel.append(str(int(float(w) * i / (xnum))))
    for j in range(ynum): ylabel.append(str(int(float(h) * j / (ynum - 1))))
    ylabel.reverse()
    if kwargs.get("xlabel"):
        ax.set_xticklabels([''] + xlabel)
        pl.ylabel("Ancho [m]")
    else:ax.set_xticklabels([''])
    if kwargs.get("ylabel"):
        ax.set_yticklabels([''] + ylabel)
        pl.ylabel("Altura [m]")
    else: ax.set_yticklabels([''])

    # Se establece el titulo de la ventana
    pl.title("Temperatura en t=" + str(int(t)) + "\n")
    cfg.canvas.set_window_title("Temperatura en t=" + str(int(t)))
    plt.show()

# Funcion que muestra el gráfico quiver de la matriz
def quiver(matrix, t, h, w, **kwargs):
    mpl.rcParams['axes.facecolor'] = 'ffffff'
    [u, v] = np.gradient(matrix)
    fig = pl.figure()
    ax = fig.add_subplot(111)
    ax.quiver(u, v)
    pl.gca().invert_yaxis()
    cfg = pl.gcf()

    # Experimental: se modifican las etiquetas de los ejes
    xnum = len(ax.get_xticks()) - 2
    ynum = len(ax.get_yticks()) - 2
    xlabel = []
    ylabel = []
    for i in range(xnum): xlabel.append(str(int(float(w) * i / (xnum))))
    for j in range(ynum): ylabel.append(str(int(float(h) * j / (ynum - 1))))
    ylabel.reverse()
    if kwargs.get("xlabel"):
        ax.set_xticklabels([''] + xlabel)
        pl.ylabel("Ancho [m]")
    else:ax.set_xticklabels([''])
    if kwargs.get("ylabel"):
        ax.set_yticklabels([''] + ylabel)
        pl.ylabel("Altura [m]")
    else: ax.set_yticklabels([''])
    pl.title("Quiver en t=" + str(int(t)) + "\n")
    cfg.canvas.set_window_title("Quiver en t=" + str(int(t)))
    plt.show()

# Funcion que retorna el calor dado un cierto instante de tiempo
def temp(t):
    return (-0.005) * (2 ** (math.sqrt(5 - (float(t) / 10))) + math.cos(t))

# Funcion que retorna true si hay un NAN en torno a a[i][j]
def nearNAN(a, i, j):
    if np.isnan(a[i - 1][j]): return True
    if np.isnan(a[i + 1][j]): return True
    if np.isnan(a[i][j - 1]): return True
    if np.isnan(a[i][j + 1]): return True
    return False

# Funcion auxiliar para calcular usando el metodo iterativo
def f(a, i, j, e, time, wrel, width, height, pos_lava, delta):
    if 0 < i < height and 0 < j < width:  # Si no esta en los bordes exteriores de la matriz
        if nearNAN(a, i, j):  # Si es una condicion de borde
            if i == pos_lava[2] and pos_lava[0] <= j <= pos_lava[1]:  # condicion de neumann para la lava
                n = a[i][j] + (1.0 / 4) * (2 * a[i - 1][j] + a[i][j + 1] + a[i][j - 1] - 4 * a[i][j] - 2.0 * (delta ** 2) * temp(time)) * wrel
            else:  # Condiciones de borde de neuman sobre cerro
                if np.isnan(a[i][j + 1]):  # Si el lado derecho es NAN
                    if np.isnan(a[i + 1][j]):  # Si ademas abajo es NAN -> Esquina derecha
                        n = a[i][j] + (1.0 / 4) * (2 * a[i - 1][j] + 2 * a[i][j - 1] - 4 * a[i][j]) * wrel
                    else:  # Borde derecho
                        n = a[i][j] + (1.0 / 4) * (a[i + 1][j] + a[i - 1][j] + 2 * a[i][j - 1] - 4 * a[i][j]) * wrel
                elif np.isnan(a[i + 1][j]):  # Si el lado de abajo es NAN
                    if np.isnan(a[i][j - 1]):  # Si el lado izquierdo es NAN -> Esquina izquierda
                        n = a[i][j] + (1.0 / 4) * (2 * a[i - 1][j] + 2 * a[i][j + 1] - 4 * a[i][j]) * wrel
                    else:  # Borde inferior
                        n = a[i][j] + (1.0 / 4) * (2 * a[i - 1][j] + a[i][j + 1] + a[i][j - 1] - 4 * a[i][j]) * wrel
                elif np.isnan(a[i][j - 1]):
                    n = a[i][j] + (1.0 / 4) * (a[i + 1][j] + a[i - 1][j] + 2 * a[i][j + 1] - 4 * a[i][j]) * wrel
                else: return (a[i][j], 1)
        else:  # Punto interior
            n = a[i][j] + (1.0 / 4) * (a[i + 1][j] + a[i - 1][j] + a[i][j + 1] + a[i][j - 1] - 4 * a[i][j]) * wrel
    else:
        # Esquinas
        if i == 0 and j == 0:  # esquina superior izquierda
            n = a[i][j] + (1.0 / 4) * (2 * a[i + 1][j] + 2 * a[i][j + 1] - 4 * a[i][j]) * wrel
        elif i == 0 and j == width:  # esquina superior derecha
            n = a[i][j] + (1.0 / 4) * (2 * a[i + 1][j] + 2 * a[i][j - 1] - 4 * a[i][j]) * wrel
        elif i == height and j == 0:  # esquina inferior izquierda
            n = a[i][j] + (1.0 / 4) * (2 * a[i - 1][j] + 2 * a[i][j + 1] - 4 * a[i][j]) * wrel
        elif i == height and j == width:  # esquina inferior derecha
            n = a[i][j] + (1.0 / 4) * (2 * a[i - 1][j] + 2 * a[i][j - 1] - 4 * a[i][j]) * wrel
        # Bordes
        else: n = a[i][j]  # Como son dirichlet no se hace nada
    e = abs(a[i, j] - n)
    return (n, e)
