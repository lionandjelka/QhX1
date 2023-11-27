# data_manager.py
import numpy as np
import pandas as pd
from sqlalchemy.engine import URL
from sqlalchemy.engine import create_engine
import matplotlib.pyplot as plt
import scipy
from scipy.optimize import curve_fit
from scipy.optimize import OptimizeWarning
from dateutil.relativedelta import relativedelta
import warnings
from itertools import groupby
import pyarrow as pa
import pyarrow.parquet as pq
class DataManager:
    def __init__(self):
        self.fs_df = None
        self.fs_gp = None
        self.object_df = None
        self.td_objects = None

    def load_fs_df(self, path_source):
        """
        Load forced source data from a file.
        """
        try:
            self.fs_df = pd.read_parquet(path_source)
            print("Forced source data loaded successfully.")
            return self.fs_df  # Return the loaded DataFrame
        except Exception as e:
            print(f"Error loading fs_df: {e}")
            return None  # Return None in case of an error

    def group_fs_df(self):
        """
        Group forced source data by object ID.
        """
        if self.fs_df is not None:
            self.fs_gp = self.fs_df.groupby('objectId')
            print("Forced source data grouped successfully.")
            return self.fs_gp  # Return the grouped DataFrame
        else:
            print("fs_df is not available for grouping.")
            return None  # Return None if fs_df is not available

    def load_object_df(self, path_obj):
        """
        Load object data and filter for time-domain objects.
        """
        try:
            self.object_df = pd.read_parquet(path_obj)
            lc_cols = [col for col in self.object_df.columns if 'Periodic' in col]
            self.td_objects = self.object_df.dropna(subset=lc_cols, how='all').copy()
            print("Object data loaded and processed successfully.")
            return self.td_objects  # Return the filtered DataFrame
        except Exception as e:
            print(f"Error loading object_df: {e}")
            return None  # Return None in case of an error
            
    def get_qso(self, set11):
        """
        Get QSOs with complete u,g,r,i light curves with at least 100 points.
        """
        sett = []
        for set1 in set11:
            if str(set1) in self.fs_gp.groups:
                demo_lc = self.fs_gp.get_group(str(set1))
                if all(len(demo_lc[demo_lc['filter'] == f].dropna()) >= 100 for f in range(1, 5)):
                    sett.append(str(set1))
        return sett
# Example usage:
# dm = DataManager()
# dm.load_fs_df('path_to_fs_df.parquet')
# dm.group_fs_df()
# object_ids = ['id1', 'id2', ...]  # Example object IDs
# quasar_ids = dm.get_qso(object_ids)
