import pandas as pd
import logging

class DataManager:
    """
    A class for managing and processing astronomical data sets.

    This class provides methods to load and process forced source data and object data, 
    specifically focusing on time-domain objects and quasars.

    Attributes
    ----------
    fs_df : pd.DataFrame or None
        DataFrame containing forced source data.
    fs_gp : pd.core.groupby.DataFrameGroupBy or None
        GroupBy object with forced source data grouped by object ID.
    object_df : pd.DataFrame or None
        DataFrame containing object data.
    td_objects : pd.DataFrame or None
        DataFrame containing time-domain objects.
    """

    def __init__(self):
        """
        Initializes the DataManager with empty data attributes.
        """
        self.fs_df = None
        self.fs_gp = None
        self.object_df = None
        self.td_objects = None

    def load_fs_df(self, path_source: str) -> pd.DataFrame:
        """
        Load forced source data from a file.

        Parameters
        ----------
        path_source : str
            The path to the source data file.

        Returns
        -------
        pd.DataFrame or None
            The loaded DataFrame or None in case of an error.

        Examples
        --------
        >>> dm = DataManager()
        >>> dm.load_fs_df('path_to_fs_df.parquet')
        Forced source data loaded successfully.
        """
        try:
            self.fs_df = pd.read_parquet(path_source)
            logging.info("Forced source data loaded successfully.")
            return self.fs_df
        except Exception as e:
            logging.error(f"Error loading fs_df: {e}")
            return None

    def group_fs_df(self) -> pd.core.groupby.DataFrameGroupBy:
        """
        Group forced source data by object ID.

        Returns
        -------
        pd.core.groupby.DataFrameGroupBy or None
            The grouped DataFrame or None if fs_df is not available.

        Examples
        --------
        >>> dm = DataManager()
        >>> dm.load_fs_df('path_to_fs_df.parquet')
        >>> dm.group_fs_df()
        Forced source data grouped successfully.
        """
        if self.fs_df is not None and self.fs_gp is None:
            self.fs_gp = self.fs_df.groupby('objectId')
            logging.info("Forced source data grouped successfully.")
            return self.fs_gp
        else:
            logging.warning("fs_df is not available for grouping.")
            return None

    def load_object_df(self, path_obj: str) -> pd.DataFrame:
        """
        Load object data and filter for time-domain objects.

        Parameters
        ----------
        path_obj : str
            The path to the object data file.

        Returns
        -------
        pd.DataFrame or None
            The filtered DataFrame or None in case of an error.

        Examples
        --------
        >>> dm = DataManager()
        >>> dm.load_object_df('path_to_object_df.parquet')
        Object data loaded and processed successfully.
        """
        try:
            self.object_df = pd.read_parquet(path_obj)
            lc_cols = [col for col in self.object_df.columns if 'Periodic' in col]
            self.td_objects = self.object_df.dropna(subset=lc_cols, how='all').copy()
            logging.info("Object data loaded and processed successfully.")
            return self.td_objects
        except Exception as e:
            logging.error(f"Error loading object_df: {e}")
            return None

    def get_qso(self, object_ids: list, min_points: int = 100) -> list:
        """
        Get QSOs with complete u,g,r,i light curves with at least 'min_points' points.

        Parameters
        ----------
        object_ids : list
            List of object IDs to check.
        min_points : int, optional
            Minimum number of points required in each light curve (default is 100).

        Returns
        -------
        list
            List of QSO IDs that meet the criteria.

        Examples
        --------
        >>> dm = DataManager()
        >>> dm.load_fs_df('path_to_fs_df.parquet')
        >>> dm.group_fs_df()
        >>> dm.load_object_df('path_to_object_df.parquet')
        >>> object_ids = ['id1', 'id2', 'id3']
        >>> quasar_ids = dm.get_qso(object_ids)
        """
        valid_qsos = []
        for obj_id in object_ids:
            if obj_id in self.fs_gp.groups:
                demo_lc = self.fs_gp.get_group(obj_id)
                if all(len(demo_lc[demo_lc['filter'] == f].dropna()) >= min_points for f in range(1, 5)):
                    valid_qsos.append(obj_id)
        return valid_qsos

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Example usage:
# dm = DataManager()
# dm.load_fs_df('path_to_fs_df.parquet')
# dm.group_fs_df()
# dm.load_object_df('path_to_object_df.parquet')
# object_ids = ['id1', 'id2', ...]  # Example object IDs
# quasar_ids = dm.get_qso(object_ids)
