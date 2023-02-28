##################################
# Retrofitting Persp. Correction #
#     SENSEable Design Lab       #
##################################
# v1.0
# 2/21/2021
##################################
# EXP: 'python PerspectiveCorrection.py full_file_path'
##################################
# Authors: 
# Sermarini
# Kider
##################################

'''
    1.
        Select outer edges of ruler/wall combo. Make it a tight fit
    2.
        Mark the dimensions of the wall using the 0 inch and 60 inch ruler markers
    3.
        Mark the cutout wall areas using triangles or rectangles. Triangles seem more accurate
'''

import sys
import os
import cv2
import numpy as np
import math
from Undistorter import undistort

DEBUG_EDGES = False
DEBUG_DIMENSIONS = False
DEBUG_AREA = False

color = (0, 0, 255)

warp_window = "Display"
undistorted_image = None
image = None
corners = [] #[(x1, y1), (x2, y2), ...]
corners_images = []

dimension_window = "Dimensions"
wall_dimensions = [] #[min x (pixel), max x (pixel), min y (pixel), max y (pixel)]
dimensions_images = []

area_window = "Area"
areas = [] # [[vertex 1, vertex 2, vertex 3], [vertex 1, vertex 2, vertex 3, vertex 4]] Can be triangles or rectangles 
area_images = []


def reset():
    global undistorted_image
    global image
    global corners
    global corners_images
    global wall_dimensions
    global dimensions_images
    global areas
    global area_images
    global warped

    undistorted_image = None
    image = None
    corners = []
    corners_images = []

    wall_dimensions = []
    dimensions_images = []

    areas = []
    area_images = []

    warped = None


# https://pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
def order_points(pts):
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype = "float32")
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect

# https://pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
def four_point_transform(image, pts):
    # obtain a consistent order of the points and unpack them
    # individually
    rect = order_points(pts)
    (tl, tr, br, bl) = rect
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    # return the warped image
    return warped

# LEGACY
def rectangle_boundaries(points):
    minimum_x = 1000000
    maximum_x = -1
    minimum_y = 1000000
    maximum_y = -1
    for point in points:
        minimum_x = min(point[0], minimum_x)
        maximum_x = max(point[0], maximum_x)
        minimum_y = min(point[1], minimum_y)
        maximum_y = max(point[1], maximum_y)
    top_left = [minimum_x, minimum_y]
    bottom_right = [maximum_x, maximum_y]
    return top_left, bottom_right

def distance_between_two_points(A, B):
    x1 = A[0]
    x2 = B[0]
    y1 = A[1]
    y2 = B[1]
    return abs(math.sqrt((x2-x1)**2 + (y2-y1)**2))

