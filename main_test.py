#!/usr/bin/env python
#-*- coding: utf-8 -*-

import datetime
import RPi.GPIO as GPIO
import time
#import audio
import os
import pygame.mixer
import pandas as pd
import numpy as np

GPIO.setmode(GPIO.BCM)
buttonPin = 17
buttonPin2 = 27

GPIO.setup(buttonPin,GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(buttonPin2,GPIO.IN, pull_up_down = GPIO.PUD_UP)

#Se tiene que inicializar el modilo de pygames.mixer de esta manera
pygame.mixer.init(44100, -16, 2, 2048)
#Despues ya se puede guardar los sonidos

def cancion(filename):
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play(1)#Para que se reproduzca c1 vez
    global vector
    #global max_count
    if filename == "tamborine_100bpm.mp3" or "cumbia_corta.mp3":
        span = 0.6
        vector = np.arange(0,35,.6)#cantidad de beats por segundo de 100BPM
    #    max_count = 50
    elif filename == "tamborine_50bpm.mp3":
        span = 1.2
        vector = np.arange(0,35,1.2)# 50 BPM
    #    max_count = 25
    elif filename =="tamborine_170bpm.mp3":
        span = 0.353
        vector = np.arange(0,35,.353)# 160 BPM
    #    max_count = 85
    global timesaveMano
    global timesavePie
    global new_vector
    timesaveMano = []
    timesavePie = []
    t0 = time.time()
    new_vector = []
    counter = 0
    while True:
        cronometro = time.time() - t0
        if cronometro > (counter * span):
            counter += 1
        if cronometro > 30.1:
            pygame.mixer.music.stop()
            break
        input_value = GPIO.input(17)
        input_value2 = GPIO.input(27)
        if not input_value:
            tiempo = round(time.time() - t0,4)
            print tiempo
            timesaveMano.append(tiempo)
            timesavePie.append(None)
            new_vector.append(round(vector[counter-1],2))
            while not input_value:
                input_value = GPIO.input(17)
                time.sleep(0.01)
        if not input_value2:
            tiempo2 = round(time.time() - t0,4)
            print tiempo2
            timesavePie.append(tiempo2)
            timesaveMano.append(None)
            new_vector.append(round(vector[counter - 1],2))
            while not input_value2:
                input_value2 = GPIO.input(27)
                time.sleep(0.01)
    data = pd.DataFrame({'beats': new_vector,'input_1':timesaveMano,'input_2':timesavePie})
    return data

msj = "BIENVENIDO A LA PRUEBA DE SINCRONIZACION MUSICAL. \n A continuación completa los siguientes datos personales:"
print msj
name = raw_input("- ¿Cuál es tu nombre? ")
sex = raw_input("- ¿Cuál es tu sexo? ")
edad = raw_input("- ¿Cuál es tu edad? ")
test = raw_input("- ¿Qué 'test' deseas realizar? \n 1) Dedo índice \n 2) Aplauso \n 3) Marcha \n" )
prueba = raw_input("- ¿Qué prueba quieres realizar?\n 1) 100 BPM \n 2) 50 BPM \n 3) 170 BPM \n 4) Canción 'Baila esta cumbia - Selena y KKs' \n")

if test == '1':
    song_test = "dedo"
elif test == '2':
    song_test = "aplauso"
elif test == '3':
    song_test = "marcha"

if prueba == '1':
    song_file = "tamborine_100bpm.mp3"
    file_prueba = "100BPM"
elif prueba == '2':
    song_file = "tamborine_50bpm.mp3"
    file_prueba = "50BPM"
elif prueba == '3':
    song_file = "tamborine_170bpm.mp3"
    file_prueba = "170BPM"
elif prueba == '4':
    song_file = "cumbia_corta.mp3"
    file_prueba = "100BPM_baila_esta_cumbia"

msj2 = "La prueba inicia en: "
print msj2
os.system('say ' + repr(msj2))

for i in range(3,0,-1):
    time.sleep(1)
    print i

time.sleep(1)
print "Ahora"

data = cancion(song_file)
hoy = time.strftime("%b-%d-%Y %H:%M:%S") #Imprime hora actual
today = time.strftime('%Y%m%d-%H%M%S')
filename = file_prueba +'_'+name.lower().replace(" ","_")+today+'_'+song_test+'.txt'
with open(filename,'a') as f:
    f.write('fecha: '+ hoy + '\n'+ 'nombre: '+name + '\n'+'edad: ' + edad + '\n' +'sexo: '+ sex +'\n' +'ejercicio: ' +song_test + '\n' + 'velocidad: '+file_prueba +'\n')
    data.to_csv(f, header = True, index = True, sep = '\t')

os.system('say "Prueba finalizada" '+ repr(name) + ". Hasta pronto.")
