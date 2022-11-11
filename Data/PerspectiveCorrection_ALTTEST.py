##################################
# Retrofitting Persp. Correction #
#     SENSEable Design Lab       #
##################################
# v1.0
# 2/12/2021
##################################
# EXP: 'python PerspectiveCorrection.py'
##################################
# Authors: 
# Sermarini
# Kider
##################################

import sys
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Undistorter import undistort

image_directory = "Camera/Perspective/Test/"

color = (0, 0, 255)

warp_window = "Display"
undistorted_image = None
image = None
corners = [] #[(x1, y1), (x2, y2), ...]
corners_images = []

def swapPositions(list, pos1, pos2):
     
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

def shi_tomashi(image):
    """
    Use Shi-Tomashi algorithm to detect corners

    Args:
        image: np.array

    Returns:
        corners: list

    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    corners = cv2.goodFeaturesToTrack(gray, 4, 0.01, 100)
    corners = np.int0(corners)
    corners = sorted(np.concatenate(corners).tolist())
    
    corners = swapPositions(corners,0,1)
    corners = swapPositions(corners,1,2)
    print('\nThe corner points are...\n')


    im = image.copy()
    for index, c in enumerate(corners):
        x, y = c
        cv2.circle(im, (x, y), 3, 255, -1)
        character = chr(65 + index)
        print(character, ':', c)
        cv2.putText(im, character, tuple(c), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

    plt.imshow(im)
    plt.title('Corner Detection: Shi-Tomashi')
    plt.show()
    return corners


def get_destination_points(corners):
    """
    -Get destination points from corners of warped images
    -Approximating height and width of the rectangle: we take maximum of the 2 widths and 2 heights

    Args:
        corners: list

    Returns:
        destination_corners: list
        height: int
        width: int

    """

    w1 = np.sqrt((corners[0][0] - corners[1][0]) ** 2 + (corners[0][1] - corners[1][1]) ** 2)
    w2 = np.sqrt((corners[2][0] - corners[3][0]) ** 2 + (corners[2][1] - corners[3][1]) ** 2)
    w = max(int(w1), int(w2))

    h1 = np.sqrt((corners[0][0] - corners[2][0]) ** 2 + (corners[0][1] - corners[2][1]) ** 2)
    h2 = np.sqrt((corners[1][0] - corners[3][0]) ** 2 + (corners[1][1] - corners[3][1]) ** 2)
    h = max(int(h1), int(h2))

    destination_corners = np.float32([(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)])

    print('\nThe destination points are: \n')
    for index, c in enumerate(destination_corners):
        character = chr(65 + index) + "'"
        print(character, ':', c)

    print('\nThe approximated height and width of the original image is: \n', (h, w))
    return destination_corners, h, w


def unwarp_whole(img, src, dst):
    """

    Args:
        img: np.array
        src: list
        dst: list

    Returns:
        un_warped: np.array

    """
    h, w = img.shape[:2]
    H, _ = cv2.findHomography(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    print('\nThe homography matrix is: \n', H)

    t = [int(h/2),int(w/2)]
    Ht = np.array([[1,0,t[0]],[0,1,t[1]],[0,0,1]]) # translate
    H=Ht.dot(H)

    un_warped = cv2.warpPerspective(img, H, (w+t[0], h+t[1]), flags=cv2.INTER_LINEAR)
    cv2.imwrite(image_directory + "j1_undistorted.png", un_warped)

    # plot

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    # f.subplots_adjust(hspace=.2, wspace=.05)
    ax1.imshow(img)
    ax1.set_title('Original Image')

    x = [src[0][0], src[2][0], src[3][0], src[1][0], src[0][0]]
    y = [src[0][1], src[2][1], src[3][1], src[1][1], src[0][1]]

    ax2.imshow(img)
    ax2.plot(x, y, color='yellow', linewidth=3)
    ax2.set_ylim([h, 0])
    ax2.set_xlim([0, w])
    ax2.set_title('Target Area')

    plt.show()
    return un_warped



def unwarp(img, src, dst):
    """

    Args:
        img: np.array
        src: list
        dst: list

    Returns:
        un_warped: np.array

    """
    h, w = img.shape[:2]
    H, _ = cv2.findHomography(src, dst, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    print('\nThe homography matrix is: \n', H)
    un_warped = cv2.warpPerspective(img, H, (w, h), flags=cv2.INTER_LINEAR)
    return un_warped



def example_one():
    """
    Skew correction using homography and corner detection using Shi-Tomashi corner detector

    Returns: None

    """
    image = cv2.imread(image_directory + 'j1.png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.title('Original Image')
    plt.show()

    corners = shi_tomashi(image)
    destination, h, w = get_destination_points(corners)
    un_warped_whole = unwarp_whole(image, np.float32(corners), destination)
    un_warped = unwarp(image, np.float32(corners), destination)
    cropped = un_warped[0:h, 0:w]

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), facecolor='w', edgecolor='k')
    # f.subplots_adjust(hspace=.2, wspace=.05)

    ax1.imshow(un_warped_whole)
    ax2.imshow(cropped)

    plt.show()


def apply_filter(image):
    """
    Define a 5X5 kernel and apply the filter to gray scale image
    Args:
        image: np.array

    Returns:
        filtered: np.array

    """
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    kernel = np.ones((5, 5), np.float32) / 15
    filtered = cv2.filter2D(gray, -1, kernel)
    plt.imshow(cv2.cvtColor(filtered, cv2.COLOR_BGR2RGB))
    plt.title('Filtered Image')
    plt.show()
    return filtered

def apply_threshold(filtered):
    """
    Apply OTSU threshold

    Args:
        filtered: np.array

    Returns:
        thresh: np.array

    """
    ret, thresh = cv2.threshold(filtered, 250, 255, cv2.THRESH_OTSU)
    plt.imshow(cv2.cvtColor(thresh, cv2.COLOR_BGR2RGB))
    plt.title('After applying OTSU threshold')
    plt.show()
    return thresh

def detect_contour(img, image_shape):
    """

    Args:
        img: np.array()
        image_shape: tuple

    Returns:
        canvas: np.array()
        cnt: list

    """
    canvas = np.zeros(image_shape, np.uint8)
    contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    cnt = sorted(contours, key=cv2.contourArea, reverse=True)[0]
    cv2.drawContours(canvas, cnt, -1, (0, 255, 255), 3)
    plt.title('Largest Contour')
    plt.imshow(canvas)
    plt.show()

    return canvas, cnt

def detect_corners_from_contour(canvas, cnt):
    """
    Detecting corner points form contours using cv2.approxPolyDP()
    Args:
        canvas: np.array()
        cnt: list

    Returns:
        approx_corners: list

    """
    epsilon = 0.02 * cv2.arcLength(cnt, True)
    approx_corners = cv2.approxPolyDP(cnt, epsilon, True)
    cv2.drawContours(canvas, approx_corners, -1, (255, 255, 0), 10)
    approx_corners = sorted(np.concatenate(approx_corners).tolist())
    print('\nThe corner points are ...\n')
    for index, c in enumerate(approx_corners):
        character = chr(65 + index)
        print(character, ':', c)
        cv2.putText(canvas, character, tuple(c), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Rearranging the order of the corner points
    approx_corners = [approx_corners[i] for i in [0, 2, 1, 3]]

    plt.imshow(canvas)
    plt.title('Corner Points: Douglas-Peucker')
    plt.show()
    return approx_corners

def example_two():
    """
    Skew correction using homography and corner detection using contour points
    Returns: None

    """
    image = cv2.imread(image_directory + 'example_2.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.title('Original Image')
    plt.show()

    filtered_image = apply_filter(image)
    threshold_image = apply_threshold(filtered_image)

    cnv, largest_contour = detect_contour(threshold_image, image.shape)
    corners = detect_corners_from_contour(cnv, largest_contour)

    destination_points, h, w = get_destination_points(corners)
    un_warped = unwarp(image, np.float32(corners), destination_points)

    cropped = un_warped[0:h, 0:w]
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    # f.subplots_adjust(hspace=.2, wspace=.05)
    ax1.imshow(un_warped)
    ax2.imshow(cropped)

    plt.show()


def example_wall_img():
    """
    Skew correction using homography and corner detection using contour points
    Returns: None

    """
    image = cv2.imread(image_directory + 'DSC_3073_Undistorted_Cropped.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.title('Original Image')
    plt.show()

    filtered_image = apply_filter(image)
    threshold_image = apply_threshold(filtered_image)

    cnv, largest_contour = detect_contour(threshold_image, image.shape)
    corners = detect_corners_from_contour(cnv, largest_contour)

    destination_points, h, w = get_destination_points(corners)
    un_warped = unwarp(image, np.float32(corners), destination_points)

    cropped = un_warped[0:h, 0:w]
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    # f.subplots_adjust(hspace=.2, wspace=.05)
    ax1.imshow(un_warped)
    ax2.imshow(cropped)

    plt.show()

# https://stackoverflow.com/questions/35180764/opencv-python-image-too-big-to-display
def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)

# https://www.geeksforgeeks.org/displaying-the-coordinates-of-the-points-clicked-on-the-image-using-python-opencv/
def click_event_perspective_corners(event, x, y, flags, params):
    # Add corner
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(corners) < 4:
            print("Adding corner...")
            # Copy previous corner image
            if len(corners) == 0:
                marked_image = image.copy()
            else:
                marked_image = corners_images[len(corners_images) - 1].copy()
            # Add data to corners list
            corners.append((x,y))
            # Add text and dot
            marked_image = cv2.circle(marked_image, (x,y), 2, color, 2)
            marked_image = cv2.putText(marked_image, str(len(corners)), (x + 5,y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
            corners_images.append(marked_image)
            # Show updated image
            cv2.imshow(warp_window, marked_image)
            print(corners)
    # Remove corner
    if event == cv2.EVENT_RBUTTONDOWN:
        if len(corners) > 0: # Otherwise there's nothing to undo
            print("Undoing last corner...")
            corners_images.pop()
            corners.pop()
            print(corners)
            # Show previous image
            if len(corners) != 0: # put previous marked image
                cv2.imshow(warp_window, corners_images[len(corners_images) - 1])
            else: # Put back original
                cv2.imshow(warp_window, image)

if __name__ == '__main__':
    #example_one()
    #example_two()
    #example_wall_img()

    '''
        Open original image
        Use undistorer script to remove lens distortion from original picture if needed
    '''
    assert os.path.exists(sys.argv[1]), "Error: File " + sys.argv[1] + " not found."
    # Read and open image
    if not "_Undistorted" in sys.argv[1]: # Need to undistort image first
        print("Image requires camera lens distortion removal. Initiating...") 
        undistort(sys.argv[1])
        image_name = sys.argv[1][:-4] + "_Undistorted.jpg"
        undistorted_image = cv2.imread(image_name, 1)
        print("Opening undistorted " + image_name + "...")
    else:
        image_name = sys.argv[1]
        undistorted_image = cv2.imread(image_name, 1)
        print("No undistortion required. Opening " + image_name + "...")
    #undistorted_image = cv2.imread("Camera\\Perspective\\Test\\DSC_3073.jpg", 1)
    height, width, _ = undistorted_image.shape

    '''
        Grab the corners of the wall (with giant rulers) to warp the image to be straight.
        Select the outlines in this order: top-left, top-right, bottom-right, bottom-left. 
    '''
    # Set up window
    image = ResizeWithAspectRatio(undistorted_image, width=1400)
    cv2.imshow(warp_window, image)
    cv2.setWindowTitle(warp_window, 'Select 4 wall corners (with giant rulers)')
    cv2.setMouseCallback(warp_window, click_event_perspective_corners)
    # Hold for mouse input
    cv2.waitKey(0)
    # If four corner points have not been selected, close
    if(len(corners) != 4):
        cv2.destroyAllWindows()
        print("ERROR: 4 corner points not selected.")
        print("Exiting program...")
        sys.exit()

    destination, h, w = get_destination_points(corners)
    un_warped_whole = unwarp_whole(image, np.float32(corners), destination)
    un_warped = unwarp(image, np.float32(corners), destination)
    cropped = un_warped[0:h, 0:w]

    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5), facecolor='w', edgecolor='k')
    # f.subplots_adjust(hspace=.2, wspace=.05)

    ax1.imshow(un_warped_whole)
    ax2.imshow(cropped)

    plt.show()


    """
    destination_points, h, w = get_destination_points(corners)
    un_warped = unwarp(image, np.float32(corners), destination_points)

    cropped = un_warped[0:h, 0:w]
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
    # f.subplots_adjust(hspace=.2, wspace=.05)
    ax1.imshow(un_warped)
    ax2.imshow(cropped)
    """

    plt.show()
