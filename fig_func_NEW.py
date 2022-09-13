#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 00:28:14 2022

@author: dunn
"""

import file
import figure
from PreProcess_package import data
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

def init(filelist, path): #***turn into dict visualization***EDIT***
    file_dict=u.make_dict.by_autonumber(filelist) #Creat a dictionary to use as shortcuts to select files

    file_dict=dict(sorted(file_dict.items(), key=lambda item: item[0])) #sort by number
    for key, val in file_dict.items():
        print(key,val)
    return file_dict

def make_df(selection, select_dict):
    df=pd.DataFrame()
    for s in selection: 
        data=pd.read_csv(indir+select_dict[s], header=None)
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

def base_plot(df, i_up=0, color='name', clusterGroup='name', lineGroup='name', title=None,
              xax='raman shift', yax='intensity'):
    df=df.copy(deep=True)
    
    df['num']=df[clusterGroup].astype('category').cat.codes
    label=df[clusterGroup].astype('category')
    cat_dict=dict(enumerate(label.cat.categories))
    #Calculate intensity increase
    df['increase']=df['num']*i_up
    #Apply increase
    df['intensity']=df[yax]+df['increase']
    
    #Create Figure
    fig=px.line(df, x=xax, y='intensity',
                color=color, line_group=lineGroup,
                title=title, width=900, height=400)
    return fig
#%%
 
if __name__ == '__main__':
    filelist=file.names.find(indir)
    print('Files available:')
    file_dict=init(filelist,indir)
    
    #df=make_df([8,9,11,13,15], file_dict)
    #print(df)
    
    '''
    print('\nEdit DF, Add column(s):')
    new_list=u.df.col_edit(df, 'name', '_', 0)
    u.df.col_add(df, new_list, 'id')'''
'''    
    base=base_plot(df, i_up=1700, color='id', title='Neurospheres 08/18', clusterGroup='id')
    fig=figure.format(base)
    anno=figure.anno(fig,text='60s, 532nm, 10mW, 40X', x=0.7,size=20)
    figure.save.web(anno, outdir, 'neurosphereVmedia_08182022_60s_532nm_10mW_40X_stacked')
    
'''

        