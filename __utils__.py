#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 15:13:50 2022

@author: dunn
"""
import pandas as pd
import file
import os
import numpy as np
from datetime import datetime

def date():
    dt=datetime.now()
    return dt.year, dt.month, dt.day

def check_path(dir_to_check): 
    '''
    Checks is directory exists. If not, directory will be created.
    If direct does exist, indicate so to user.

    Parameters
    ----------
    dir_to_check : TYPE
    
    check:
        True = directory exitsts
        False = directory does not exist

    Returns
    -------
    None.

    '''
    check=os.path.isdir(dir_to_check) #Bool if dir exists
    #useful related code: for (root, dirs, files) in os.walk(indir):
    if check==True:
        print('\nOutput directory (%s) already exists.\n'%dir_to_check)
        print('This directory contains %s files.'%(len(os.listdir(dir_to_check))))
    elif check == False:
        print('\nOutput directory (%s) does not currently exist, will be created for you.\n'%dir_to_check)
        os.mkdir(dir_to_check)
        print('\nThe following directory has been created for you: %s\n'%dir_to_check)
    else:
        print('\n***check path function error***\n')


class make_dict:
    def by_autonumber(input_list): #For files that have unique numbers assigned to them automatically in Lightfield
        key_list=[]
        for item in input_list:
            k=item.split(' ')[2] #alt = [0]
            k=k.split('.')[0]
            key=int(k)
            key_list.append(key)
        result={key_list[i]:input_list[i] for i in range(len(key_list))}
        return result
    def default(input_list):
        key_list=[]
        for item in input_list:
            key=item.split('_')[0]
            key=int(key)
            key_list.append(key)
        result={key_list[i]:input_list[i] for i in range(len(key_list))}
        return result

def idAndFrame(input_list): #For files that have unique numbers assigned to them automatically in Lightfield
    ##-Frame-#.csv
    key_list=[]
    for item in input_list:
        k=item.split(' ')[2] #alt = [0]
        key=int(k)
        key_list.append(key)
    result={key_list[i]:input_list[i] for i in range(len(key_list))}
    return result

class df:
#    def grab_df(select_num, select_dict=None):
    def create(*selection, select_dict=None, path=None):
        dfs=[]
        
        for s in selection:
            data=pd.read_csv(path+select_dict[s])
            filename=file.names.edit(select_dict[s],'.',0)
            data['file']=filename
            dfs.append(data)
        df=pd.concat(dfs)
        df.reset_index(inplace=True, drop=True)
        return df
    
    def col_edit(df,edit_col,split_value,split_keep_loc,show=True):
        '''
        Returns a list -> input for col_add

        '''
        list1=df[edit_col].to_list()
        result=[]
        for l in list1:
            r=l.split(split_value)[split_keep_loc]
            result.append(r)
        if show==True:
            print('Result list values: %s'%list(set(result)))
            print('Result length: %s \n'%len(result))
        else:
            pass
        return(result)
    def col_add(df, input_list, col_name):
        df[col_name]=input_list
        return df
    def col_extract(df, i):
        '''
        FORMERLY EXTRACT_COL from DATA.PY
        Extracts an entire column of int/float data from dataframe,
        Returned as np.array.

        Parameters
        ----------
        df : DataFrame, int/float data column
            Dataframe containing column to extract as a list.
        i : integer
            Column location numerical value.

        Returns
        -------
        r : Array list, selected column data
        '''
        r=np.array(df.iloc[:,i])
        return r






        