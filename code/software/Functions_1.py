"""
Created on Wed Jul 20 21:44:49 2016

@author: JP
"""

import numpy as np
import cv2
import winsound

import Classes as C

DEBUG_CONSOLE = False       # To view console debugging
DEBUG_CONTOUR = False       # To view contour information
DEBUG_IMAGE = False         # To view image debugging
DEBUG_PIECE_CENTERS = False  # To view piece centers


def Perspective_Transform_Points(img_c):
    """
    Finds points necesary to perform perspective transform on puzzle layout image.
        Input:      Colour image, skewed allong depth axis
        Output:     Points for transform
    """

##### Upper and lower HSV colour boundries for corner markers [Calibration Values]
    corner_lower_PT = np.array([100, 0, 155], dtype = "uint8") # [0, 0, 200] | [100, 50, 150]
    corner_upper_PT = np.array([170, 100, 255], dtype = "uint8") # [180, 55, 255] | [160, 100, 255]


    # Copy image in HSV colourspace
    img_hsv_PT = cv2.cvtColor(img_c, cv2.COLOR_BGR2HSV)

    # Get image dimentions
    rows_PT, cols_PT, chan_PT = img_hsv_PT.shape

    # Search untill all corner markers are found by continually decreasing HSV Value lower threshold
    top_left_found_PT = False
    top_right_found_PT = False
    bottom_left_found_PT = False
    bottom_right_found_PT = False

    while not (top_left_found_PT and top_right_found_PT and bottom_left_found_PT and bottom_right_found_PT):
        # Find colour within specified boundaries and apply mask
        mask_PT = cv2.inRange(img_hsv_PT, corner_lower_PT, corner_upper_PT)

######### Define search area's dimentions [Calibration Values]
        y_PT = 0.125
        top_x_PT = 0.125
        bottom_x_PT = 0.075

        # Find inner most top left corner mark index
        if not top_left_found_PT:
            for x in xrange(int(cols_PT*top_x_PT), -1, -1):
                for y in xrange(int(rows_PT*y_PT), -1, -1):
                    if mask_PT[y, x] == 255:
                        top_left_PT = [x, y]
                        top_left_found_PT = True
                        break
                if top_left_found_PT:
                    break

        # Find inner most top right corner mark index
        if not top_right_found_PT:
            for x in xrange(int(cols_PT - cols_PT*top_x_PT), cols_PT):
                for y in xrange(int(rows_PT*y_PT), -1, -1):
                    if mask_PT[y, x] == 255:
                        top_right_PT = [x, y]
                        top_right_found_PT = True
                        break
                if top_right_found_PT:
                    break

        # Find inner most bottom right corner mark index
        if not bottom_right_found_PT:
            for x in xrange(int(cols_PT - cols_PT*bottom_x_PT), cols_PT):
                for y in xrange(int(rows_PT - rows_PT*y_PT), rows_PT):
                    if mask_PT[y, x] == 255:
                        bottom_right_PT = [x, y]
                        bottom_right_found_PT = True
                        break
                if bottom_right_found_PT:
                    break

        # Find inner most bottom left corner mark index
        if not bottom_left_found_PT:
            for x in xrange(int(cols_PT*bottom_x_PT), -1, -1):
                for y in xrange(int(rows_PT - rows_PT*y_PT), rows_PT):
                    if mask_PT[y, x] == 255:
                        bottom_left_PT = [x, y]
                        bottom_left_found_PT = True
                        break
                if bottom_left_found_PT:
                    break
        # If any corner markers aren't found, decreasing HSV Value lower threshold and try again
        if not (top_left_found_PT and top_right_found_PT and bottom_left_found_PT and bottom_right_found_PT):
            corner_lower_PT[2] -= 10

        if DEBUG_CONSOLE:
            if not top_left_found_PT:
                print "Top Left Missed [line 100]"
            if not top_right_found_PT:
                print "Top Right Missed [line 100]"
            if not bottom_left_found_PT:
                print "Bottom Left Missed [line 100]"
            if not bottom_right_found_PT:
                print "Bottom Right Missed [line 100]"

    if DEBUG_IMAGE:
		cv2.imshow('HSV', img_hsv_PT)
		cv2.imshow('MASK', mask_PT)

    return [top_left_PT, top_right_PT, bottom_right_PT, bottom_left_PT]




