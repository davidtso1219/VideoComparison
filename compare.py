import glob, os, cv2

from MyTypes import Frame
from utils import find_mp4_file_in_path
from process import process_target, process_expected


def compare_img(target: Frame, expected: Frame) -> int:
    """Compare Two Images And Return The Similarity Score of Them

    Args:
        target (Frame): target image
        expected (Frame): expected image

    Returns:
        int: the similarity score
    """

    # process the images first
    target = process_target(target)
    expected = process_expected(expected)

    # TODO: compare the similarity of target and expected
    return 100

def compare_video(target: str, expected: str) -> int:

    # get video captures
    target_cap = cv2.VideoCapture(target)
    expected_cap = cv2.VideoCapture(expected)

    # get frame_counts
    target_frame_count = target_cap.get(cv2.CAP_PROP_FRAME_COUNT)
    expected_frame_count = expected_cap.get(cv2.CAP_PROP_FRAME_COUNT)

    scores = 0
    count = min(target_frame_count, expected_frame_count)

    # compare each frame
    for i in range(count):
        ret, target_img = target_cap.read()
        ret, expected_img = expected_cap.read()
        score = compare_img(target_img, expected_img)
        scores += score

    # release the captures
    target_cap.release()
    expected_cap.release()

    return scores / count

def compare_videos(target_path: str = './target/', expected_path: str = './expected/', threshold: int = 80) -> None:
    """
    compare videos in target_path and expected_path
    """

    # check if the paths end with the seperator
    if not target_path.endswith(os.sep):
        target_path += os.sep

    if not expected_path.endswith(os.sep):
        expected_path += os.sep

    # the the list of the mp4 files in these directories
    targets = glob.glob(target_path + '*.mp4')

    # for each target, find the corresponding expected and compare them
    for target in targets:
        name = target.split(os.sep)[-1]
        expected = find_mp4_file_in_path(name, expected_path)
        score = compare_video(target, expected)

        # if the score is less than the threshold, warn in the log
        if score < threshold:
            print(f'[log] Something is wrong with {name}')