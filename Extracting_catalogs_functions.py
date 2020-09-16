

###
### Goals
###

# Select one main catalog. Checks all other selected catalogs for similar stars
# and creats a joint dataframe with all the gathered parameters

###
### Imports
###

import pickle
import galpy
import numpy as np
import csv
import matplotlib.pyplot as plt

from astroquery.vizier import Vizier
from astroquery.simbad import Simbad

from multiprocessing import Queue, Process

import pandas as pd
import time as time

###
### Inputs
###

# Examples extracted from VizieR, check Instructions

main_catalog = 'result_J-A+A-545-A32-table45.csv'

catalogs = ['result_J-A+A-606-A94-table1.csv',
            'result_J-A+A-634-A136-table3.csv',
            'result_J-ApJ-724-154-table1.csv']



# The label corresponding to the star's list in each catalog

keyword_main_catalog = 'SimbadName'

keywords_catalogs = ['SimbadName', 'SimbadName', 'Name']

# Find it through:
# dataframe_cat = pd.read_csv('Catalogs/' + catalogs[i])
# list(dataframe_cat)

###
### General Functions
###

def Simbad_names(star_names, time_pause = 60, n_step = 402):
    """ Converts list of star names to the Simbad ID of each star. Useful for
    comparision with same stars written in different ways.

    Args
    ----------
	star_names: List of stars
	time_pause: Time to pause every number of n_step to avoid query problems from Simbad
    n_step: Number of star evalueted before stopping to avoid crashing Simbad's query

    Returns
    ----------
	Simbad ID's for a list of stars
    """

    all_names_my_stars = []

    count = 1

    for star in star_names:
        result_table = Simbad.query_objectids(star)
        if result_table != None:
            names_star_Simbad = result_table['ID']
            all_names_my_stars.append(names_star_Simbad)
        else:
            pass

        if count%n_step == 0:
            time.sleep(time_pause)

        #print_progress(count, len(star_names)-1, prefix='Progress:', suffix='Complete', decimals=1, bar_length=100)
        count += 1

    return(all_names_my_stars)


def check_dataframe_Simbad_list(dataframe_cat, stars_dataframe_cat, compare_Simbad,
                             time_pause = 60, n_step = 300):

    """ Checks correspondence between in stars between two dataframes

    Args
    ----------
	dataframe_cat: List of stars
	stars_dataframe_cat: Time to pause every number of n_step to avoid query
    problems from Simbad
    compare_Simbad: List of Simbad ID stars (from previous catalog) that I want
    to match
    time_pause: Time to pause every number of n_step to avoid query problems from Simbad
    n_step: Number of star evalueted before stopping to avoid crashing Simbad's query

    Returns
    ----------
	Simbad ID's for a list of stars
    """

    index_new_dataframe = [None]*len(dataframe_cat)

    count_orig = 0

    for index_star in range(len(dataframe_cat)):
        result_table = Simbad.query_objectids(stars_dataframe_cat[index_star])
        #print(count_orig)
        if result_table != None:
            names_star_Simbad = result_table['ID']
            first_name = names_star_Simbad[0]
            count_original_dataframe = 0
            for simbad_name in compare_Simbad:
                if first_name == simbad_name[0]:
                    index_new_dataframe[count_orig] = (count_original_dataframe)
                count_original_dataframe += 1

        else:
            continue

        if count_orig%n_step == 0:
            time.sleep(time_pause)

        count_orig += 1

    return index_new_dataframe