# Pass in 4 vertices and solve using Bretschneider's formula
# https://en.wikipedia.org/wiki/Bretschneider%27s_formula
# https://proofwiki.org/wiki/Bretschneider's_Formula forumla gives a lower number than ^^^
def quadrilateral_area(A, B, C, D):
    # Method 1 - https://en.wikipedia.org/wiki/Bretschneider%27s_formula
    """
    a = distance_between_two_points(A, B)
    b = distance_between_two_points(C, B)
    c = distance_between_two_points(C, D)
    d = distance_between_two_points(A, D)
    s = (a + b + c + d) / 2.0
    A = np.array(A)
    B = np.array(B)
    C = np.array(C)
    D = np.array(D)
    a_vector = B - A
    d_vector = D - A
    c_vector = D - C
    b_vector = B - C
    # https://manivannan-ai.medium.com/find-the-angle-between-three-points-from-2d-using-python-348c513e2cd
    alpha = np.arccos(np.dot(a_vector, d_vector) / (np.linalg.norm(a_vector) * np.linalg.norm(d_vector)))
    gamma = np.arccos(np.dot(c_vector, b_vector) / (np.linalg.norm(c_vector) * np.linalg.norm(b_vector)))
    area = math.sqrt((s-a)*(s-b)*(s-c)*(s-d)-0.5*(a*b*c*d)*math.cos(alpha + gamma))
    """

    # Method 2 - https://proofwiki.org/wiki/Bretschneider's_Formula
    '''
    a = distance_between_two_points(A, D)
    b = distance_between_two_points(A, B)
    c = distance_between_two_points(C, B)
    d = distance_between_two_points(D, C)
    s = (a + b + c + d) / 2.0
    e = distance_between_two_points(D, B)
    alpha = math.acos((a**2 + b**2 - e**2) / (2*a*b))
    gamma = math.acos((d**2 + c**2 - e**2) / (2*d*c))
    area = math.sqrt((s-a)*(s-b)*(s-c)*(s-d) - a*b*c*d * (math.cos((alpha + gamma)/2)**2))
    '''

    # Method 3 (It's method 1 with a bug fixed I think) - https://en.wikipedia.org/wiki/Bretschneider%27s_formula
    a = distance_between_two_points(A, B)
    b = distance_between_two_points(C, B)
    c = distance_between_two_points(C, D)
    d = distance_between_two_points(A, D)
    f = distance_between_two_points(B, D)
    s = (a + b + c + d) / 2.0
    alpha = math.acos((d**2 + a**2 - f**2) / (2*a*d))
    gamma = math.acos((c**2 + b**2 - f**2) / (2*c*b))
    area = math.sqrt((s-a)*(s-b)*(s-c)*(s-d) - 0.5*(a*b*c*d)*(1 + math.cos(alpha + gamma)))   
    
    #print(np.degrees(alpha))
    #print(np.degrees(gamma))
    return area

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
            marked_image = cv2.putText(marked_image, str(len(corners)), (x + 5,y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
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

def click_event_wall_dimensions(event, x, y, flags, params):
    # Add dimension
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(wall_dimensions) < 4:
            print("Adding dimension...")
            # Copy previous image
            if len(wall_dimensions) == 0:
                marked_image = warped.copy()
            else:
                marked_image = dimensions_images[len(dimensions_images) - 1].copy()
            # Add data to dimensions list
            line_start = None
            line_end = None
            line_text = ""
            image_height = marked_image.shape[0]
            image_width = marked_image.shape[1]
            # TODO SET DIMENSIONS
            if len(wall_dimensions) == 0: # X min
                wall_dimensions.append(x)
                line_start = (x, 0)
                line_end = (x, image_height)
                line_text = "X-Left"
            elif len(wall_dimensions) == 1: # X max
                wall_dimensions.append(x)
                line_start = (x, 0)
                line_end = (x, image_height)
                line_text = "X-Right"
            elif len(wall_dimensions) == 2: # Y min
                wall_dimensions.append(y)
                line_start = (0, y)
                line_end = (image_width, y)
                line_text = "Y-Bottom"
            elif len(wall_dimensions) == 3: # Y max
                wall_dimensions.append(y)
                line_start = (0, y)
                line_end = (image_width, y)
                line_text = "Y-Top"
            # Add text and line
            marked_image = cv2.line(marked_image, line_start, line_end, color, 1)
            marked_image = cv2.putText(marked_image, line_text, (x + 5,y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
            dimensions_images.append(marked_image)
            # Show updated image
            cv2.imshow(dimension_window, marked_image)
            print(wall_dimensions)
    # Remove dimension
    if event == cv2.EVENT_RBUTTONDOWN:
        if len(wall_dimensions) > 0: # Otherwise there's nothing to undo
            print("Undoing last dimension...")
            dimensions_images.pop()
            wall_dimensions.pop()
            print(wall_dimensions)
            # Show previous image
            if len(wall_dimensions) != 0: # put previous marked image
                cv2.imshow(dimension_window, dimensions_images[len(dimensions_images) - 1])
            else: # Put back original
                cv2.imshow(dimension_window, warped)

def click_event_area(event, x, y, flags, params):
    # Add corner
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get current shape
        if len(areas) == 0:
            areas.append([])
        current_shape = areas[len(areas) - 1]
        if len(current_shape) < 4: # Max shape size is 4 corners
            print("Adding Area position...")
            # Copy previous corner image
            if len(area_images) == 0: # Get default, no shapes in memory
                marked_image = warped.copy()
            #if len(current_shape) == 0:
                #marked_image = warped.copy()
            else:
                marked_image = area_images[len(area_images) - 1].copy()
            # Add data to corners list
            areas[len(areas) - 1].append((x,y))
            # Add text and dot
            marked_image = cv2.circle(marked_image, (x,y), 2, color, 2)
            marked_image = cv2.putText(marked_image, str(len(areas[len(areas) - 1])), (x + 5,y - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
            area_images.append(marked_image)
            # Show updated image
            cv2.imshow(area_window, marked_image)
            print(areas)
    # Remove corner
    if event == cv2.EVENT_RBUTTONDOWN:
        if len(areas) == 0: # No points have been added yet
            return
        if len(areas[len(areas) - 1]) > 0: # Otherwise there's nothing to undo
            print("Undoing last Area position...")
            area_images.pop()
            areas[len(areas) - 1].pop()
            if len(area_images) != 0:
                cv2.imshow(area_window, area_images[len(area_images) - 1])
            else:
                cv2.imshow(area_window, warped)
            # Whole shape now empty so get rid of the empty list
            #if len(areas[len(areas) - 1]) == 0:
            #    areas.pop()
            print(areas)
    # "Lock in" the shape
    if event == cv2.EVENT_MBUTTONDOWN:
        # Check if shape can be made
        if len(areas) == 0: # No points have been added yet
            return
        if len(areas[len(areas) - 1]) < 3: # not enough points to make a shape
            return
        # Get base image to draw on top of
        shape = areas[len(areas) - 1]
        shape_length = len(shape)
        if ((len(area_images) - shape_length)) == 0: # Replace with blank image
            marked_image = warped
        else: # Replace with previous image
            marked_image = area_images[(len(area_images) - shape_length) - 1]
        # Draw shape to window
        if shape_length == 3: # Triangle
            marked_image = cv2.drawContours(marked_image, [np.array(shape)], 0, color, -1)
        else: # Rectangle
            marked_image = cv2.drawContours(marked_image, [np.array(shape)], 0, color, -1)
            #top_left, bottom_right = rectangle_boundaries(shape)
            #marked_image = cv2.rectangle(marked_image, top_left, bottom_right, color, -1)
        cv2.imshow(area_window, marked_image)
        # Prepare for next left click
        areas.append([])
        area_images.append(marked_image) 
        print(areas)

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

def calculate_area(image_name):
    global image
    global warped
    reset()

    undistorted_image = cv2.imread(image_name, 1)
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
    # Warp image for proper perspective
    pts = np.array(corners, dtype = "float32")
    warped = four_point_transform(image, pts)

    '''
        Select the wall outlines by adding lines to the x minimum, x maximum, y minimum, and y maximum
    '''
    # Set up window
    cv2.imshow(dimension_window, warped)
    cv2.setWindowTitle(dimension_window, 'Select Wall dimension outlines')
    cv2.setMouseCallback(dimension_window, click_event_wall_dimensions)
    # Hold for mouse input
    cv2.waitKey(0)
    # If wall dimensions have not been selected, close
    if(len(wall_dimensions) != 4):
        cv2.destroyAllWindows()
        print("ERROR: 4 wall dimensions not selected.")
        print("Exiting program...")
        sys.exit()

    '''
        Draw out the area of the cutout sections
    '''
    # cv.rectangle(img,(384,0),(510,128),(0,255,0),3)
    # Set up window
    cv2.imshow(area_window, warped)
    cv2.setWindowTitle(area_window, 'Draw out cut-out area of wall')
    cv2.setMouseCallback(area_window, click_event_area)
    # Hold for mouse input
    cv2.waitKey(0)

    '''
        Calculate the area in inches using the dimensions and area data
    '''
    width_inches = 60.0
    height_inches = 60.0
    wall_area_inches = width_inches * height_inches
    width_pixles = wall_dimensions[1] - wall_dimensions[0]
    height_pixels = wall_dimensions[2] - wall_dimensions[3]
    wall_area_pixels = width_pixles * height_pixels
    pixles_per_inch = wall_area_pixels / wall_area_inches
    print("========== Dimensions ==========")
    print("Wall width (inches):", width_inches)
    print("Wall height (inches):", height_inches)
    print("Wall width (pixels):", width_pixles)
    print("Wall height (pixels):", height_pixels)
    print("Wall area (pixels):", wall_area_pixels)
    print("Pixels per inch:", pixles_per_inch)
    print("============ Shapes ============")
    # Total area of cut out sections
    cutout_area = 0
    for shape in areas:
        if len(shape) == 3: # Triangle
            print("Triangle")
            a = shape[0]
            b = shape[1]
            c = shape[2]
            area = 0.5 * ((b[0]-a[0])*(c[1]-a[1])-(c[0]-a[0])*(b[1]-a[1]))
            cutout_area = cutout_area + abs(area)
        elif len(shape) == 4: # Rectangle
            print("Rectangle")
            '''
            top_left, bottom_right = rectangle_boundaries(shape)
            width = bottom_right[0] - top_left[0]
            height = top_left[1] - bottom_right[1]
            # Get area
            area = width * height
            cutout_area = cutout_area + abs(area)
            print("Top left vertex (pixels):", top_left)
            print("Bottom right vertex (pixels):", bottom_right)
            print("Width (pixels):", width)
            print("Width (inches):", width / pixles_per_inch)
            print("Height (pixels):", height)
            print("Height (inches):", height / pixles_per_inch)
            print("Area (pixels):", area)
            print("Area (inches):", area / pixles_per_inch)
            print("Total cutout area so far:", cutout_area)
            '''
            a = shape[0]
            b = shape[1]
            c = shape[2]
            d = shape[3]
            area = quadrilateral_area(a, b, c, d)
            cutout_area = cutout_area + abs(area)
            print("Area (pixels):", area)
            print("Area (inches):", area / pixles_per_inch)
    print("============= Area =============")
    print("Cutout area (pixles):", cutout_area)
    print("Cutout area (inch):", (cutout_area / pixles_per_inch))

    cv2.destroyAllWindows()

    # Total cutout area in pixels and inches
    return cutout_area, (cutout_area / pixles_per_inch),


if __name__ == '__main__':
    """
    # Set debug values for an easier time getting to what I need to get to
    if DEBUG_EDGES:
        print("RUNNING WITH DEBUG PRESET CORNERS")
        corners = [(382, 134), (1144, 124), (1157, 901), (380, 891)]
    if DEBUG_DIMENSIONS:
        print("RUNNING WITH DEBUG PRESET DIMENSIONS")
        wall_dimensions = [50, 756, 775, 35]
    if DEBUG_AREA:
        print("RUNNING WITH DEBUG PRESET CUTOUT AREA")
        areas = [[(564, 566), (565, 494), (614,491), (614, 564)], []]
    """

    '''
        Open original image
        Use undistorer script to remove lens distortion from original picture if needed
    '''
    assert os.path.exists(sys.argv[1]), "Error: File " + sys.argv[1] + " not found."
    # Read and open image
    """
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
    """
    #undistorted_image = cv2.imread("Camera\\Perspective\\Test\\DSC_3073.jpg", 1)
    image_name = sys.argv[1]
    calculate_area(image_name)