def Minimise_Perspective_Transform_Points(pts_1, pts_2):
    """
    Finds the innermost points between points pts_1 and pts_2.
        Input:      Perspective transform points 1, Perspective transform points 2
        Output:     Minimised perspective transform points for transform
    """

    # perform deep copy
    pts_1 = np.copy(pts_1)
    pts_2 = np.copy(pts_2)

    # Array to hold most inner point values
    pts_min = [[0, 0], [0, 0], [0, 0], [0, 0]]

    # Set top left to min value
    if pts_1[0][0] >= pts_2[0][0] and pts_1[0][1] >= pts_2[0][1]:
        pts_min[0][0] = pts_1[0][0]
        pts_min[0][1] = pts_1[0][1]
    else:
        pts_min[0][0] = pts_2[0][0]
        pts_min[0][1] = pts_2[0][1]

    # Set top right to min value
    if pts_1[1][0] <= pts_2[1][0] and pts_1[1][1] >= pts_2[1][1]:
        pts_min[1][0] = pts_1[1][0]
        pts_min[1][1] = pts_1[1][1]
    else:
        pts_min[1][0] = pts_2[1][0]
        pts_min[1][1] = pts_2[1][1]

    # Set bottom right to min value
    if pts_1[2][0] <= pts_2[2][0] and pts_1[2][1] <= pts_2[2][1]:
        pts_min[2][0] = pts_1[2][0]
        pts_min[2][1] = pts_1[2][1]
    else:
        pts_min[2][0] = pts_2[2][0]
        pts_min[2][1] = pts_2[2][1]

    # Set bottom left to min value
    if pts_1[3][0] >= pts_2[3][0] and pts_1[3][1] <= pts_2[3][1]:
        pts_min[3][0] = pts_1[3][0]
        pts_min[3][1] = pts_1[3][1]
    else:
        pts_min[3][0] = pts_2[3][0]
        pts_min[3][1] = pts_2[3][1]

    return pts_min




def Draw_Perspective_Transform_Points(img, pts):
    """
    Draws the perspective transform points onto image.
        Input:      Untransformed image, Perspective transform points
        Output:     Untransformed image with perspective points drawn on
    """


    for i, p in enumerate(pts):
        cv2.line(img, tuple(pts[i-1]), tuple(p), (0,0,0), 8)
        cv2.line(img, tuple(pts[i-1]), tuple(p), (255,0,0), 2)
    for i, p in enumerate(pts):
        cv2.circle(img, tuple(p), 6, (0,0,0), -1)
        cv2.circle(img, tuple(p), 3, (0,255,255), -1)

    return img




def Perspective_Transform(img_PT, corner_PT):
    """
    Performs perspective transform on colour image of puzzle layout.
        Input:      Colour image, skewed allong depth axis; Points for transform
        Output:     Straightened colour image with constant image depth
    """

    # Get image dimentions
    rows_PT, cols_PT, chan_PT = img_PT.shape

    # Define points for transform
    current_points_PT = np.float32([corner_PT[0], corner_PT[1], corner_PT[2], corner_PT[3]])
    desired_points_PT = np.float32([[0, 0], [cols_PT-1, 0], [cols_PT-1, rows_PT-1], [0, rows_PT-1]])

    # Calculate transform matrix
    M = cv2.getPerspectiveTransform(current_points_PT, desired_points_PT)

    # Calculate and return adjusted image
    return cv2.warpPerspective(img_PT, M, (cols_PT, rows_PT))




def Clear_Background(img_c):
    """
    Find puzzle layout background and set it to black
        Input:      Colour puzzle layout image
        Output:     Colour image with its background set to black
    """

##### Upper and lower boundries background [Calibration Values]
    background_lower = np.array([160, 175, 125], dtype = "uint8") # [165, 75, 75] For hulk puzzle # [160, 175, 125] For chicken puzzle
    background_upper = np.array([175, 255, 255], dtype = "uint8") # [180, 255, 255] For hulk puzzle # [170, 255, 255] For chicken puzzle


    # Copy image in HSV colourspace
    img_hsv_B = cv2.cvtColor(img_c, cv2.COLOR_BGR2HSV)

    # Get image dimentions
    rows_B, cols_B, chan_B = img_hsv_B.shape

    # Find colour within specified boundaries and apply mask
    mask_B = cv2.inRange(img_hsv_B, background_lower, background_upper)
    mask_inv_B = cv2.bitwise_not(mask_B)

    # Apply mask to clear background
    img_B = cv2.bitwise_and(img_c, img_c, mask = mask_inv_B)

