import numpy as np
import matplotlib.pyplot as plt
import h5py
from labrad import types as T
import base64
import os

URL_PREFIX = 'data:application/labrad;base64,'

def read_metadata(val):
    if not isinstance(val,str) or URL_PREFIX not in val:
        return val
    else:
        try:
            f = base64.urlsafe_b64decode(bytes(val[len(URL_PREFIX):],'utf-8'))
            t,data_bytes = T.unflatten(f,'ss')
            #print('typea: '+ str(type(data_bytes)))

            data = T.unflatten(bytes(data_bytes,'utf-8'),t)
        except:
            f = base64.urlsafe_b64decode(bytes(val[len(URL_PREFIX):],'utf-8'))
            t,data_bytes = T.unflatten(f,'ss')
            #print('typeb: '+ str(type(data_bytes)))
            data = T.unflatten(data_bytes,t)

            #data = 'err'
        return data

def readDVFile(path,directory_pointer='./',output='np'):
    try:
        if isinstance(path,str):
            hf = h5py.File(path,'r')
            DV = hf.get('DataVault')
        elif isinstance(path,int):
            for filename in os.listdir(directory_pointer):
                if filename[-4:] == 'hdf5' and int(filename[0:5]) == path:
                    hf = h5py.File(filename,'r')
                    DV = hf.get('DataVault')
                    break
    except:
        print('Cannot open file, perhaps an invalid path')
        return -1
    metadata = {}
    dep_list = []
    indep_list = []
    for element in DV.attrs.keys():
        read_data = read_metadata(DV.attrs.get(element))
        if read_data != '':
            metadata[element] = read_data
        if 'Dependent' in element and 'label' in element:
            dep_list.append(read_data)
        if 'Independent' in element and 'label' in element:
            indep_list.append(read_data)
    var_list = indep_list + dep_list
    
    if output == 'np':
        raw_data = np.zeros((DV.size,len(var_list)))
        for row in range(0,DV.size):
            for elt in range(0,len(var_list)):
                raw_data[row,elt] = DV[row][elt]
    elif output == 'dict':
        raw_data = {}
        for variable in var_list:
            raw_data[variable] = np.zeros(DV.size)
        for row in range(0,DV.size):
            for elt in range(0,len(var_list)):
                raw_data[var_list[elt]][row] = DV[row][elt]
    hf.close()
    return metadata,var_list,raw_data
