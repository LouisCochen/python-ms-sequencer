#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

#### COMMENTS
#
# Lines with #dev are just for troubleshooting
#
# #### CAPITAL LETTERS : part title
# #CAPITAL : project/idea/read the first word
#
# I've tried to make the variables as simple as possible.
# The idea is reading through the peaks for the next amino acid by
# mass of peptide + m/z of next AA. Reads the multiple possible peaks and stores
# in readings, and the AAs in multi_AA. Then pick the first one and sequence.
# If at the end, mass!=mol, try again with second peak of the last multi found.
# If last multi doesn't give anything go to previous and so the same.
#
# Exemple :
# Find R/K as Y1 ion
# 147,204,218,234,261,275,289,291,305
# $K===================!                 BAD    mass_y!=mol
# $K===========================!         BAD    mass_y!=mol
# $K==================================$  GOOD   mass_y==mol

from timeit import default_timer as timer

def finding_ions(peaks_list,seq,mass_list,key,mass_change):
    masses_dict[key]=[]
#    print(key,'    :',masses_dict[key])
    for n in range(len(seq)):
        masses_dict[key].append(0)
        if mass_list[n]+mass_change in peaks_list:
            masses_dict[key][n]=mass_list[n]+mass_change
            pass
        if  masses_dict[key][n]!='' and masses_dict[key][n] in peaks_list:
            peaks_list.remove(masses_dict[key][n])
            pass
        pass
    pass
#    print(key,'new :',masses_dict[key])

MW_AA = {57:'G',71:'A',87:'S',97:'P',99:'V',101:'T',103:'C',
         113:'I/L',114:'N', 115:'D',128:'K/Q',129:'E',131:'M',137:'H',
         147:'F',156:'R',161:'AcC',163:'Y',186:'W'}
AA_MW = {'G':57,'A':71,'S':87,'P':97,'V':99,'T':101,'C':103,
         'I/L':113,'N':114,'D':115,'K':128,'K/Q':128,'E':129,'M':131,
         'H':137,'F':147,'R':156,'AcC':161,'Y':163,'W':186}

####    INPUT PEAKS

# PROJECT : OCR with Tesseract from Google and pyOCR/pytesser to bind it.
# I found : https://pythontips.com/2016/02/25/ocr-on-pdf-files-using-python/

peaks_list=[]
while peaks_list==[]:
    in_mode=input('Input type : .txt file (F) or manual (M) ? ')
#file input
    if in_mode=='F':
        filename=input('\nWhat is the name of your file ? ')#get name of file
        mol=int(input('\nWrite the m/z of the molecular ion :\n'))#molecular ion
        start = timer()
        filename=filename+'.txt'
        with open(filename, "rt", encoding='utf-8') as peaks_file:#open file copy text
            for line in peaks_file:
                for peak in line:
                    peaks_list.append(peak)
                    pass
                pass
        peaks_file.close()
    elif in_mode=='M':
#manual input
        peaks_input = input('\nWrite your MS/MS peaks values separated by a space :\n')
        mol=int(input('\nWrite the m/z of the molecular ion :\n'))#molecular ion
        start = timer()
        peaks_list = list(map(int, peaks_input.split(' ')))
        print(peaks_list)
    elif in_mode!='F' and in_mode!='M':
        print('Please enter F for .txt file or M for manual.\n')
    pass

# List of peaks useful for troubleshooting, obtained from actual MS/MS data,
# 704,311,125,890 are added to create a branch
# The sequence is :['K', 'I/L', 'I/L', 'E', 'V', 'I/L', 'A', 'T', 'K/Q']
# The branch is :                                'C', 'W'
#peaks_list=[101, 129, 147, 202, 230, 260, 273, 301, 342, 373, 386, 414,
#            485,495, 502, 513, 601, 624, 642, 656, 714, 727, 755, 785,
#            801, 840, 868, 886, 1014,704,311,125,890]
#mol=1014

####    START
if mol not in peaks_list:
    peaks_list.append(mol)
peaks_list.append(1)#for the H+ on the first b ion
peaks_list.sort()
#peaks_list_original=peaks_list #not used yet

