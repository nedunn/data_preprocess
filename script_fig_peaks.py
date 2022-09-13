#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 16:13:12 2022

@author: dunn
"""
import script_quick_fig as f

datas,basefig=f.result()

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

def init(filelist, path): #***turn into dict visualization***EDIT***
    file_dict=u.make_dict.by_autonumber(filelist) #Creat a dictionary to use as shortcuts to select files
    #print('Files available:')
    #file_dict=dict(sorted(file_dict.items(), key=lambda item: item[0])) #sort by number
    #for key, val in file_dict.items():
    #    print(key,val)
    return file_dict

def add(input_fig,peakDF, y_max=1.11):
    fig=go.Figure(input_fig)
    peaks=pd.DataFrame(peakDF)
    peaks['y_max']=y_max
    
    #Generate coordinates for peak labels
    for w,i in zip(peaks.iloc[:,0], peaks['y_max']):
        fig.add_annotation(x=w,y=i,text=f'{w:.0f}',showarrow=False,
                           textangle=-50,yref='paper')
    #Add vertical lines
    for x in peaks.iloc[:,0].to_list():
        fig.add_vline(x=x,line_width=0.5,opacity=0.4)
    
    return fig
    


#%%

Filedict=init(file.names.find(indir), indir)

DF=pd.read_csv(indir+Filedict[1])

peaks=figure.peaks.detect(DF,sensitive=26)
    
fig1=figure.format(basefig)
fig=add(fig1,peaks)

