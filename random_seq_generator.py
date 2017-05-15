#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import random

dict1 = {57:'G',71:'A',87:'S',97:'P',99:'V',101:'T',103:'C',113:'I/L',114:'N',115:'D',128:'K/Q',129:'E',131:'M',137:'H',147:'F',156:'R',161:'AcC',163:'Y',186:'W'}
dict2 = {'G':57,'A':71,'S':87,'P':97,'V':99,'T':101,'C':103,'I/L':113,'N':114,'D':115,'K':128,'K/Q':128,'E':129,'M':131,'H':137,'F':147,'R':156,'AcC':161,'Y':163,'W':186}
seq=[]
my=[]
mb=[]

length=input('length : ')

#create pseudo-random sequence
for i in range(int(length)-1):
    seq.append(random.choice(list(dict2.keys())))
    #print(random.choice(list(dict2.keys())))
#add pseudo random C-term
x=random.randrange(0,2,1)
print(x)
if x==1:
    seq.append('K')
    my.append(147)
else:
    seq.append('R')
    my.append(175)
print(seq)

#append m/z values for sequence in y ions
for i in range(len(seq)):
    n=-i-1
    if i==0:
        #print(seq[n], my[i],'      ',seq[i],dict2[seq[i]]+1)
        mb.append(dict2[seq[i]]+1)
    if i>0:
        #print(seq[n],my[i-1],dict2[seq[n]],my[i-1]+dict2[seq[n]],seq[i],mb[i-1],dict2[seq[i]],mb[i-1]+dict2[seq[i]])
        my.append(my[i-1]+dict2[seq[n]])
        mb.append(mb[i-1]+dict2[seq[i]])

mb.remove(mb[-1])

m=sorted(my+mb)
print(' '.join([str(m[i]) for i in range(len(m))]))
