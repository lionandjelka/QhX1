# processing_utils.py
import QhX
from QhX.data_manager import DataManager
from QhX.light_curve import get_lctiktok, get_lc22
from QhX.calculation import periods, signif_johnson
from QhX.algorithms.wavelets.wwtz import *
from QhX.detection import process1_new


def process1_wrapper(set_id, data_manager):
    print(f"Processing setid: {set_id}")  # Using print for visibility in Google Colab
    # Call the actual process1 function
    return QhX.detection.process1_new(data_manager, set_id, ntau=80, ngrid=200, provided_minfq=500, provided_maxfq=10, include_errors=False)

def process1_caller(args):
    return process1_wrapper(*args)
