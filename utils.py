import cv2, glob, numpy as np
from typing import List, Dict

from MyTypes import Frame
from interpreter import interpreter

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


def get_monitor(img: Frame) -> Frame:
    CAMERA_HEIGHT, CAMERA_WIDTH = img.shape[0], img.shape[1]
    img_np = cv2.resize(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), (320,320))

    results = detect_objects(interpreter, img_np, 0.8)
    results.sort(key=lambda r: r['score'])

    coords = []
    bounding_box_img = []

    for result in results:
        ymin, xmin, ymax, xmax = result['bounding_box']
        # print(result['score'])
        xmin = int(max(1,xmin * CAMERA_WIDTH))
        xmax = int(min(CAMERA_WIDTH, xmax * CAMERA_WIDTH))
        ymin = int(max(1, ymin * CAMERA_HEIGHT))
        ymax = int(min(CAMERA_HEIGHT, ymax * CAMERA_HEIGHT))
        coords.append((xmin, ymin, xmax, ymax))

    print(coords)
    for c in coords:
        c = [int(n) for n in c]
        bounding_box_img.append(img[c[1]:c[3], c[0]:c[2],:])

    return bounding_box_img[0]


def set_input_tensor(interpreter, image: Frame) -> None:
    """Sets the input tensor."""
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = np.expand_dims((image - 255) / 255, axis=0)


def get_output_tensor(interpreter, index):
    """Returns the output tensor at the given index."""
    output_details = interpreter.get_output_details()[index]
    tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
    return tensor

def detect_objects(interpreter, image: Frame, threshold: float) -> List[Dict]:
    """Returns a list of detection results, each a dictionary of object info."""
    set_input_tensor(interpreter, image)
    interpreter.invoke()

    # Get all output details
    boxes = get_output_tensor(interpreter, 1)
    classes = get_output_tensor(interpreter, 3)
    scores = get_output_tensor(interpreter, 0)
    count = int(get_output_tensor(interpreter, 2))

    results = []
    for i in range(count):

        if scores[i] >= threshold:

            result = {
                'bounding_box': boxes[i],
                'class_id': classes[i],
                'score': scores[i]
            }

            results.append(result)

    return results
