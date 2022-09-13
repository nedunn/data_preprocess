#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 12 20:34:58 2022

@author: dunn
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.offline import plot
import scipy.signal as ss
#from scipy.signal import find_peaks
import numpy as np
import file
import __utils__

class save:
    #suffix (fig type) does include '.pdf' and ',=.svg'
    def static(fig, path, name, suffix='jpeg'):
        __utils__.check_path(path) #from 'file.py'
        fig.write_image('%s%s.%s'%(path,name,suffix))
        print('Saved figure(s can now be found here:   %s'%path)

    def web(fig, path, name):
        __utils__.check_path(path) #from 'file.py'
        fig.write_html('%s%s.html'%(path,name))
        print('Saved figure(s) can now be found here:   %s'%path) 

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

def preprocess(xax, int_raw, int_final, baseline, name, figType='jpeg'):
    '''Generates a 2 pane figure that shows raw spectra, baseline, and output spectra.

    Parameters
    ----------
    xax : np.array / float list
        X axis values (EX wavelengh)
    int_raw : np.array
        Spectra raw intensity
    int_final : np.array
        Spectral intensity  after processing
    baseline : np.array
        Baseline output, what is subtracted from the raw intensity
    name : string
        Name of file, will be used as the title in the resuling figure
    figType : 'jpeg', 'bmp', etc, optional
        Format type of the output figure. The default is 'jpeg'.

    Returns
    -------
    fig : Object
        2 panel figure that contains original spectra and resutling, processed, spectra

    '''
    #initalize figure
    fig=make_subplots(rows=2, cols=1,
                      shared_xaxes=True, shared_yaxes=True,
                      vertical_spacing=0.05,
                      x_title='Raman Shift (cm-1)', y_title='Intensity')
    #add traces
    fig.append_trace(go.Scatter(x=xax, y=int_raw, name='raw'),row=1,col=1)
    fig.append_trace(go.Scatter(x=xax, y=baseline, name='baseline'),row=1,col=1)
    fig.append_trace(go.Scatter(x=xax, y=int_final, name='output'),row=2,col=1)
    #adjust layout
    fig.update_layout(title_text=name,title_font_size=15,plot_bgcolor='rgba(0,0,0,0)')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', gridcolor='lightgrey')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', gridcolor='lightgrey')
    return fig

def format(input_fig, title_size=30, axis_size=20, reverse_legend=True):
    fig=go.Figure(input_fig)
    fig.update_layout(title_font_size=title_size, plot_bgcolor='rgba(0,0,0,0)',
                      margin=dict(l=20,r=20,b=20,t=50),
                      legend=dict(yanchor='bottom',y=0))
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black',
                     title_text='Relative Intensity', title_font_size=axis_size,
                     gridcolor='white')
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black',
                     title_text='Raman Shift (cm-1)', title_font_size=axis_size,
                     gridcolor='white') #lightgrey to see gridlines
    if reverse_legend == True:
        fig.update_layout(legend_traceorder='reversed')
    elif reverse_legend == False:
        pass
    return fig

def frames(df, name_col, x_col, y_col, size):
    names=[name.split('-') for name in df[name_col]]
    traces=[name[2] for name in names]
    fig=px.line(df, x=x_col, y=y_col, color=traces, line_group=df[name_col])
    return fig

def anno(input_fig, x=1, y=1.15, text=None, size=None):
    fig=go.Figure(input_fig)
    fig.add_annotation(xref='paper', yref='paper',
                       xanchor='left',
                       x=x, y=y,
                       showarrow=False, align='center',
                       text=text)
    if size==None:
        pass
    else:
        fig.update_annotations(font=dict(size=size))
    return fig
    '''fig.add_annotation(xref='paper', yref='paper',
                   xanchor='left',
                   x=1, y=1.15,
                   showarrow=False,
                   align='center',
                   text='%s, %s'%(laser, power))
    fig.add_annotation(xref='paper', yref='paper',
                       xanchor='left',
                   x=1, y=1.10,
                   showarrow=False,
                   align='center',
                   text='%s, %s'%(objective, time))
    fig.add_annotation(xref='paper', yref='paper',
                       xanchor='left',
                   x=1, y=1.05,
                   showarrow=False,
                   align='center',
                   text='%s'%date)'''

class peaks:
    def detect(df, threshold=300, sensitive=15):
        y=df.iloc[:,1]
        y=np.array(y)
        np.array(y)
        
        i_peaks=ss.argrelextrema(y, np.greater, order=sensitive)[0] #returns index value where peaks are detected
        y_peaks=y[i_peaks]
        peak_plot=[y for y in y_peaks if y > threshold] #remove elements that are greater than a threshold from a list
        
        peakDF=(df[df.iloc[:,1].isin(peak_plot)])
        peakDF.reset_index(inplace=True, drop=True)
        peakDF.columns=['wave number', 'input df intensity']
        
        return(peakDF)
    #def add_peaks(input_fig, peakDF, y_max=1.11):
        
        
    