import json
import cv2 as cv
import numpy as np
from PIL import Image
import json
import imutils

from websockets.sync.client import connect

# detection
def detect(resized):
    start = 40, 20
    box_size = 95, 78
    jump = 15, 10

    boxes = []

    for i in range(9):
        y, x = divmod(i, 3)
        bx = start[0] + box_size[0] * x + x * jump[0]
        by = start[1] + box_size[1] * y + y * jump[1]

        box = (bx, by, bx + box_size[0], by + box_size[1])
        boxes.append(box)



    box_images = [resized.crop(box).convert('L') for box in boxes]
    board_detect = [' '] * 9
    cannys = []

# detect
    for i, box_image in enumerate(box_images):
        box_ar = np.array(box_image)
        rows = box_ar.shape[0]
        circles = cv.HoughCircles(box_ar, cv.HOUGH_GRADIENT, 1, rows / 1,
                                   param1=100, param2= 30, #, 30,
                                   minRadius=10, maxRadius=50)
        n_circles = 0
        if circles is not None:
            n_circles = len(circles[0])
            # print(circles)

        canny = cv.Canny(box_ar, 50, 200, None, 3)
        # canny = cv.bitwise_not(box_ar)
        cannys.append(canny)
        lines = cv.HoughLinesP(
            canny, # Input edge image
            1, # Distance resolution in pixels
            np.pi/180, # Angle resolution in radians
            threshold=25, # Min number of votes for valid line
            minLineLength=10, # Min allowed length of line
            maxLineGap=35 # Max allowed gap between line for joining them
        )

        n_lines = 0
        if lines is not None:
            n_lines = len(lines)
            # print(lines)

        print(f"{i} {n_circles=} {n_lines=}")

        result = ''
        if n_circles > 0:
            result = 'O'
        elif n_lines >= 3:
            result = 'X'
        else:
            result = ' '

        board_detect[i] = result

    return board_detect

def print_detcted(board_detect):
    print(' {} | {} | {}'.format(*board_detect[:3]))
    print('---+---+---')
    print(' {} | {} | {}'.format(*board_detect[3:6]))
    print('---+---+---')
    print(' {} | {} | {}'.format(*board_detect[6:]))


DEVICE = 2
FLY_FRAMES = 30

webcam = cv.VideoCapture(DEVICE)

# skip first frames. let the webcam adjust settings
for i in range(FLY_FRAMES):
    result, src = webcam.read()

original = src.copy()
# webcam.release()

gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
#gray = cv.equalizeHist(gray)
gray = cv.medianBlur(gray, 3)


rows = gray.shape[0]

circles = cv.HoughCircles(gray, cv.HOUGH_GRADIENT, 1, rows / 8,
                           param1=100, param2= 10, #, 30,
                           minRadius=7, maxRadius=10)


# calibration
if circles is not None:
    circles = np.uint16(np.around(circles))

    det_points = circles[0, :].copy()

    # To sort by the second column of a:
    det_points = det_points[det_points[:, 0].argsort()]
    top_left, bottom_left = det_points[:2]
    top_right, bottom_right = det_points[-2:]

    if top_left[1] > bottom_left[1]:
        top_left, bottom_left = bottom_left, top_left

    if top_right[1] > bottom_right[1]:
        top_right, bottom_right = bottom_right, top_right

    # render corners
    cv.circle(src, top_left[:2], top_left[2], (255, 0, 0), 3) # red top left
    cv.circle(src, bottom_left[:2], bottom_left[2], (0, 0, 255), 3) # blue bottom left
    cv.circle(src, top_right[:2], top_right[2], (0, 255, 0), 3) # green top right
    cv.circle(src, bottom_right[:2], bottom_right[2], (255, 255, 0), 3) # yellow bottom right
    # det_points = np.sort(det_points, order=0)
    # print(det_points)
    transform_data = np.hstack([top_left[:2], bottom_left[:2], bottom_right[:2], top_right[:2]]).astype(int)

    W = 400
    H = W * 3 // 4
    img = Image.fromarray(src)
    resized = img.transform((W, H), Image.Transform.QUAD, data=transform_data)


W = 400
H = W * 3 // 4
img = Image.fromarray(gray)
resized = img.transform((W, H), Image.Transform.QUAD, data=transform_data)
background = np.array(resized)

CNT_THRESH = 60
previous = True
try:
    frame_no = 0

    while True:
        result, frame = webcam.read()
        frame_no += 1
        if frame is None or frame_no % 15:
            continue

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        gray = cv.medianBlur(gray, 3)

        img = Image.fromarray(gray)
        resized_img = img.transform((W, H), Image.Transform.QUAD, data=transform_data)
        resized = np.array(resized_img)

        frameDelta = cv.absdiff(background, resized)
        thr = cv.threshold(frameDelta, 25, 255, cv.THRESH_BINARY)[1]
        thr = cv.dilate(thr, None, iterations=2)
        cnts = cv.findContours(thr.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        motion = False
        for c in cnts:
            if cv.contourArea(c) > CNT_THRESH:
                motion = True
                break

        if previous and not motion:
            print(f'{frame_no:4d} Change detected!')
            detected_board = detect(resized_img)
            print_detcted(detected_board)

            with connect("ws://localhost:8765") as websocket:
                websocket.send(json.dumps(detected_board))

        background = resized
        previous = motion

except KeyboardInterrupt:
    print('Received Ctrl-C')

webcam.release()