##### Edge percentage to blackout [Calibration Values]
    edge_blackout = 0.01

    # Blackout edges
    img_B[:int(rows_B*edge_blackout), :, :] = 0
    img_B[:, :int(cols_B*edge_blackout), :] = 0
    img_B[int(rows_B - rows_B*edge_blackout):rows_B, :, :] = 0
    img_B[:, int(cols_B - cols_B*edge_blackout):cols_B, :] = 0

    return img_B




def Binarise(img_b):
    """
    Creates a binarised version of the puzzle image
        Input:      Colour puzzle layout image with cleared background
        Output:     Binarised image
    """

    # Copy image as grayscale
    img_bw_BIN = cv2.cvtColor(img_b, cv2.COLOR_BGR2GRAY)

##### Apply Gaussian filter [Calibration Values]
    img_gf_BIN = cv2.GaussianBlur(img_bw_BIN, (3, 3), 0)

    # Find and return binarised image
    return cv2.threshold(img_gf_BIN, 1, 255, cv2.THRESH_BINARY)[1]




def Detect_Pieces(img_bin, img_c):
    """
    Finds all the valaid, stacked or unstacked, puzzle pieces
        Input:      Binarised puzzle layout image, Image to print piece edge and indexing on
        Output:     Piece edge and index image, Valaid piece contours, Overlapping piece contours
    """

    # Copy image
    img_DC = np.copy(img_c)

    # Get image dimentions
    rows_DC, cols_DC, chan_DC = img_DC.shape

    # Colours to use for drawing
    color = np.array([(0,0,255), (0,125,255), (0,255,255), (0,255,125), (0,255,0), (125,255,0),
                  (255,255,0), (255,125,0), (255,0,0), (255,0,125), (255,0,255), (125,0,255)])

    # Detect contours
    contours = cv2.findContours(np.copy(img_bin), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

    font = cv2.FONT_HERSHEY_SIMPLEX

    piece_count = 0
    overlap_count = 0

    piece_cnt = []
    overlap_cnt = []

##### Min and Max piece areas [Calibration Values]
    piece_min_area = 15000 # 16000 For hulk puzzle # 15000 For chicken puzzle
    piece_max_area = 22000 # 26000 For hulk puzzle # 21000 For chicken puzzle
    overlap_max_area = 3*piece_max_area
    min_wh_ratio = 0.575
    max_wh_ratio = 1.75
    min_wh_ratio_overlap = 0.2
    max_wh_ratio_overlap = 3.6
    min_fo_area = 1000
    max_fo_area = 260000

    # Loop over contours to find valaid or overlapping ones
    for h, cnt in reversed(list(enumerate(contours))):
        area = int(np.ceil(cv2.contourArea(cnt)))
        x,y,w,h = cv2.boundingRect(cnt)
        if area >= piece_min_area and area <= piece_max_area and float(w)/float(h) < max_wh_ratio and float(w)/float(h) > min_wh_ratio:
            if DEBUG_CONSOLE and DEBUG_CONTOUR:
                print "Piece  ", piece_count, "Area =", area, "Bound Rect H/W = {:<8.2f}".format(float(w)/float(h))

            cv2.drawContours(img_DC, [cnt], 0, [0,0,0], 5)
            cv2.drawContours(img_DC, [cnt], 0, color[piece_count%12], 2)

            M = cv2.moments(cnt)
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            string = str(piece_count)
            cv2.putText(img_DC,string, (cx-20*(1+int(piece_count>9)), cy+20), font, 2, [0,0,0], 6)
            cv2.putText(img_DC,string, (cx-20*(1+int(piece_count>9)), cy+20), font, 2, color[piece_count%12], 2)

            # Add contour to piece contour list
            piece_cnt.append(cnt)
            piece_count += 1
        elif area > piece_max_area and area < overlap_max_area and float(w)/float(h) < max_wh_ratio_overlap and float(w)/float(h) > min_wh_ratio_overlap:
            if DEBUG_CONSOLE and DEBUG_CONTOUR:
                print "Overlap", piece_count, "Area =", area, "Bound Rect H/W = {:<8.2f}".format(float(w)/float(h))
            cv2.drawContours(img_DC, [cnt], 0, color[(overlap_count*3+1)%12], -1)
            cv2.drawContours(img_DC, [cnt], 0, [0,0,0], 2)

            # Add contour to overlap contour list
            overlap_cnt.append(cnt)
            overlap_count += 1
        elif area > min_fo_area and area < max_fo_area:
            if DEBUG_CONSOLE and DEBUG_CONTOUR:
                print "Foreign", piece_count, "Area =", area, "Bound Rect H/W = {:<8.2f}".format(float(w)/float(h))
            if DEBUG_IMAGE:
                cv2.drawContours(img_DC, [cnt], 0, [125,125,125], -1)
                cv2.drawContours(img_DC, [cnt], 0, [0,0,0], 6)
                cv2.drawContours(img_DC, [cnt], 0, [0,0,255], 1)



    if DEBUG_CONSOLE and DEBUG_CONTOUR:
        print ""

    return img_DC, piece_cnt, overlap_cnt




def Separate_Overlap(img_bin, img_dp, overlap_cnt):
    """
    Find open area to move overlapping pieces to if any are present
        Input:      Binarised puzzle layout image, Colour puzzle layout image, Overlapping piece contours
        Output:     Movement indicating image, From coordinates, To coordinates
    """

    # If no overlapping contours are present return none
    if np.shape(overlap_cnt)[0] == 0:
        if DEBUG_CONSOLE:
            print "False exit [line 270]"
        return False, False, False

    # Copy images
    img_bin_SO = np.copy(img_bin)
    img_SO = np.copy(img_dp)

    # Get image dimentions
    rows_SO, cols_SO = img_bin_SO.shape

    # Colours to use for drawing
    color = np.array([(0,0,255), (0,125,255), (0,255,255), (0,255,125), (0,255,0), (125,255,0),
                  (255,255,0), (255,125,0), (255,0,0), (255,0,125), (255,0,255), (125,0,255)])

    # To stoor to and from coordinates
    From = []
    To = []
    Dir = []

    # For all overlapping contours
    for h, cnt in enumerate(overlap_cnt):

        M = cv2.moments(cnt)
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])

        # Find estimate centre line
        [vx,vy,x,y] = cv2.fitLine(cnt, cv2.cv.CV_DIST_HUBER, 0, 0.01, 0.01)
        y1 = (-x*vy/vx) + y
        y2 = ((cols_SO-x)*vy/vx)+y

        m = (cols_SO-1)/(y2-y1)
        c = -y1*m

        # Pick up coordinate
        pickup_point = []

