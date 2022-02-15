# -*- coding: utf-8 -*-
"""
Created on Mon Jul 26 13:02:22 2021

@author: sbana
"""

from tkinter import *                             #GUI
from matplotlib.animation import FuncAnimation    #ANIMACJA WYKRESU 
import matplotlib.pyplot as plt                   #TWORZENIE WYKRESU
import matplotlib.ticker as ticker                #MODYFIKACJA OZNACZEŃ OSI 
import csv                                        #ZAPIS/ODCZYT DANYCH DO PLIKU CSV 
#import pyautogui


# KLASA ODPOWIEDZIALNA ZA STOWRZENIE CHECKLISTY

class ChecklistBox(Frame):
    def __init__(self, parent, choices, **kwargs):
        Frame.__init__(self, parent, **kwargs)

        self.vars = []
        bg = self.cget("background")
        for choice in choices:
            var = StringVar(value=choice)
            self.vars.append(var)
            cb = Checkbutton(self, var=var, text=choice,
                                onvalue=choice, offvalue="",
                                anchor="w", width=20, background=bg,
                                relief="flat", highlightthickness=0
            )
            cb.pack(side="top", fill="x", anchor="w")


    def getCheckedItems(self):
        values = []
        for var in self.vars:
            value =  var.get()
            if value:
                values.append(value)
        return values
    
# def read_moded():
#     filepath = "moded.txt"
#     moded_list = []
#     f = open(filepath,"r")
#     for n in f: 
#         moded_list.append(n)
#     f.close()
#     return moded_list
def read_moded_csv():
    filepath = "moded.CSV"
    moded_list=[]
    with open(filepath) as plik:
        czytnik = csv.reader(plik)
        for row in czytnik :
            moded_list.append(row[0])
    return moded_list
        
    
# FUNKCJA WCZYTUJĄCA DANE Z PLIKU
global num
num = 0 
def animate_list(i,lista, ograniczenie,fig,ax,moded_list):
    global num 
    size = len(lista)
    dane = []
    
    for i in range(size):
        with open (lista[i]+'.CSV') as plik:
            czytnik=csv.reader(plik,delimiter=',')
            temp1=[]
            temp2=[]
            temp3=[]
            temp4=[]
            data=[]
            for row in czytnik:
                if len(row) > 0:
                    data.append(row[0])
                    temp1.append(float(row[1]))
                    temp2.append(float(row[2]))
                    temp3.append(float(row[3]))
#                    if lista[i]=='ASS1':
#                        temp4.append(float(row[3]))
#                    else:
                    temp4.append(float(row[4]))
                        
            # OGRANICZENIE KONTENERA W ZALEŻNOŚCI OD PRZEKAZANEGO ARGUMENTU
            
            if ograniczenie == 0:

                
                data_cut = data[0-ograniczenie:-1]
                temp1_cut = temp1[0:-1]
                temp2_cut = temp2[0-ograniczenie:-1]
                temp3_cut = temp3[0-ograniczenie:-1]
                temp4_cut = temp4[0-ograniczenie:-1]
            else:
                data_cut = data[len(data)-ograniczenie:-1]
                temp1_cut = temp1[len(temp1)-ograniczenie:-1]
                temp2_cut = temp2[len(temp2)-ograniczenie:-1]
                temp3_cut = temp3[len(temp3)-ograniczenie:-1]
                temp4_cut = temp4[len(temp4)-ograniczenie:-1]

                
            dane_temp = [data_cut,temp1_cut,temp2_cut,temp3_cut,temp4_cut]
            dane.append(dane_temp)
            plik.close()
            temp1.clear()
            temp2.clear()
            temp3.clear()
            temp4.clear()
            data.clear()
            
