"""
"""

import os
import re
import click
import subprocess
from loguru import logger
from src.logging import DEFAULT_LOG_LEVEL, set_logger, sniff_log_level

from src.utils import create_user_bundle, create_team_bundle, create_connection, \
    user_exists_raw, group_exists_raw, populate_hr_db_raw, db_password, clean_user_name
    

import pandas as pd

def get_groups_in_file( filename ):
    """ return list of groups in file """
    logger.debug(f"get_groups_in_file( {filename} )")
    try:
        df = pd.read_csv(filename)
        groups = sorted(list(set(df['group_name'].tolist())))
        return groups
    except FileNotFoundError:
        logger.error(f"File {filename} not found.")
        return []
    except pd.errors.EmptyDataError:
        logger.error(f"File {filename} is empty.")
        return []
    except pd.errors.ParserError:
        logger.error(f"Error parsing file {filename}.")
        return []
    except KeyError:
        logger.error(f"Column 'group_name' not found in {filename}.")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []

def get_users_in_file( filename ):
    """ return list of groups in file """
    logger.debug(f"get_users_in_file( {filename} )")
    try:
        df = pd.read_csv( filename )
        users = sorted(list(set(df['login_id'].tolist())))
        return users
    except FileNotFoundError:
        logger.error(f"File {filename} not found.")
        return []
    except pd.errors.EmptyDataError:
        logger.error(f"File {filename} is empty.")
        return []
    except pd.errors.ParserError:
        logger.error(f"Error parsing file {filename}.")
        return []
    except KeyError:
        logger.error(f"Column 'group_name' not found in {filename}.")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []

def get_groups_and_users_in_file( filename ):
    """ return list of group and users in file """
    logger.debug(f"get_groups_and_users_in_file( {filename} )")
    try:
        df = pd.read_csv( filename )
        bundles = []
        for i,row in df.iterrows():
            bundles.append( dict(group=row['group_name'],user=row['login_id']))
        return bundles
    except FileNotFoundError:
        logger.error(f"File {filename} not found.")
        return []
    except pd.errors.EmptyDataError:
        logger.error(f"File {filename} is empty.")
        return []
    except pd.errors.ParserError:
        logger.error(f"Error parsing file {filename}.")
        return []
    except KeyError:
        logger.error(f"Column 'group_name' not found in {filename}.")
        return []
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        return []


def get_counts_in_file( filename ):
    """ return list with various counts from file """
    counts = dict( users=len(get_users_in_file( filename)),teams=len(get_groups_in_file(filename)),pairs=len(get_groups_and_users_in_file(filename)) )
    return counts

def list_counts_in_file( filename ):
    """ list counts in file """
    status = get_counts_in_file( filename )
    for key in status.keys():
        print(f"{key}\t{status[key]}")

def list_groups_in_csv_file( filename ):
    """ list groups in file """
    groups = get_groups_in_file( filename )
    for i,group in enumerate( groups ):
        print( group+"\t"+clean_user_name(group)+ "\t" + db_password( clean_user_name(group) )  )

def list_users_in_csv_file( filename ):
    users = get_users_in_file( filename )
    for i,user in enumerate( users ):
        print( user+"\t"+clean_user_name(user)  )

def list_groups_and_users_in_csv_file( filename ):
    bundles = get_groups_and_users_in_file( filename )
    for i,bundle in enumerate( bundles ):
        print( bundle["group"] + "\t"+ bundle["user"]  )

def create_users_from_csv_file( filename ):
    users = get_users_in_file( filename )
    for i,user in enumerate( users ):
        create_user_bundle( clean_user_name(user) )

def create_groups_from_csv_file( filename ):
    groups = get_groups_in_file( filename )
    for i,group in enumerate( groups ):
        create_team_bundle( clean_user_name(group) )

def create_connections_from_csv_file( filename ):
    """ connect teams and users """
    bundles = get_groups_and_users_in_file( filename )
    for i,bundle in enumerate( bundles ):
        group_name = clean_user_name(bundle["group"])
        user_name = clean_user_name(bundle["user"])
        if not user_exists_raw( user_name):
            create_user_bundle( user_name )
        if not group_exists_raw( group_name ):
            create_team_bundle( group_name )
        create_connection( group_name, user_name )

def populate_hr_databases_from_csv_file( team_file, hr_ddl_file ):
    """ populate HR databases """
    users = get_users_in_file( team_file )
    hr_file = os.path.abspath( hr_ddl_file )
    if os.path.exists( hr_file ):
        for i,user in enumerate( users ):
            populate_hr_db_raw( clean_user_name(user), hr_data_file=hr_file )
    else:
        logger.error(f"Missing hr datafile: {hr_ddl_file}")