######### Manipulator radius [Calibration Values]
        man_rad = 30
        min_man_rad = 15

        # Search allong center line for suficient manipulator space
        spot_found = False
        while not spot_found:
            for y in xrange(rows_SO-1,-1, -3):
                x = int(m*y + c)
                if x >= 0:
                    if cv2.pointPolygonTest(cnt, (x, y), True) >= man_rad:
                        pickup_point.append((x, y))
                        spot_found = True
            if not spot_found:
                if man_rad <= min_man_rad:
                    break
                man_rad -= 5

        p_pts = np.shape(pickup_point)[0]

        # Continue only if possible pickup point is found
        if p_pts > 0:
            # Which possible pick up point to use
            if np.sqrt((pickup_point[0][0] - cx)**2 + (pickup_point[0][1] - cy)**2) > np.sqrt((pickup_point[-1][0] - cx)**2 + (pickup_point[-1][1] - cy)**2):
                pp_index = 0
            else:
                pp_index = -1

            # Draw possible points and recommended point
            cv2.line(img_SO, pickup_point[0], pickup_point[-1], (0,0,0), 30)
            cv2.circle(img_SO, pickup_point[pp_index], 10, (255,255,255), -1)

            if DEBUG_IMAGE:
                cv2.circle(img_SO, tuple([cx, cy]), 10, (0,0,0), -1)
                cv2.circle(img_SO, tuple([cx, cy]), 5, (100,200,100), -1)

            # Add to list
            From.append(pickup_point[pp_index])

            if abs(pickup_point[pp_index][0] - cx) > abs(pickup_point[pp_index][1] - cy):
                if pickup_point[pp_index][0] > cx:
                    Dir.append(1)
                else:
                    Dir.append(3)
            else:
                if pickup_point[pp_index][1] < cy:
                    Dir.append(0)
                else:
                   Dir.append(2)


