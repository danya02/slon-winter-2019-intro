import numpy as np
import matplotlib.pyplot as plt
import requests
import json
import bs4
import threading

class BlackBox:
    def __getitem__(self,item):
        item=round(item,8)
        if item in self.data:return self.data[item]
        return self.get(item)
    def __init__(self):
        self.data={}
        try:
            for i in open('data.txt'):
                self.data.update({float(i.split()[0]):float(i.split()[1])})
        except FileNotFoundError:
            pass
    def save(self):
        a=open('data.txt','w')
        for i in self.data:
            print(i,self.data[i] if self.data[i] is not None else 0,file=a)
        a.close()
    def get(self,value):
        print(f'Hitting blackbox for {value} -> ',end='')
        with requests.post('http://95.85.18.95:8010/blackbox',data={'value':value}) as r:
            v=bs4.BeautifulSoup(r.text).find('input',{'disabled':'disabled'}).get('value')
            try:
                v=float(v)
            except ValueError:
                v=None
        self.data.update({value:v})
        print(v)
        self.save()
bb=BlackBox()

low=-50
high=60
precision=30

arr=[]
dist=np.arange(low,high,precision)
for i in dist:
    arr+=[bb[i]]
arr=np.array(arr)
plt.plot(dist,arr, label='black box')


plt.xlabel('input')
plt.ylabel('output')

plt.title("Black Boxery")

plt.legend()

plt.show()