# INICJALIZACJA I USTAWIENIE WYKRESU

    
    fig.suptitle('POMIAR TEMPERATURY')
    if size == 1:

        for i in range(len(ax)):
            ax[i].cla()
            # ax[i].plot(dane[0][0],dane[0][i+1])
            max_dane = max(dane[0][i+1])
            leg = str(max_dane)
            
            ax[i].xaxis.set_major_locator(ticker.AutoLocator())
            ax[i].yaxis.set_major_locator(ticker.AutoLocator())
            if lista[0]=='ASS1':
                names = ['50R1','45R1','40R1','35R1']
            else:
                names = ['R1','R2','R3','R4']
            graph_title =  lista[0] + ' ' + names[i]
            ax[i].set_title(graph_title)
            ax[i].text(dane[0][0][-1],dane[0][i+1][-1],
                       str(dane[0][i+1][-1]))
            ax[i].grid(True)
            if graph_title in moded_list:
                ax[i].plot(dane[0][0],dane[0][i+1],'lime')
                ax[i].legend(['max (MOD)= '+leg])
            else:
                ax[i].plot(dane[0][0],dane[0][i+1])
                
                
                

    else:
        for i in range (0,size):
            for j in range(0,4):
                ax[j][i].cla()
                # ax[j][i].plot(dane[i][0],dane[i][j+1])
                ax[j][i].xaxis.set_major_locator(ticker.AutoLocator())
                ax[j][i].yaxis.set_major_locator(ticker.AutoLocator())
                ax[j][i].grid(True)
                max_dane = max(dane[i][j+1])
                leg = str(max_dane)
                
                ax[j][i].text(dane[i][0][-1],dane[i][j+1][-1],
                              str(dane[i][j+1][-1]))
                
                if lista[i]=='ASS1':
                    names = ['50R1','45R1','40R1','35R1']
                else:
                    names = ['R1','R2','R3','R4']
                graph_title =  lista[i] + ' ' + names[j]
                ax[j][i].set_title(graph_title)
                if graph_title in moded_list:
                    ax[j][i].plot(dane[i][0],dane[i][j+1],'lime')
                    ax[j][i].legend(['max (MOD) = '+leg])
                else:
                    ax[j][i].plot(dane[i][0],dane[i][j+1])
                    ax[j][i].legend(['max  = '+leg])
                

                    
                

                
# USTAWIENIE DOLNYCH OPISÓW OSI POD KĄTEM
    if size>1:        
        for i in range(size):        
            plt.sca(ax[3][i])
            plt.xticks(rotation=45,fontsize='large')
    else:
        plt.sca(ax[3])
        plt.xticks(rotation=45,fontsize='large')
        
    #plt.savefig('/home/pi/Desktop/temp_new/zapis_wykresów/'+str(num)+'.png')
    num=num+1
    #win = pyautogui.getWindows()
    #print(win)

# FUNKCJA ANIMUJĄCA CYKLICZNIE WYKRES 

def show_plot(ograniczenie,lista):
    moded_list = read_moded_csv()
    fig,ax = plt.subplots(4,len(lista),sharex='col',constrained_layout=True)
    ani = FuncAnimation(fig,animate_list,fargs=(lista,ograniczenie,fig,ax,moded_list)
                            ,interval=60000)
    
    plt.show()
      
root = Tk()

czas = IntVar()
lista_linii = ['ASS1','ASS2','ASS10']


# INICJALIZACJA LISTY I PRZYCISKÓW 
checklist = ChecklistBox(root, lista_linii, bd=1, relief="sunken", background="white")

g1 = Radiobutton(root,text='6godz',variable=czas,value=360/2.5)
g2 = Radiobutton(root,text='12godz',variable=czas,value=720/2.5)
g3 = Radiobutton(root,text='24godz',variable=czas,value=1440/2.5)
g4 = Radiobutton(root,text='Wszystkie pomiary',variable=czas,value=0)
g5 = Button(root,text='POKAŻ WYKRES',command=lambda:show_plot(czas.get(),checklist.getCheckedItems()))

# WYWOŁANIE ELEMENTÓW INTERFEJSU 

checklist.pack()
g1.pack()
g2.pack()
g3.pack()
g4.pack()
g5.pack()

root.mainloop()