############# Available area search parameters [Calibration Values]
            search_radius = 110 # 125 For hulk puzzle # 110 For hoarse puzzle
            edge_search_dist = 50 + search_radius
            x_search_step = 200
            y_search_step = 150
            min_x_search_step = 10

            # Search untill sufficient open space is found by decreasing search step if necessary
            spot_found = False
            while not spot_found:
                for y in xrange(rows_SO-edge_search_dist, edge_search_dist, -y_search_step):
                    for x in xrange(cols_SO-edge_search_dist, edge_search_dist, -x_search_step):
                        if np.average(img_bin_SO[y-search_radius:y+search_radius, x-search_radius:x+search_radius]) == 0:
                            # Add to list
                            To.append((x, y))

                            # Draw available spot
                            cv2.rectangle(img_SO,(x-search_radius, y-search_radius), (x+search_radius, y+search_radius), (0,0,0), 9)
                            cv2.rectangle(img_SO,(x-search_radius, y-search_radius), (x+search_radius, y+search_radius), color[(h*3+1)%12], 3)
                            cv2.circle(img_SO, (x, y), 15, (0,0,0), -1)
                            cv2.circle(img_SO, (x, y), 10, (255,255,255), -1)

                            # Label spot just taken as unavailable
                            img_bin_SO[y-search_radius:y+search_radius, x-search_radius:x+search_radius] = 255
                            spot_found = True
                            break
                    if spot_found:
                        break
                # If still not found perform more search steps
                if not spot_found:
                    # If possible point is still not found stop searching
                    if x_search_step <= min_x_search_step:
                        # Discard contour all together
                        From.pop()
                        if DEBUG_CONSOLE:
                            print "\nERROR! No enough available space [line 369]\n" # Could perhaps return False, False, False to request new image
                            Freq = 500
                            Dur = 250
                            winsound.Beep(Freq, Dur)
                        break
                    x_search_step = int(x_search_step/2)
                    y_search_step = int(y_search_step/2)
        else:
            if DEBUG_CONSOLE:
                print "\nERROR! Pick up point not found [line 377]\n" # Could perhaps return False, False, False to request new image
                Freq = 1000
                Dur = 250
                winsound.Beep(Freq,Dur)

        # Draw movement arrows
        for i, frm in enumerate(From):
            cv2.arrowedLine(img_SO, From[i], To[i], (0,0,0), 9)
            cv2.arrowedLine(img_SO, From[i], To[i], (125,125,125), 3)

    return img_SO, From, To, Dir



def Classify_Pieces(img_b, piece_cnt):
    """
    Once all pieces are fully visable this function will classify them all
        Input:      Binarised puzzle layout image, Colour puzzle layout image with blacked out background, Piece contours
        Output:     True if edge_num edges are found, Array containing piece objects
    """

##### Max piece width [Calibration Values]
    max_piece_width = 230 # 240 for hulk puzzle # 230 for hoarse puzzle

##### Angle deviation on line [Calibration Values]
    ang_dev = 0.35 # Rad

    # Define piece object array
    Piece_C = np.empty(0, dtype=object)

    # Copy images
    img_b_PC = np.copy(img_b)

    # Get image dimentions
    rows_PC, cols_PC, chan_PC = img_b_PC.shape

