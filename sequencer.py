#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

#### COMMENTS
#
# Lines with #dev are just for troubleshooting
#
# #### CAPITAL LETTERS : part title
# #CAPITAL : project
#
# I've tried to make the variables as simple as possible.
# The idea is reading through the peaks for the next amino acid by
# mass of peptide + m/z of next AA. Reads the multiple possible peaks and stores
# in multi_peaks, and the AAs in multi_AA. Then pick the first one and sequence.
# If at the end, mass!=mol, try again with second peak of the last multi found.
# If last multi doesn't give anything go to previous and so the same.
#
# Exemple :
# Find R/K as Y1 ion
# 147,204,218,234,261,275,289,291,305
# $K===================!                 BAD    mass!=mol
# $K===========================!         BAD    mass!=mol
# $K==================================$  GOOD   mass==mol

from timeit import default_timer as timer

MW_AA = {57:'G',71:'A',87:'S',97:'P',99:'V',101:'T',103:'C',
         113:'I/L',114:'N', 115:'D',128:'K/Q',129:'E',131:'M',137:'H',
         147:'F',156:'R',161:'AcC',163:'Y',186:'W'}
AA_MW = {'G':57,'A':71,'S':87,'P':97,'V':99,'T':101,'C':103,
         'I/L':113,'N':114,'D':115,'K':128,'K/Q':128,'E':129,'M':131,
         'H':137,'F':147,'R':156,'AcC':161,'Y':163,'W':186}

####    INPUT PEAKS

# PROJECT : OCR with Tesseract from Google and pyOCR to bind it.
# I found : https://pythontips.com/2016/02/25/ocr-on-pdf-files-using-python/

peaks_list=[]
while peaks_list==[]:
    in_mode=input('Input type : .txt file (F) or manual (M)?')
# file input
    if in_mode=='F':
        filename=input('What is the name of your file ? ')#get name of file
        filename=filename+'.txt'
        with open(filename, "rt", encoding='utf-8') as peaks_file:#open file copy text
            for line in peaks_file:
                for peak in line:
                    peaks_list.append(peak)
        peaks_file.close()
    elif in_mode=='M':
#manual input
        peaks_input = input('Write your MS/MS peaks values separated by a space :\n')
        peaks_list = list(map(int, peaks_input.split(' ')))
    elif in_mode!=='F' and in_mode=='M':
        print('Please enter F for .txt file or M for manual.')
    pass

# List of peaks useful for troubleshooting, first list is made of actual results,
# second list needs update to work with the new verif step.

'''peaks_list=[101, 129, 147, 202, 230, 260, 273, 301, 342, 373, 386, 414,
            485,495, 502, 513, 601, 624, 642, 656, 714, 727, 755, 785,
            801, 840, 868, 886, 1014]
mol=1014'''

'''peaks_list=[147,204,218,234,261,275,289,291,305]
mol=305'''

####    INPUT MOLECULAR ION M/Z
mol=int(input('\nWrite the m/z of the molecular ion :\n'))

####    START
start = timer()
if mol not in peaks_list:
    peaks_list.append(mol)
peaks_list.append(1)#for the H+ on the first b ion
peaks_list.sort()
#peaks_list_original=peaks_list #not used yet

####    CONFIRM TO USER
print ('\nYour values are : ',', '.join(map(str,peaks_list)),
       '.\n\nm/z(molecular ion) = ',mol,'\n')

####    INITIATION OF SEQUENCING Y1 = K or R,
mol_b=mol-18 #mol-18 for calculating b ions
if 147 in peaks_list and (mol_b-128) in peaks_list:
    print('Y1=K')#dev
    seq=['K']
    mass_y=147
    mass_y_list=[mass_y]
    mass_b=mol_b-128
    mass_b_list=[mass_b]
elif 175 in peaks_list and (mol_b-156) in peaks_list:
    print('Y1=R')#dev
    seq=['R']
    mass_y=175
    mass_y_list=[mass_y]
    mass_b=mol_b-128
    mass_b_list=[mass_b]
else: print ('restart1')#dev

####    SEQUENCING
list_multi=[]
while mass_y!=mol and mass_b!=1:
    print('mass_y :',mass_y,'mass_b :',mass_b)#dev
    multi_peaks_y=[]
    multi_peaks_b=[]
    multi_AA=[]
    print(len(multi_AA))
    for x in sorted(MW_AA.keys()):
        #print('mass+x :',mass+x,'// x :',x)#dev
        if mass_y+x in peaks_list and mass_b-x in peaks_list:
            #print()
            multi_peaks_y.append(mass_y+x)
            multi_AA.append(MW_AA[x])
            multi_peaks_b.append(mass_b-x)
            #safety=0
        else:
            #safety=safety + 1
            continue
        continue
    print('peaks_y :',multi_peaks_y, '\npeaks_b :',multi_peaks_b,'\nAAs   :',multi_AA)#dev
    list_multi.append((mass_y, list(multi_peaks_y), list(multi_peaks_b), list(multi_AA)))
    if len(multi_peaks_y)==0 and len(multi_peaks_b)==0:
        print('failed')#dev
        break   #Get the next peak from the last multi.
                #i.e. 275 and make it mass, restart sequencing
# NEXT : When last multi doesn't work, use previous.
    elif len(multi_peaks_y)==1 and len(multi_peaks_b)==1:
        mass_y=multi_peaks_y[0]
        mass_b=multi_peaks_b[0]
        seq.append(multi_AA[0])
        print('seq : ',seq)#dev
        continue
    else:
        mass_y=multi_peaks[0]
        mass_b=multi_peaks_b[0]
        seq.append(multi_AA[0])
        print('seq : ',seq)#dev
        continue
    break

####    CALCULATING M/Z OF IONS
for n in range(len(seq)-1):
    mass_y_list.append(mass_y_list[n]+AA_MW[seq[n+1]])
    mass_b_list.append(mass_b_list[n]-AA_MW[seq[n+1]])
    #if mass_y_list[n] in peaks_list:
    peaks_list.remove(mass_y_list[n])
    #if  mass_b_list[n] in peaks_list:
    peaks_list.remove(mass_b_list[n])
print('peaks left :',peaks_list)
mass_a_list=[]
for n in range(len(seq)-1):
    mass_a_list.append('')
    if mass_b_list[n]-28 in peaks_list:
        mass_a_list[n]=mass_b_list[n]-28
    if  mass_a_list[n]!='':
        peaks_list.remove(mass_a_list[n])
print('final peaks :',peaks_list)

print('m y :',mass_y_list,'\nm b :',mass_b_list,'\nm a :',mass_a_list)#dev


####    OUTPUT
print('list_multi : ',list_multi)#dev
print('\nThe sequence is',len(seq),'residues long.')

####    END
#Timing is the coolest thing !
end=timer()
print ('\nDone in {0} secs.'.format(end-start))
