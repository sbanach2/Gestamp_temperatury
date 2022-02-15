import requests
import re 
import csv 
import time 
from datetime import datetime 

lines = {'ASS1':('http://172.30.198.129/','/home/pi/Desktop/temp_new/ASS1.CSV'),
         'ASS2':('http://172.30.199.38/','/home/pi/Desktop/temp_new/ASS2.CSV'),
         'ASS10':('http://172.30.199.248/','/home/pi/Desktop/temp_new/ASS10.CSV')
         }
lista_linii = ['ASS1','ASS2','ASS10']


if __name__ == '__main__':
    while True:
        for ASS in lista_linii:
            ip, file = lines[ASS]
            connection = True
            try:
                r = requests.get(ip)
            except:
                print("CONNECTION FAILED")
                connection = False 
                
            if connection:
                plik = open(file,'a')
                czytnik = csv.writer(plik)
                
                now = datetime.now()
                temperatura = re.findall('(\d+.\d+)\s&deg;C', str(r.text))
                temperatura.reverse()
        
                czas = str(now.date()) + "-" + str(now.time().hour) + "-" + str(now.time().minute)
        
                temperatura.append(czas)
                temperatura.reverse()
        
                czytnik.writerow(temperatura)
                print(ASS)
                print(temperatura)
                plik.close()
            else:
                print('Próba połączenia... z'+' '+ASS)
        time.sleep(300)
        
        
