#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 00:28:14 2022

@author: dunn
"""

import file
import figure
import data
import __utils__ as u
import pandas as pd
import scipy.signal as ss
import pybaselines.spline as py
import plotly.graph_objects as go
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

import fig_func_NEW as foo

root = '/home/dunn/Data/hippo_tissue/04-01/'
indir = root+'2_averaged/'
outdir = root+'figures/'

def load(dir_path):
    filelist=file.names.find(indir)
    file_dict=foo.init(filelist, indir)
    return file_dict

def col_edit(df, col_name, new_col, text, loc):
    new=[]
    for x in df[col_name]:
        new.append(file.names.edit(x, text, loc))
    df[new_col]=new
    return df
    
def fix_df(df):
    l1=[]
    l2=[]
    for x in df['name']:
        y=x.split('_')[0]
        l1.append(y)
    for x in df['name']:
        y=x.split('_')[1]
        l2.append(y)    
    df['id']=l1
    df['group']=l2
    
    fig=foo.base_plot(df, sample_dfcol='group')
    return fig
    
def make_fig(df):
    fig=foo.base_plot(df, sample_dfcol='group')
    return fig
    
def finish_fig(fig):
    figure.annotation(fig, x=0.7, text='785nm, 10mW, 40X, 60s')
    figure.annotation(fig, x=0.7, y=1.10, text='ewe hippocampus dry slices')
    figure.annotation(fig, x=0.7, y=1.05, text='04-01-2022')
    figure.annotation(fig, x=0.7, y=1, text='spectra #: %s'%select)
    return fig


if __name__ == '__main__':
    file_dict=load(indir)
    
    #control=[2,3,5,6,10]
    #lps=[16,17,18,20]
    select=[16,17,18,20,23,24,25,26,27]
    
    df=foo.make_df(select, file_dict)
    
    #f=foo.base_plot(df)

    #print('col_edit(df, \'col to edit\',\'new col\', \'split text\', \'int\')')

        