import numpy as np
import pandas as pd
import datetime
import math
from uszipcode import SearchEngine


def find_county_and_state(zipcode):
    '''
    Function
    --------
    Takes Zipcode and returns County & State

    Parameters
    ----------
    zipcode : Zip Code to Match on

    Returns
    -------
    county : county of zipcode
    state : state of zipcode
    '''
    search = SearchEngine(simple_zipcode=True)
    result = search.by_zipcode(zipcode)
    county = result.county
    state = result.state

    return county, state

def find_zip_state(df,zipcode):
    '''
    Function
    --------
    Looks through DataFrame and returns Entries with same state

    Parameters
    ----------
    df : Pandas DataFrame of Charities
    zip_code : Zip Code to Match on

    Returns
    -------
    Pandas DataFrame with Entries matching provided state
    '''
    search = SearchEngine(simple_zipcode=True)
    state = search.by_zipcode(zipcode).state
    temp_df = df[df['STATE']==state]

    return temp_df

def find_major_category(df,category:str):
    '''
    Function
    --------
        Filter a Pandas DataFrame by an NTEE Major Category

    Parameters
    ----------
        df : Pandas DataFrame with 'NTEE_Major_Category' column
        category : NTEE Category to Filter

    Return
    ------
        Filtered Pandas DataFrame
    '''
    temp_df = df[df['NTEE_Major_Category']==category]

    return temp_df

def find_minor_category(df,category:str):
    '''
    Function
    --------
        Filter a Pandas DataFrame by an NTEE Major Category

    Parameters
    ----------
        df : Pandas DataFrame with 'NTEE_Major_Category' column
        category : NTEE Category to Filter

    Return
    ------
        Filtered Pandas DataFrame
    '''
    temp_df = df[df['NTEE_Minor_Category']==category]

    return temp_df


def search_zip_to_state_major_category(df, zipcode, category):
    '''
    Function
    --------
    Filter a Pandas DataFrame by Zip Code and NTEE Major Category

    Parameters
    ----------
    df : Pandas DataFrame with 'NTEE_Major_Category' column
    zipcode : Zipcode to Filter on
    category : NTEE Major Category to Filter on

    Return
    ------
    Filtered Pandas DataFrame
    '''
    temp_df = find_zip_state(df,zipcode)
    temp_df = find_major_category(temp_df,category)

    return temp_df

def add_score_and_sort_df(df,zipcode,zip_factor = 1,county_factor = 1,state_factor=1,top_char=3):
    '''
    Function
    --------
        ADD score column to Pandas DataFrame and return top X rated Charities by score

    Parameters
    ----------
        df : Pandas DataFrame with 'ZIP_FIVE' column
        zipcode : Zipcode to Filter on
        zip_factor : Weighting Variable for Charities with Same Zip Code
        county_factor : Weighting Variable for Charities with Same Zip Code
        state_factor : Weighting Variable for Charities with Same State
        top_char : Number of "Top" results to return sorted by score descending

    Return
    ------
        Filtered Pandas DataFrame
    '''
    search = SearchEngine(simple_zipcode=True)

    county = search.by_zipcode(zipcode).county
    state = search.by_zipcode(zipcode).state

    df['zip_factor'] = df['ZIP_FIVE'].apply(lambda x: zip_factor if int(x) == zipcode else 0)
    df['county_factor'] = df['County'].apply(lambda x: county_factor if x == county else 0)
    df['state_factor'] = df['STATE'].apply(lambda x: state_factor if x == state else 0)

    df['score'] = (df['INCOME_CD']+1)*(1+df['zip_factor']+df['county_factor']+df['state_factor'])

    temp_df = df.sort_values(by='score',ascending=False).head(top_char)

    return temp_df

def recommend_charities(df,zipcode,category,num_rec=3):
    '''
    Function
    --------
        Recommends Charities from a Given Pandas DataFrame
        Uses other functions to filter on a category and score each charity

    Parameters
    ----------
        df : Pandas DataFrame with 'ZIP_FIVE' and 'NTEE_Major_Category' columns
        zipcode : Zipcode to Filter on
        category : Category to Filter on
        top_char : Number of "Top" results to return sorted by score descending

    Return
    ------
        Filtered Pandas DataFrame with "num_rec" recommendations
    '''
    temp_df = find_major_category(df,category)

    scored_df = add_score_and_sort_df(temp_df,zipcode,top_char=num_rec)

    return scored_df
