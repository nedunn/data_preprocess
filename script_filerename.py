#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 26 12:06:04 2022

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


root = '/home/dunn/Data/2022-08-24/'
indir = root+'1_processed/'
outdir = root+'1_processed_renamed/'

    
def process(file):
    df=pd.read_csv(indir+file)
    name=f.names.edit(file,'.',0)
    
    idAndFrame=name.split(' ')[-1]
    framesplits=idAndFrame.split('-')
    spotid=framesplits[0]
    frame=framesplits[-1]
    
    sample=name.split('_785')[0]
    
    newname='%s-spot%s-frame%s'%(sample,spotid,frame)
    
    return df, newname
    
    

if __name__=='__main__':
    filelist=f.names.find(indir)
    u.check_path(outdir)
    for file in filelist:
        df,name=process(file)
        df.to_csv('%s%s.csv'%(outdir,name), index=False)
        
    print('\nEnd.')
    