##### To check if all edges were found [Calibtarion Values]
    edge_num = 14

    edge_count = 0

    # For all valid piece contours
    for i, cnt in enumerate(piece_cnt):
        # Center location in overall image
        M = cv2.moments(cnt)
        cx_original = int(M["m10"]/M["m00"])
        cy_original = int(M["m01"]/M["m00"])

        # Find bound rectangle points
        x,y,w,h = cv2.boundingRect(cnt)
        if w%2 != 0:
            w += 1
        if h%2 != 0:
            h += 1

        # Create max_piece_width by max_piece_width image with puzzle piece at its center
        img_piece = np.zeros((max_piece_width, max_piece_width, 3), np.uint8)
        img_piece[max_piece_width/2-h/2:max_piece_width/2+h/2, max_piece_width/2-w/2:max_piece_width/2+w/2] = img_b_PC[y:y+h, x:x+w]

        # Find new piece image contour for re-centering
        img_piece_bin = Binarise(img_piece)
        piece_cnt = cv2.findContours(img_piece_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

        # Use only largest contour
        max_area = 0
        m_a_index = 0
        for h, cnt in enumerate(piece_cnt):
            area = int(np.ceil(cv2.contourArea(cnt)))
            if  area > max_area:
                max_area = area
                m_a_index = h

        # True center of piece
        M = cv2.moments(piece_cnt[m_a_index])
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])

        # Offset from true center
        c_off_x = max_piece_width/2 - cx
        c_off_y = max_piece_width/2 - cy

        # Re-center image
        M = np.float32([[1,0,c_off_x],[0,1,c_off_y]])
        img_piece = cv2.warpAffine(img_piece,M,(max_piece_width,max_piece_width))

        # Set new piece image center
        cx = max_piece_width/2
        cy = max_piece_width/2

        # Binarise piece image and apply Canny edge detection
        img_piece_bin = Binarise(img_piece)
        img_piece_edge = cv2.Canny(img_piece_bin, 50, 150, apertureSize = 3)

        # Find all Hough lines in edge piece image
        lines = cv2.HoughLines(img_piece_edge, 1, np.pi/180, 30, 75)

        A_1 = []
        A_2 = []
        A_3 = []
        A_4 = []

        # For all lines
        for rho,theta in lines[0]:
            # Add all lines that are within ang_dev radians from one another
            if np.shape(A_1)[0] == 0:
                A_1.append(theta)
            elif abs((sum(A_1)/len(A_1)) - theta) <= ang_dev:
                A_1.append(theta)

            elif np.shape(A_2)[0] == 0:
                A_2.append(theta)
            elif abs((sum(A_2)/len(A_2)) - theta) <= ang_dev:
                A_2.append(theta)

            elif np.shape(A_3)[0] == 0:
                A_3.append(theta)
            elif abs((sum(A_3)/len(A_3)) - theta) <= ang_dev:
                A_3.append(theta)

            elif np.shape(A_4)[0] == 0:
                A_4.append(theta)
            elif abs((sum(A_4)/len(A_4)) - theta) <= ang_dev:
                A_4.append(theta)

        # Use edge with the most lines
        if len(A_1) >= len(A_2) and len(A_1) >= len(A_3) and len(A_1) >= len(A_4):
            A = sum(A_1)/len(A_1)
        elif len(A_2) >= len(A_3) and len(A_2) >= len(A_4):
            A = sum(A_2)/len(A_2)
        elif len(A_3) >= len(A_4):
            A = sum(A_3)/len(A_3)
        else:
            A = sum(A_4)/len(A_4)

        # Convert angle to degrees (<90)
        A_C = (A*180/np.pi)%90

        # Rotate piece image and binarised image
        M = cv2.getRotationMatrix2D((max_piece_width/2, max_piece_width/2), A_C, 1)
        img_piece = cv2.warpAffine(img_piece, M, (max_piece_width, max_piece_width))

        # Find new piece contour defects
        img_piece_bin = Binarise(img_piece)
        piece_cnt = cv2.findContours(img_piece_bin, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

        # Use only largest contour
        max_area = 0
        m_a_index = 0
        for h, cnt in enumerate(piece_cnt):
            area = int(np.ceil(cv2.contourArea(cnt)))
            if  area > max_area:
                max_area = area
                m_a_index = h

        # Find piece contour defects
        hull = cv2.convexHull(piece_cnt[m_a_index], returnPoints = False)
        defects = cv2.convexityDefects(piece_cnt[m_a_index], hull)

        top_found_bool = False
        right_found_bool = False
        bottom_found_bool = False
        left_found_bool = False

######### Indent\tab boundary defect distances [Calibration Values]
        indent_min_d = 6500 # 9500 For hulk Puzzle # 6500 For hoarse puzzle
        tab_max_d = 500
        defect_line_max_d = 15 # 30 # 25 Previous value

######### Tab width from (cx, cy) to consider [Calibration Values]
        tab_w_off = max_piece_width/10

        # Indent/tab matrix
        it_class_C = np.zeros(4, dtype=int)

        if DEBUG_IMAGE:
            img_piece_debug = np.copy(img_piece)

        # Search for indents
        for search in range(defects.shape[0]):
            s,e,f,d = defects[search,0]
            if s<cnt.shape[0] and e<cnt.shape[0] and f<cnt.shape[0]:
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                # If defect is far enough from fit contour
                if d > indent_min_d:
                    # Indent to top
                    if not top_found_bool and cy > far[1] and np.abs(cx-far[0]) < np.abs(cy-far[1]):
                        top_found_bool = True
                        it_class_C[0] = -1
                        if DEBUG_IMAGE:
                            cv2.line(img_piece_debug,start,end,[255,0,255],2)
                            cv2.circle(img_piece_debug,far,3,[0,0,255],-1)
                            cv2.circle(img_piece_debug,far,1,[255,0,255],-1)
                    # Indent to right
                    elif not right_found_bool and cx < far[0] and np.abs(cx-far[0]) > np.abs(cy-far[1]):
                        right_found_bool = True
                        it_class_C[1] = -1
                        if DEBUG_IMAGE:
                            cv2.line(img_piece_debug,start,end,[255,0,255],2)
                            cv2.circle(img_piece_debug,far,3,[0,0,255],-1)
                            cv2.circle(img_piece_debug,far,1,[255,0,255],-1)
                    # Indent to bottom
                    elif not bottom_found_bool and cy < far[1] and np.abs(cx-far[0]) < np.abs(cy-far[1]):
                        bottom_found_bool = True
                        it_class_C[2] = -1
                        if DEBUG_IMAGE:
                            cv2.line(img_piece_debug,start,end,[255,0,255],2)
                            cv2.circle(img_piece_debug,far,3,[0,0,255],-1)
                            cv2.circle(img_piece_debug,far,1,[255,0,255],-1)
                    # Indent to left
                    elif not left_found_bool and cx > far[0] and np.abs(cx-far[0]) > np.abs(cy-far[1]):
                        left_found_bool = True
                        it_class_C[3] = -1
                        if DEBUG_IMAGE:
                            cv2.line(img_piece_debug,start,end,[255,0,255],2)
                            cv2.circle(img_piece_debug,far,3,[0,0,255],-1)
                            cv2.circle(img_piece_debug,far,1,[255,0,255],-1)

        # Search for tabs
        for search in range(defects.shape[0]):
            s,e,f,d = defects[search,0]
            if s<cnt.shape[0] and e<cnt.shape[0] and f<cnt.shape[0]:
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                if d < tab_max_d and np.sqrt((start[0]-end[0])**2+(start[1]-end[1])**2) < defect_line_max_d:
                    # Tab to top
                    if not top_found_bool and cy > far[1] and np.abs(cx-far[0]) < np.abs(cy-far[1]) and np.abs(cx-far[0]) <= tab_w_off:
                        top_found_bool = True
                        it_class_C[0] = 1
                        if DEBUG_IMAGE:
                            cv2.line(img_piece_debug,start,end,[0,255,0],2)
                            cv2.circle(img_piece_debug,far,3,[255,0,0],-1)
                            cv2.circle(img_piece_debug,far,1,[0,255,0],-1)
                    # Tab to right
                    elif not right_found_bool and cx < far[0] and np.abs(cx-far[0]) > np.abs(cy-far[1]) and np.abs(cy-far[1]) <= tab_w_off:
                        right_found_bool = True
                        it_class_C[1] = 1
                        if DEBUG_IMAGE:
                            cv2.line(img_piece_debug,start,end,[0,255,0],2)
                            cv2.circle(img_piece_debug,far,3,[255,0,0],-1)
                            cv2.circle(img_piece_debug,far,1,[0,255,0],-1)
                    # Tab to bottom
                    elif not bottom_found_bool and cy < far[1] and np.abs(cx-far[0]) < np.abs(cy-far[1]) and np.abs(cx-far[0]) <= tab_w_off:
                        bottom_found_bool = True
                        it_class_C[2] = 1
                        if DEBUG_IMAGE:
                            cv2.line(img_piece_debug,start,end,[0,255,0],2)
                            cv2.circle(img_piece_debug,far,3,[255,0,0],-1)
                            cv2.circle(img_piece_debug,far,1,[0,255,0],-1)
                    # Tab to left
                    elif not left_found_bool and cx > far[0] and np.abs(cx-far[0]) > np.abs(cy-far[1]) and np.abs(cy-far[1]) <= tab_w_off:
                        left_found_bool = True
                        it_class_C[3] = 1
                        if DEBUG_IMAGE:
                            cv2.line(img_piece_debug,start,end,[0,255,0],2)
                            cv2.circle(img_piece_debug,far,3,[255,0,0],-1)
                            cv2.circle(img_piece_debug,far,1,[0,255,0],-1)

        if not top_found_bool: # Edge to top
            edge_count += 1
            top_found_bool = True
        if not right_found_bool: # Edge to right
            edge_count += 1
            right_found_bool = True
        if not bottom_found_bool: # Edge to bottom
            edge_count += 1
            bottom_found_bool = True
        if not left_found_bool: # Edge to left
            edge_count += 1
            left_found_bool = True

        if DEBUG_IMAGE:
            cv2.circle(img_piece_debug,tuple([max_piece_width/2,max_piece_width/2]),3,[0,0,0],-1)
            cv2.circle(img_piece_debug,tuple([max_piece_width/2,max_piece_width/2]),1,[255,255,255],-1)

        # Offset due to unsemetric piece shapes
        c_off_x = 0
        c_off_y = 0

######### Percentage to compensate for unsemetric shape [Calibration Values]
        tab_offset = 3.5
        indent_offset = 1.75

        # Find unsemetric compensation values
        for it in xrange(4):
            if it == 0:
                c_off_y -= int(it_class_C[it] == 1)*int(max_piece_width*tab_offset/100) - int(it_class_C[it] == -1)*int(max_piece_width*indent_offset/100)
            elif it == 1:
                c_off_x += int(it_class_C[it] == 1)*int(max_piece_width*tab_offset/100) - int(it_class_C[it] == -1)*int(max_piece_width*indent_offset/100)
            elif it == 2:
                c_off_y += int(it_class_C[it] == 1)*int(max_piece_width*tab_offset/100) - int(it_class_C[it] == -1)*int(max_piece_width*indent_offset/100)
            elif it == 3:
                c_off_x -= int(it_class_C[it] == 1)*int(max_piece_width*tab_offset/100) - int(it_class_C[it] == -1)*int(max_piece_width*indent_offset/100)

        # Apply unsemetric compensation
        M = np.float32([[1,0,c_off_x],[0,1,c_off_y]])
        img_piece = cv2.warpAffine(img_piece,M,(max_piece_width,max_piece_width))
        if DEBUG_IMAGE:
            img_piece_debug = cv2.warpAffine(img_piece_debug,M,(max_piece_width,max_piece_width))

        # Calculate parameters to adjust original image piece coordinates
        r = np.sqrt(c_off_x**2 + c_off_y**2)
        a = -(np.arctan2(-c_off_y, c_off_x)*180/np.pi) + A_C + 180

        # Adjust original image piece coordinates
        cx_original = cx_original + int(r*np.cos(a*np.pi/180))
        cy_original = cy_original + int(r*np.sin(a*np.pi/180))
        piece_center_location_C = tuple([cx_original,cy_original])

        if DEBUG_PIECE_CENTERS:
            cv2.circle(img_b,piece_center_location_C,3,[0,0,0],-1)
            cv2.circle(img_b,piece_center_location_C,1,[0,165,255],-1)
            cv2.imshow("Debug Center", img_b)



        # Save piece image
        piece_file_name_C = "pieces\\classification\\p_"+str(i)+".png"
        cv2.imwrite(piece_file_name_C, img_piece)

        # Create piece object
        Piece_C = np.append(Piece_C, C.Puzzle_Piece(i, piece_center_location_C, it_class_C, A_C, piece_file_name_C))

        if DEBUG_IMAGE:
            cv2.circle(img_piece_debug,tuple([max_piece_width/2,max_piece_width/2]),3,[0,0,0],-1)
            cv2.circle(img_piece_debug,tuple([max_piece_width/2,max_piece_width/2]),1,[0,165,255],-1)

        if DEBUG_IMAGE:
            cv2.imshow("Debug [Piece"+str(i)+"]", img_piece_debug)

    return edge_count == edge_num, Piece_C































