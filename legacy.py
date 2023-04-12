# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 15:57:08 2022

@author: rafal
"""

import pandas as pd
import numpy as np
from glob import glob
import matplotlib.pyplot as plt
# import tkinter as tk
import os
from tkinter import filedialog
from scipy.signal import find_peaks
from sys import exit
from scipy.optimize import curve_fit
from random import random

plt.close('all')

# scezka dostepu do folderu
directory = filedialog.askdirectory()
print(directory)
print('')

tlo20_dir = directory + '/tło_20s.dat'
tlo40_dir = directory + '/tło_40s.dat'
tlo60_dir = directory + '/tło_60s.dat'
tlo90_dir = directory + '/tło_90s.dat'

# import tła
try:
    tlo20 = pd.read_csv(tlo20_dir, header=None, delimiter='\t', skiprows=1, dtype=float)
    tlo20 = np.array(tlo20)
    tlo = tlo20
except:
    pass

try:
    tlo40 = pd.read_csv(tlo40_dir, header=None, delimiter='\t', skiprows=1, dtype=float)
    tlo40 = np.array(tlo40)
    tlo = tlo40
except:
    pass

try:
    tlo60 = pd.read_csv(tlo60_dir, header=None, delimiter='\t', skiprows=1, dtype=float)
    tlo60 = np.array(tlo60)
    tlo = tlo60
except:
    pass

try:
    tlo90 = pd.read_csv(tlo90_dir, header=None, delimiter='\t', skiprows=1, dtype=float)
    tlo90 = np.array(tlo90)
    tlo = tlo90
except:
    pass

# listy
czasy_integracji = []
zmierzone_moce = []
moce_num = []
widma = []
widma_argumenty = []
n = 0
os.chdir(directory)
nazwy_plikow = glob('*.dat')
nazwa_mezy = set()

# sortowanie plikow wg mocy rosnaco
for i in nazwy_plikow[:]:
    if i[0:3] == 'tło':
        nazwy_plikow.remove(i)


def sort(filename):
    name = filename.replace('.dat', '')
    splitted = name.split('_')
    power = splitted[3]

    if power[-2:] == 'nW':
        power_num = float(power[:-2].replace('p', '.')) * 10 ** (-9)
        return power_num

    elif power[-2:] == 'uW':
        power_num = float(power[:-2].replace('p', '.')) * 10 ** (-6)
        return power_num


nazwy_plikow = sorted(nazwy_plikow, key=sort)

# pętla po folderze z rozszerzeniem .dat
for filename in nazwy_plikow:

    nazwa_pliku = filename

    if nazwa_pliku[0:3] == 'tło':
        continue

    rozdzielone = nazwa_pliku.split('_')

    rozmiar = rozdzielone[0]
    nazwa_mezy.add(rozmiar)
    meza = rozdzielone[1]
    nazwa_mezy.add(meza)
    czas = rozdzielone[2]
    czas_num = float(czas[:-1])
    czasy_integracji.append(czas_num)
    moc = rozdzielone[3].replace('.dat', '')
    zmierzone_moce.append(moc)

    if moc[-2:] == 'nW':
        moc_num = float(moc[:-2].replace('p', '.')) * 10 ** (-9)
        moce_num.append(moc_num)

    elif moc[-2:] == 'uW':
        moc_num = float(moc[:-2].replace('p', '.')) * 10 ** (-6)
        moce_num.append(moc_num)

    dane = pd.read_csv(filename, header=None, delimiter='\t', index_col=False, skiprows=1, dtype=float)

    X = np.array(dane.loc[:, 0])
    Y = np.array(dane.loc[:, 1])

    if czas == '20s':
        Y = Y - tlo20[:, 1]
        Y = Y / 20

    elif czas == '40s':
        Y = Y - tlo40[:, 1]
        Y = Y / 20

    elif czas == '60s':
        Y = Y - tlo60[:, 1]
        Y = Y / 90

    elif czas == '90s':
        Y = Y - tlo90[:, 1]
        Y = Y / 90

    # Y -= sum(Y[3:10])/7
    Y -= Y[-3]

    widma = np.append(widma, Y)
    # widma_argumenty = np.append(widma_argumenty, X)
    n += 1

print(len(Y[3:10]))

# wykres wszystkich widm
widma = np.reshape(widma, (n, len(tlo[:, 1])))
widma = np.transpose(widma)
fig = plt.figure(1)
plt.plot(tlo[:, 0], widma)
plt.legend(zmierzone_moce)
plt.title('{}'.format(nazwa_mezy))
plt.xlabel('Długosc fali [nm]')
plt.ylabel('Intensywnosc [j.w.]')
# plt.show()

wart_find_peaks = widma[:, -5]
arg_find_peaks = tlo[:, 0]

peaks, _ = find_peaks(wart_find_peaks, height=5, threshold=None, distance=None, prominence=2)
plt.plot(arg_find_peaks[peaks], wart_find_peaks[peaks], 'x', markersize=10)

# markery danych
# for xy in zip(arg_find_peaks, arg_find_peaks):                                       # <--
#     plt.annotate('(%s, %s)' % xy, xy=xy, textcoords='data')

plt.show()

# pobranie wartosci pikow
print('')
choose_way = input('Wybierz metodę analizy linii spektralnych: a - automatyczniem, r - ręcznie, e - zakoncz:    ')

if choose_way == 'e':
    exit()

fale_piki = []
nazwy_pikow = []

if choose_way == 'a':
    for wavelength in arg_find_peaks[peaks]:
        fale_piki.append(wavelength)
        wavelength = str(wavelength)
        wl_string = wavelength.replace('.', 'p')
        exec('pik_{} = []'.format(str(wl_string)))
        eval('nazwy_pikow.append(\'pik_{}\')'.format(wl_string))

elif choose_way == 'r':
    while True:
        print('aby zakonczyc nacisnij \'z\'')
        wavelength = input('Podaj długosc fali piku: ')

        if wavelength == 'z':
            break

        fale_piki.append(float(wavelength))
        wl_string = wavelength.replace('.', 'p')
        exec('pik_{} = []'.format(str(wl_string)))
        eval('nazwy_pikow.append(\'pik_{}\')'.format(wl_string))

else:
    exit()

# wyznacznie wartosci intensywnosci dla danej wl
for spectrum_number in range(widma.shape[1]):
    spectrum = widma[:, spectrum_number]

    # for data_point_number in range(len(spectrum)):
    #     if spectrum[data_point_number] <= 0:
    #         spectrum[data_point_number] = 0.01

    for wl in fale_piki:
        wl_string = str(wl).replace('.', 'p')
        eval('pik_{}.append(float(spectrum[np.where(tlo[:,0] == wl)]))'.format(wl_string))


# tworzenie dopasowania linowego do kazdej lini spektralnej
def exponential(x, a, p):
    y = a * x ** p
    return y


fit_bound = 0.7
number_of_good_fits = 0
choosen_wavelengths = []

plik_wybrane_linie = open('linie_dopasowane.txt', 'w')
plik_wybrane_linie.writelines('dlugosc fali ; p ; a ; R^2 ; Energia max ; \n')

for spectrum_line_for_fit in nazwy_pikow:
    intensity_list = eval(spectrum_line_for_fit)

    for value_num in range(len(intensity_list)):
        if intensity_list[value_num] <= 0:
            intensity_list[value_num] = 0.1  # 0.5*intensity_list[value_num+1]

    R2 = 0

    for l in range(len(moce_num) - 2):
        if l < 4:
            continue

        E = moce_num[:l]
        I_list = intensity_list[:l]

        try:
            fit, fiterr = curve_fit(exponential, E, I_list)

            # obliczenia R^2
            residuals = I_list - exponential(E, *fit)
            ss_res = np.sum(residuals ** 2)
            ss_tot = np.sum((I_list - np.mean(I_list)) ** 2)
            r_squared = 1 - (ss_res / ss_tot)

            if r_squared >= fit_bound:
                R2 = r_squared
                a = fit[0]
                p = fit[1]

            # # print('ostania osiągnięta moc: ', '%4.8f' % moce_num[l])
            else:
                break

        except:
            continue
            # print('nie udalo sie wykonac fitu')

    fig2 = plt.figure(3)
    # plt.plot(moce_num, intensity_list, 'o')
    plt.xscale('log')
    plt.yscale('log')

    if R2 >= fit_bound:
        print('Dla dlugosci fali {} dopasowanie R^2 = {}'.format(spectrum_line_for_fit, R2))
        number_of_good_fits += 1
        # plt.plot(E, exponential(E, *fit))
        # plt.plot(moce_num, intensity_list, 'o')
        print(p)

        if p > 0.80 and p < 1.2:
            plik_wybrane_linie.writelines('{} ; {} ; {} ; {} ; {} ; \n'.format(spectrum_line_for_fit, p, a, R2, E[-1]))
            plt.plot(E, exponential(E, *fit))
            plt.plot(moce_num, intensity_list, 'o')
            choosen_wavelengths.append(spectrum_line_for_fit + '_fit')
            choosen_wavelengths.append(spectrum_line_for_fit)

        elif p > 1.8 and p < 2.2:
            plik_wybrane_linie.writelines('{} ; {} ; {} ; {} ; {} ; \n'.format(spectrum_line_for_fit, p, a, R2, E[-1]))
            plt.plot(E, exponential(E, *fit))
            plt.plot(moce_num, intensity_list, 'o')
            choosen_wavelengths.append(spectrum_line_for_fit + '_fit')
            choosen_wavelengths.append(spectrum_line_for_fit)

plt.legend(choosen_wavelengths)
plt.show()
plik_wybrane_linie.close()
print(number_of_good_fits)

# Generacja funkcji liniowej i kwadratowej
# def ekscyton(g, tx, txx):
#     return g/(1 + g*tx + g**2*tx*txx)

# def biekscyton(g, tx, txx):
#     return (g**2*tx)/(1 + g*tx + g**2*tx*txx)

# tx = 10**(-10)
# txx = 10**(-10)

# ekscyton_od_mocy = ekscyton(np.array(moce_num), tx, txx)
# biekscyton_od_mocy = biekscyton(np.array(moce_num), tx, txx)

# Wykres intensywnosci z mocą i zapis do pliku txt

# plt.figure(2)
# plt.plot(moce_num, ekscyton_od_mocy)
# plt.plot(moce_num, biekscyton_od_mocy)

do_pliku = np.array(moce_num)

for i in nazwy_pikow:
    do_pliku = np.append(do_pliku, eval(i))

    plt.figure(2)
    plt.plot(moce_num, eval(i), 'o')

legenda = nazwy_pikow.copy()
# legenda.insert(0, 'ekscyton')
# legenda.insert(1, 'biekscyton')

plt.xscale('log')
plt.yscale('log')
plt.legend(legenda)
plt.title(nazwa_mezy)
plt.xlabel('moc pobudzania [W]')
plt.ylabel('Intensywnosc [j.w.]')
plt.show()

nazwy_pikow.insert(0, 'Moc')
do_pliku = np.reshape(do_pliku, (len(nazwy_pikow), len(moce_num)))
do_pliku = np.transpose(do_pliku)
do_pliku = np.absolute(do_pliku)

# Do Pandas
do_pliku_df = pd.DataFrame(do_pliku, columns=[nazwy_pikow])

do_pliku_df.to_csv('linie_wybrane.txt', sep=';', mode='w')