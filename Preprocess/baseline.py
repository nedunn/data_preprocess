#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FORMERLY data.py
Functions relating to data retrevial and processing.

Created on Sat Jun 11 00:34:03 2022

@author: dunn
"""
import numpy as np
import pandas as pd
import pybaselines as py
from scipy.sparse import csc_matrix, eye, diags #smooth.whitaker
from scipy.sparse.linalg import spsolve #smooth.whitaker


class smooth:
    def Whittaker(x,w,lambda_,differences):
        '''
        Function formeraly (6/12/22), known as WhittakerSmooth
        Penalized least squares algorithm for background fitting.
        
        Parameters
        ----------
        x : float
            Input data (i.e. chromatogram of spectrum)
        w : binary masks
            value of the mask is 0 if a point belongs to peaks and one otherwise)
        lambda_ : TYPE
            Parameter that can be adjusted by user. The larger lambda is,
            the smoother the resulting backgrouand.
        differences : int
            Indicates the order of the difference of penalties.
        
        Returns
        -------
        The fitted background vector

        '''
        X=np.matrix(x)
        m=X.size
        i=np.arange(0,m)
        E=eye(m,format='csc')
        D=E[1:]-E[:-1] # numpy.diff() does not work with sparse matrix. This is a workaround.
        W=diags(w,0,shape=(m,m))
        A=csc_matrix(W+(lambda_*D.T*D))
        B=csc_matrix(W*X.T)
        background=spsolve(A,B)
        return np.array(background)   
    
class baseline:
    def airPLS(x, lambda_=100, itermax=15, porder=1):        
        '''
        Adaptive iteratively reweighted penalized lease squares for baseline fitting

        Parameters
        ----------
        x : float
            Input data (i.e. chromatogram of spectrum)
        lambda_ : TYPE
            Parameter that can be adjusted by user. The larger lambda is, the smoother the resulting background, z.
            Original value = 100.
        itermax : TYPE
            Original value = 15.
        porder : TYPE
            Adaptive iteratively reweighted penalized least squares for baseline fitting.
            Original value = 1.

        Returns
        -------
        z : TYPE
            DESCRIPTION.

        '''
        m=x.shape[0]
        w=np.ones(m)
        for i in range(1,itermax+1):
            z=smooth.Whittaker(x,w,lambda_, porder)
            d=x-z
            dssn=np.abs(d[d<0].sum())
            if(dssn<0.001*(abs(x)).sum() or i==itermax):
                if(i==itermax): print('WARING max iteration reached!')
                break
            w[d>=0]=0 # d>0 means that this point is part of a peak, so its weight is set to 0 in order to ignore it
            w[d<0]=np.exp(i*np.abs(d[d<0])/dssn)
            w[0]=np.exp(i*(d[d<0]).max()/dssn)
            w[-1]=w[0]
        return z

class frames:
    def average(df, x_col, y_col, group_col):
        '''
        Funtion that takes an input DF containing multiple samples and frames.
        Averages frames and returns the result as a new DF.    

        Parameters
        ----------
        df : DataFrame
            Input DF containing multiple sample information with column IDing groups to frame average.
        x_col : str(column name)
            Raman shift column
        y_col : str(column name)
            Intensity column
        group_col : str(column name)
            Group name (frame average group with frame ID dropped)

        Returns
        -------
        newDF: DataFrame containing frame averaged data.
            3 columns returned: 'raman shift', 'group', 'intensity'

        '''
        df=df.copy(deep=True) #Prevents changes being made to input DF
        df[y_col]=pd.to_numeric(df[y_col])
        frameAve=df.groupby([x_col,group_col],as_index=True).intensity.mean() #pd.Series containing 1 column (intensity) with 2 indexes (ramanShift, sample)
        resultDF=pd.DataFrame(frameAve) #Dataframe containing 1 column (intensity) with 2 indexes (ramanShift, sample)
        resultDF=resultDF.reset_index() #Result = df with 3 columns: 'ramanShift', 'sample', 'intensity'
        return resultDF

        