####    CONFIRM TO USER
print ('\nYour values are : ',', '.join(map(str,peaks_list)),
       '.\n\nm/z(molecular ion) = ',mol,'\n')

####    INITIATION OF SEQUENCING Y1 = K or R,
masses_dict={}
mol_b=mol-18 #mol-18 for calculating b ions
if 147 in peaks_list and (mol_b-128) in peaks_list:
    #print('Y1=K')#dev
    seq=['K']
    mass_y=147
    masses_dict['y']=[mass_y]
    peaks_list.remove(mass_y)
    mass_b=mol_b-128
    masses_dict['b']=[mass_b]
    peaks_list.remove(mass_b)
elif 175 in peaks_list and (mol_b-156) in peaks_list:
    #print('Y1=R')#dev
    seq=['R']
    mass_y=156
    masses_dict['y']=[mass_y]
    peaks_list.remove(mass_y)
    mass_b=mol_b-156
    masses_dict['b']=[mass_b]
    peaks_list.remove(mass_b)
else: print ('restart1')#dev

####    SEQUENCING
readings={}
#format of readings :
#readings={mass_y:[[mass_y,mass_b,seq],[y],[b],[aa]]}
multiple=[[],[]]
#multiple=[[mass_y before branch],[number of branches]]
while mass_y!=mol and mass_b!=1:
    #print('SEQ while :',seq)
    readings[mass_y]=[[mass_y,mass_b],[],[],[]]
    #print('mass_y :',mass_y,'mass_b :',mass_b)#dev
    for x in sorted(MW_AA.keys()):
        #print('mass_y+x :',mass_y+x,'mass_b :',mass_b-x,'// x :',x)#dev
        if mass_y+x in peaks_list and mass_b-x in peaks_list:
            print('peak found')#dev
            readings[mass_y][1].append(mass_y+x)
            readings[mass_y][2].append(mass_b-x)
            readings[mass_y][3].append(MW_AA[x])
            pass
        pass
    #print('#=====#\nreadings :',readings,'\nx :',x,'\n#=====#')#dev
    if x==186:# so that all possible peaks have been checked
        multiple[0].insert(0,mass_y)
        multiple[1].insert(0,len(readings[mass_y][3]))
        #print('multiple',multiple,'\n#=====#')
        if multiple[1][0]>=1:
            #print('mass_y 1 :',mass_y,'mass_b 1 :',mass_b,'seq :',seq)
            mass_b=readings[mass_y][2][0]
            seq.append(readings[mass_y][3][0])
            mass_y=readings[mass_y][1][0]
            #print('mass_y 2 :',mass_y,'mass_b 2 :',mass_b,'seq :',seq)
            pass
        elif multiple[1][0]==0:
            #print('multiple',multiple)
            #del multiple[1][0]
            #print('multiple',multiple)
            print('readings is empty, trying from last branch')
            #find last branch, with multiple[1]!=1
            branch=next((i for i, x in enumerate(multiple[1]) if x>1), None)
            #print('branch',branch)
            #delete the multiple[0] and multiple [1] after the branch
            del multiple[0][:branch]
            del multiple[1][:branch]
            #print('multiple',multiple)
            #reset mass_y to before branch
            mass_y=multiple[0][0]
            #print('mass_y',mass_y)
            #remove one branch
            multiple[1][0]=multiple[1][0]-1
            #delete the part after the branch in readings
            for n in sorted(readings.keys()):
                if n>mass_y:
                    del readings[n]
                    pass
                pass
            #print('multiple',multiple)
            #delete the first reading after the branch
            #print(readings)#dev
            del readings[mass_y][1][0]
            del readings[mass_y][2][0]
            del readings[mass_y][3][0]
            #reset seq to what it was before the branch
            del seq[(len(seq)-branch):]
            #use values of second branch
            mass_b=readings[mass_y][2][0]
            #print('mass_b',mass_b)
            seq.append(readings[mass_y][3][0])
            #print('seq',seq)
            mass_y=readings[mass_y][1][0]
            #print('mass_y',mass_y)
            pass
        pass

