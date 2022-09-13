#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Import raw CSV files, apply preprocessing steps

Created on Sat Jun 11 00:28:14 2022

@author: dunn
"""


import file as f
import figure
from Preprocess import baseline
from Preprocess import zap
import __utils__ as u
import pandas as pd
import scipy.signal as ss
import pybaselines.spline as py
import plotly.express as px

home = '/home/dunn/Data/'
root = home + 'Glass/'
indir = root+'0_raw/'
outdir = root+'1_processed/'
   
    
def process(file):
    #1)Extract data + name from file
    df=pd.read_csv(indir+file, header=None)
    #option truncate
    x,y0=u.df.col_extract(df,0), u.df.col_extract(df, 1)
    fullname=f.names.edit(file, '.', 0)
    
    #2) Fix Spectra: remove spikes from cosmic rays
    try:
        y=zap.fix(y0)
        #y=zap.fix(y0)
    except IndexError: #Bias IndexError for when spike is detected at edges of datapp
        y=y0
        pass

    #3) Smooth Intensity
    iZS=ss.savgol_filter(y, 9, 3)

    #4) Apply baseline
    b_out=py.pspline_asls(iZS)[0]
    iZSB=y-b_out   
    
    #5) Processing Figure
    fig=figure.preprocess(x, y, iZSB, b_out, fullname)
    base=px.line(x=x, y=iZSB) #Simple plot, just result
    fig=figure.format(base)
    
    #6) Returns    
    return x, iZSB, fullname, fig, y, y0, b_out

def result(file, fig_save=False, fig_type='web'):
    
    X, Y, Name, Fig, Zap, Raw, Base = process(file)
    #Fig.show()
    
    full_df=pd.DataFrame(list(zip(X,Y,Zap,Raw,Base)), columns=['raman shift','intensity','zapped','raw','baseline'])
    df=pd.DataFrame(list(zip(X,Y)), columns=['raman shift','intensity'])
    
    if fig_save==False:
        pass
    elif fig_save==True:
        if fig_type=='web':
            figure.save.web(Fig, outdir, Name)
        elif fig_type=='static':
            figure.save.static(Fig, outdir, Name)
        else:
            print('Invalid fig_type. Options = \'web\' or \'static\'.')
        
    else:
        print('Invalid fig_save input.')
    return df, Fig, Name
    
                #figure.save.web(Fig, outdir, Name)

                #figure.save.static(Fig, outdir, Name)
        
if __name__=='__main__':
    filelist=f.names.find(indir)
    u.check_path(outdir)
    for File in filelist:
        DF,Fig,Name=result(File)
        Fig.show()
        DF.to_csv('%s%s.csv'%(outdir,Name), index=False)
        #print(DF)
        
    print('\nEnd.')
    