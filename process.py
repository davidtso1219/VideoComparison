import cv2

from MyTypes import Frame
from utils import correct_fisheye_distortion, get_monitor


def process_target(target: Frame) -> Frame:

    # Step 1: Gray Transform
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

    return target

def process_expected(expected: Frame) -> Frame:

    # Step 1: Correct fisheye distortion
    expected = correct_fisheye_distortion(expected)

    # Step 2: Get the monitor
    expected = get_monitor(expected)

    # Step 3: Gray Transform
    expected = cv2.cvtColor(expected, cv2.COLOR_BGR2GRAY)

    return expected