####    CALCULATING M/Z OF IONS
#print('seq :',seq)
for n in sorted(readings.keys()):
# m/z of y" ions
    masses_dict['y'].append(readings[n][1][0])
    peaks_list.remove(masses_dict['y'][-1])
# m/z of b ions
    masses_dict['b'].append(readings[n][2][0])
    peaks_list.remove(masses_dict['b'][-1])
    pass
#print(masses_dict['y'],masses_dict['b'])#dev
#print('peaks_list :',peaks_list)#dev
#print('multiple',multiple)#dev
masses_dict['b'].remove(1)
masses_dict['b'].insert(0,mol)
# m/z of a ions
finding_ions(peaks_list,seq,masses_dict['b'],'a',-28)
# NEXT 1 : these have to be present in the ion not the whole seq
# m/z of ions with H2O loss
if any(STED in residue for residue in seq for STED in 'STED'):
    first_STED=len(seq)
    last_STED=0
    for STED in 'STED':
        if seq.index(STED)<first_STED:
            first_STED=seq.index[STED]
            pass
        if list(reversed(seq)).index(STED)>last_STED:
            last_STED=list(reversed(seq)).index(STED)
            pass
        pass
    print('first_STED',first_STED)
    finding_ions(peaks_list,seq[:last_STED+1],masses_dict['y'][:last_STED+1],'y-H2O',-18)
    finding_ions(peaks_list,seq[first_STED:],masses_dict['b'][first_STED:],'b-H2O',-18)
    finding_ions(peaks_list,seq[first_STED:],masses_dict['a'][first_STED:],'a-H2O',-18)
    pass
# m/z of ions with NH3 loss
if any(RKNQ in residue for residue in seq for RKNQ in 'RKNQ'):
    first_RKNQ=len(seq)
    last_RKNQ=0
    for RKNQ in 'RKNQ':
        if seq.index(RKNQ)<first_RKNQ:
            first_RKNQ=seq.index[RKNQ]
            pass
        if list(reversed(seq)).index(RKNQ)>last_RKNQ:
            last_RKNQ=list(reversed(seq)).index(RKNQ)
            pass
        pass
    finding_ions(peaks_list,seq[:last_RKNQ+1],masses_dict['y'][:last_RKNQ+1],'y-NH3',-17)
    finding_ions(peaks_list,seq[first_RKNQ:],masses_dict['b'][first_RKNQ:],'b-NH3',-17)
    finding_ions(peaks_list,seq[first_RKNQ:],masses_dict['a'][first_RKNQ:],'a-NH3',-17)
    pass
####    OUTPUT
# NEXT 2 : do not display lists that are empty
#if all(0==value for value in masses_dict['y-NH3']):
#    print('y-NH3 is empty')

print('final peaks :',peaks_list)#dev
#print('seq',seq)#dev
#print(readings)#dev
print('\n{0:<3}{1:<5}{2:<7}{3:<7}{4:<7}{5:<7}{6:<7}{7:<7}{8:<7}{9:<7}{10:<7}'
    .format('n','Seq','y','y-H2O','y-NH3','b','b-H2O','b-NH3','a','a-H2O','a-NH3'))
print('-----------------------------------------------------------------------')
for n in range(len(seq)):
    print('{0:<3}{1:<5}{2:<7}{3:<7}{4:<7}{5:<7}{6:<7}{7:<7}{8:<7}{9:<7}{10:<7}'
    .format((len(seq)-n),seq[n],masses_dict['y'][n],masses_dict['y-H2O'][n],
    masses_dict['y-NH3'][n],masses_dict['b'][n],masses_dict['b-H2O'][n],
    masses_dict['b-NH3'][n],masses_dict['a'][n],masses_dict['a-H2O'][n],
    masses_dict['a-NH3'][n]))

#print('list_multi : ',list_multi)#dev
print('\nThe sequence is',len(seq),'residues long.')

####    END
#Timing is the coolest thing !
end=timer()
print ('\nDone in {0} secs.'.format(end-start),'\n')
