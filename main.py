#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Archivo principal de la tarea
# Pablo Pizarro, 2015

# Importación de librerías
from lib import *

# Funcion principal
def run(h=H, escalones=ESCALONES, max_altura=MAX_ALTURA, ti=TI, tf=TF, dt=DT):

    # Variables del problema
    epsilon = 0.001
    max_iteraciones = 10000
    t_array = np.linspace(ti, tf, dt)
    t_array = [0, 10, 20, 30, 40, 49]

    # Se comprueba que se las variables sean correctas
    if isValid(h, escalones):

        # Se establecen variables
        vartemp = -(0.0065 * h / FACTOR)
        dimensiones = createDimensionArray(h, 2000, 2450, 4900, max_altura - 2450, 2450 / escalones, 400, type="int")  # [entorno, altura, ancho, cielo, escalon, base]
        n = dimensiones[1] + dimensiones[3]  # altura
        m = 2 * dimensiones[0] + dimensiones[2]  # anchura
        w = createW(n, m)  # parametro de relajación
        pos_lava = [dimensiones[0] + (dimensiones[2] / (2 * escalones)) * (escalones - 1), m - (dimensiones[0] + (dimensiones[2] / (2 * escalones)) * (escalones - 1)), n - escalones * dimensiones[4]]
        xaxis = range(m)
        yaxis = range(n)
        xaxis_rev = range(m)
        yaxis_rev = range(n)
        xaxis_rev.reverse()
        yaxis_rev.reverse()
        print "Matriz de dimensiones: {1}x{0}, w calculado: {2}. Para cancelar pulse Ctrl-C".format(n+ dimensiones[5], m, round(w,3))

        # Se crea la matriz
        a = np.ones((n + dimensiones[5], m))

        # Se recorre la matriz de tiempo
        for t in t_array:

            # Se inicializa la temperatura de la atmósfera
            for h in range(n + 1):
                createRect(a, 0, n - h, m, n - h + 1, 15 + vartemp * h)

            # Se dibuja la montana, para ello se escriben rectangulos de dimensiones dadas
            createRect(a, 0, n + 1, m, n + dimensiones[5], NAN)  # suelo
            for i in range(escalones):  # escalones
                dx = (dimensiones[2] / (2 * escalones)) * i
                createRect(a, dimensiones[0] + dx, n - (i + 1) * dimensiones[4] + 1, m - dimensiones[0] - dx, n - i * dimensiones[4] + 1, NAN)

            # Se ejecuta el metodo iterativo
            e = 0  # error
            e0 = 0  # error inicial
            ni = 0  # numero de iteraciones
            t0 = time.time()  # tiempo inicial de ejecucion
            print "Main :: Ejecutando metodo iterativo para t = " + str(int(t))
            while ni <= max_iteraciones:
                for j in xaxis:
                    for i in yaxis:
                        (a[i][j], e) = f(a, i, j, e, t, w, m - 1, n - 1, pos_lava, h)
                if e < epsilon: break
                if e0 == 0: e0 = e
                sys.stdout.write("\r        " + str(int((e0 - e) * 100.0 / (e0 - epsilon))) + "% completado")
                sys.stdout.flush()
                ni += 1  # numero de iteraciones
            tf = int(time.time() - t0)
            if (tf / 60) > 0: sys.stdout.write("\r       100% completado en " + str(tf / 60) + " minutos y " + str(tf % 60) + " segundos")
            else: sys.stdout.write("\r       100% completado en " + str(tf % 60) + " segundos")
            sys.stdout.flush()

            # Se imprime la matriz en pantalla
            try:
                print "\nMain :: Imprimiendo grafico 2D"
                plot(a, int(t), max_altura, 8900, black=True, ylabel=True)
                print "Main :: Imprimiendo grafico Quiver"
                quiver(a, int(t), max_altura, 8900, ylabel=True)
            except: pass

        try: os.system("taskkill /PID " + str(os.getpid()) + " /F")
        except: pass
    else:
        print "Error :: El numero de escalones definido ({0}) no permite el h ({1}) actual".format(escalones, h)

if __name__ == "__main__":
    run()
