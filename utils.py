import glob
import numpy as np


from myTypes import Frame

def find_mp4_file_in_path(file_name: str, path: str) -> str:
    """
    Find the mp4 file in path that contains file
    """
    files = glob.glob(path + '*.mp4')
    for file in files:        
        if file_name in file:
            return file

    return ''


# TODO: implement this function
def correct_fisheye_distortion(img: Frame) -> Frame:
    return


# TODO: implement this function
def crop_monitor(img: Frame) -> Frame:
    return