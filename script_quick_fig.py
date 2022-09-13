#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 12:19:20 2022

@author: dunn
"""

import file
import figure
import __utils__ as u
import pandas as pd
import scipy.signal as ss
import pybaselines.spline as py
import plotly.graph_objects as go
import plotly.express as px
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


root = '/home/dunn/Data/08-15/'
indir = root+'1_processed/'
outdir = root+'figures/'


#%%Functions
def init(filelist, path): #***turn into dict visualization***EDIT***
    file_dict=u.make_dict.by_autonumber(filelist) #Creat a dictionary to use as shortcuts to select files
    print('Files available:')
    
    file_dict=dict(sorted(file_dict.items(), key=lambda item: item[0])) #sort by number
    for key, val in file_dict.items():
        print(key,val)
    return file_dict

def make_df(selection, select_dict):
    df=pd.DataFrame()
    for s in selection: 
        data=pd.read_csv(indir+select_dict[s])
        name=file.names.edit(select_dict[s],'.',0)
        '''
        #Trouble shooting help:
        print()
        print(name)
        print(list(data.columns))
        print(data)'''
        data['name']=name
        
        df=df.append(data)
    df.columns=['raman shift', 'intensity', 'name'] #ERROR SOURCE: will vary with whether or not import csvs have headings
    df.reset_index(inplace=True, drop=True)    
    return df

#%%Call
if __name__=='__main__':
    filedict=init(file.names.find(indir),indir)
    print('')
    
    df=make_df([1,2,3,4,5,6,7,8,9,10], filedict)
    print('File names in DF:')
    print(*list(set(df['name'].to_list())),sep='\n')
    print('')
    
    fig=base_plot(df)
    fig.show()

def result():
    filedict=init(file.names.find(indir),indir)
    df=make_df([1,2,3,4,5,6,7,8,9,10], filedict)
    fig=figure.base_plot(df)
    return df, fig


    
    
