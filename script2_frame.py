#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1) Import preprocessed data
2) Truncate 
2.1) Show Pre-Post turncation
3) Frame Comparison
4) Average
4.1) Show figure ***not yet in code***
5) Save output



@author: dunnw
"""

from PreProcessing_package import file as f
from PreProcessing_package import figure
import __utils__ as u
import pandas as pd
import scipy.signal as ss
import pybaselines.spline as py
import plotly.graph_objects as go
import plotly.express as px


root = '/home/dunn/Data/08-18/'
indir = root+'1_processed/frames/'
outdir = root+'2_averaged/'

filelist=f.names.find(indir)

def grab_truncate(file, i_before=None, i_after=None):
    #1)Extract data + name from file
    df=pd.read_csv(indir+file)
    x0,y0=u.col_extract(df,0), u.col_extract(df, 1)
    fullname=f.names.edit(file, '.', 0)
    x=x0[i_before:i_after]
    y=y0[i_before:i_after]  
    
    #2) Figure
    fig=go.Figure(layout=go.Layout(title=fullname)) #initialize
    #Traces
    before=go.Scatter(x=x0, y=y0, name='original')
    after=go.Scatter(x=x, y=y, name='truncated')
    fig.add_trace(before)
    fig.add_trace(after)
    #Adjust layout
    fig1=figure.format(fig, title_size=20)
    fig1=figure.anno(fig1, text='test')
    
    #Dataframe
    df=pd.DataFrame(list(zip(x,y)),
                    columns=['raman shift','intensity'])
    return fullname, df, fig

def frame_comparison(df, x_col='raman shift', y_col='intensity', file_col='spectra_name'):
    df=df.copy(deep=True)
    #Determine Frame Groups
    groupList=[]
    for name in df[file_col]:
        group=name.split('-Frame-')[0]
        groupList.append(group)
    df['group']=groupList
    #List of unique vales in groupList
    groups=list(set(groupList)) #?should this be taken from the DF?    
    for g in groups:
        data=df.loc[df['group']==g]
        fig=px.line(data, x=x_col, y=y_col, color=file_col,
                    title='%s'%g)
        fig.update_yaxes(showline=True, linewidth=1, linecolor='black',
                         title_text='Relative Intensity', title_font_size=15,
                         gridcolor='lightgrey')
        fig.update_xaxes(showline=True, linewidth=1, linecolor='black',
                         title_text='Raman Shift (cm-1)', title_font_size=15,
                         gridcolor='lightgrey')
        fig.update_layout(showlegend=False, title_font_size=20, plot_bgcolor='rgba(0,0,0,0)')
        fig.show()

def frameAverage(df, rsCol, filename_col):
    df=df.copy(deep=True) #Prevents changes being made to input DF
    df['intensity']=pd.to_numeric(df['intensity'])
    
    #Generate 'frame group' names = file names with 'frame' dropped
    groupList=[]
    for name in df[filename_col]:
        group=name.split('-Frame-')[0]
        groupList.append(group)
    df['frameGroup']=groupList
    
    frameAve=df.groupby([rsCol,'frameGroup'], as_index=True).intensity.mean() #pd.Series containing 1 column (intensity) with 2 indexes (ramanShift, sample)
    newDF=pd.DataFrame(frameAve) #Dataframe containing 1 column (intensity) with 2 indexes (ramanShift, sample)
    newDF=newDF.reset_index() #Result = df with 3 columns: 'ramanShift', 'sample', 'intensity'
    print('Frame Average: \n%s%s'%(newDF.head(2), newDF.tail(2)))
    return(newDF)

def splitAndSave(df, splitByCol, nameEnding, output_path): #Split up the dataframe 
    splits=list(df.groupby(splitByCol)) #Creates lift of tuples, each a dataframe for an averaged sample ramanShift+intensity
    i=0  
    for splits[i] in splits:
        data=splits[i][1] #Access the dataframe portion of the tuple
        data.drop(splitByCol,axis=1,inplace=True) #Drop columns that you dont want saved to the final csv output
        fileName=splits[i][0] #Access the dataframe NAME portion of tuple
        format_fileName=fileName+nameEnding
        data.to_csv(output_path+'%s.csv'%format_fileName,index=False,header=False)
        i=i+1
    print('Averaged files should now be found in %s'%output_path)

if __name__=='__main__':
    #Truncate
    __utils__.check_path(outdir)
    DF=pd.DataFrame()
    for file in filelist:    
        name, df, fig = grab_truncate(file,i_before=170) #truncated data
        df['spectra_name']=name
        DF=DF.append(df)
    #All data in 1 Dataframe
    DF.reset_index(inplace=True,drop=True)
    #frame_comparison(DF)
    
    DFave=frameAverage(DF, 'raman shift', 'spectra_name')
    
    splitAndSave(DFave, 'frameGroup', '', outdir)

    print('\nEnd.')