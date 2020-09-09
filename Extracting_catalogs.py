

from astroquery.vizier import Vizier

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


def check_dataframe_Simbad_list(dataframe_to_study, stars_dataframe, compare_list,
                             time_pause = 60, n_step = 300):

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

    index_new_dataframe = [None]*len(dataframe_to_study)

    count_orig = 0

    for index_star in range(len(dataframe_to_study)):
        result_table = Simbad.query_objectids(stars_dataframe[index_star])
        print(count_orig)
        if result_table != None:
            names_star_Simbad = result_table['ID']
            first_name = names_star_Simbad[0]
            count_original_dataframe = 0
            for simbad_name in compare_list:
                if first_name == simbad_name[0]:
                    index_new_dataframe[count_orig] = (count_original_dataframe)
                count_original_dataframe += 1

        else:
            continue

        if count_orig%n_step == 0:
            time.sleep(time_pause)

        count_orig += 1

    return index_new_dataframe

dataframe_Vardan_2012 = pd.read_csv("Catalogs/result_J-A+A-545-A32-table45.csv")

print(dataframe_Vardan_2012)
