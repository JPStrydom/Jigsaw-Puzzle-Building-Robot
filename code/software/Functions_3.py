"""
Created on Wed Aug 31 10:22:45 2016

@author: JP
"""

import numpy as np
import cv2

import Functions_1 as F_1

DEBUG_CONSOLE = True       # To view contour information
DEBUG_NEW_CENTERS = False  # To view new center location distances
DEBUG_NEW_ANGLES = False   # To view recalculated angles




def Generate_Command_String(Com, c_s, c_d, d, t):
    """
    Generates command string from provided coordinates, pickup-drop depth and comand tag.
        Input:      Command, x y source pixel coordinates, x y destination pixel coordinate, pickup-drop depth, scommand tag
        Output:     Command string
    """

##### Pixel to step scaling factor [Calibration Values]
    pix_to_step_x = 1.7494
    pix_to_step_x_offset = -31.852
    pix_to_step_y = 1.7735
    pix_to_step_y_offset = -51.074

    # Convert pixel coordinates to step coordinates
    x_s_step = int(round(c_s[0]*pix_to_step_x + pix_to_step_x_offset))
    y_s_step = int(round(c_s[1]*pix_to_step_y + pix_to_step_y_offset))

    x_d_step = int(round(c_d[0]*pix_to_step_x + pix_to_step_x_offset))
    y_d_step = int(round(c_d[1]*pix_to_step_y + pix_to_step_y_offset))

    command_string = Com + " " + str(x_s_step) + " " + str(y_s_step) + " " + str(x_d_step) + " " + str(y_d_step) + " " + d + " " + t + "\r\n"

    return command_string




def Generate_Movement_Commands(Piece):
    """
    Generates movement commands for a list of pieces.
        Input:      Pieces in order of sollution, Image of corectly oriented pieces
        Output:     Array containing all movement command strings, Piece detection image of correctly oriented pieces
    """

##### Black strip temporary holding coordinates [Calibration Values]
    black_mid = 115 # pix
    black_pos_1 = 125
    black_pos_2 = 373
    black_pos_3 = 622
    black_pos_4 = 870

##### Solution image dimentions [Calibration Values]
    sol_x = 536
    sol_y = 372

##### Solution start ofset [Calibration Values]
    sol_off_x = 50
    sol_off_y = 272

##### Build offset [Calibration Values]
    x_build_off = 5
    y_build_off = 5

    # Initialise all temporary locations
    Temp_Location = np.zeros([len(Piece), 3])
    Temp_Location_Count = 0
    for i in xrange(len(Piece)):
        # Calculate temporary holding spot
        if i%4 == 0:
            Temp_Location[i] = [black_pos_1, black_mid, 1 + int(i>3) + int(i>7)]
        elif i%4 == 1:
            Temp_Location[i] = [black_pos_2, black_mid, 1 + int(i>3) + int(i>7)]
        elif i%4 == 2:
            Temp_Location[i] = [black_pos_3, black_mid, 1 + int(i>3) + int(i>7)]
        else:
            Temp_Location[i] = [black_pos_4, black_mid, 1 + int(i>3) + int(i>7)]

    Command = np.empty(0)
    Command_Temp = np.empty(0)

    for i, p in reversed(list(enumerate(Piece))):
        # Generate start to temporary spot command if piece in build area
        if i > 0 and In_Range(p.center_location, [sol_off_x, sol_off_y], [sol_off_x + sol_x, sol_off_y + sol_y]):
            temp_c = Temp_Location[Temp_Location_Count, :2]
            temp_d = Temp_Location[Temp_Location_Count, 2]
            Command_String = Generate_Command_String("M", p.center_location, temp_c, str(int(10 + temp_d)), "0")
            Command = np.append(Command, Command_String)
            Temp_Location_Count += 1

            # Adjust piece parameters
            p.center_location = temp_c
            p.stack_height = temp_d

        # Calculate solution destination coordinates with offset
        if i % 4 == 0:
            s_x = int(sol_x/8.0) + sol_off_x
        elif i % 4 == 1:
            s_x = int((sol_x/8.0)*3.0) + sol_off_x + x_build_off
        elif i % 4 == 2:
            s_x = int((sol_x/8.0)*5.0) + sol_off_x + 2*x_build_off
        else:
            s_x = int((sol_x/8.0)*7.0) + sol_off_x + 3*x_build_off

        if i < 4:
            s_y = int(sol_y/6.0) + sol_off_y
        elif i < 8:
            s_y = int((sol_y/6.0)*3.0) + sol_off_y + y_build_off
        else:
            s_y = int((sol_y/6.0)*5.0) + sol_off_y + 2*y_build_off

        # Generate current spot to solution spot command
        Command_String = Generate_Command_String("M", p.center_location, [s_x, s_y] , str(int(p.stack_height*10)), "0")
        Command_Temp = np.append(Command_String, Command_Temp)

    if len(Command) > 0:
        if Command[-1] != "E\r\n":
            Command = np.append(Command, "E\r\n")

    # Add placement commands to movement commands
    Command = np.append(Command, Command_Temp)

##### How many pixels to adjust by [Calibration Values]
    adj_pix_step = 20

    # Generate solution adjustment nudge commands
    for i in xrange(4):
        if i < 2:
            s_y = int((sol_y/6.0)*5.0) + adj_pix_step + sol_off_y
            y_dir = -1
        else:
            s_y = int(sol_y/6.0) - adj_pix_step + sol_off_y
            y_dir = 1


        if i % 2 == 0:
            s_x = int((sol_x/8.0)*7.0) + adj_pix_step + sol_off_x
            x_dir = -1
        else:
            s_x = int(sol_x/8.0) - adj_pix_step + sol_off_x
            x_dir = 1


        # Generate solution nudge command
        Command_String = Generate_Command_String("P", [s_x, s_y], [s_x + x_dir*adj_pix_step, s_y + y_dir*adj_pix_step] , "00", "0")
        Command = np.append(Command, Command_String)

    # Add final reset gantry command
    Command = np.append(Command, "E\r\n")

    if DEBUG_CONSOLE:
        for i, c in enumerate(Command):
            print (c),
        print ""

    Start = [[sol_off_x, sol_off_y]]
    Stop = [[sol_off_x + sol_x, sol_off_y + sol_y]]

##### Temporary strip block width [Calibration Values]
    block_width = 110
    for i in xrange(Temp_Location_Count):
        if i < 4:
            Start.append([int(Temp_Location[i,0] - block_width), int(Temp_Location[i,1] - block_width)])
            Stop.append([int(Temp_Location[i,0] + block_width) , int(Temp_Location[i,1] + block_width)])

    return Command, Start, Stop




def Generate_Rotation_Commands(Piece):
    """
    Generates rotation movement commands for a list of pieces.
        Input:      Pieces in order of sollution
        Output:     Array containing all rotation command strings
    """

    # Reset boolean
    r_bool = False

    Command = np.empty(0)

    # Generate rotation command if rotation is necessary
    for i, p in enumerate(Piece):
        # Add reset command for difficult shapes
        if p.angle >= 5 and p.angle <= 355:
            if r_bool and Has_Opposing_Indent(p.it_class):
                Command = np.append(Command, "E\r\n")
                r_bool =False
            elif not r_bool:
                r_bool = True

            Command_String = Generate_Command_String("R", p.center_location, p.center_location, str(11), str(p.angle))
            Command = np.append(Command, Command_String)

    # If there are rotation commands and the last on is not already a reset command append a reset command
    if len(Command) > 0:
        if Command[-1] != "E\r\n":
            Command = np.append(Command, "E\r\n")

    if DEBUG_CONSOLE:
        for i, c in enumerate(Command):
            print (c),
        print ""

    return Command




def Generate_Separation_Commands(From, To, Dir):
    """
    Generates piece separation commands for separation parameters.
        Input:      From coordinates, To coordinates, Direction of interim movement
        Output:     Array containing all separation command strings
    """

    Command = np.empty(0)

    # Generate separation comands if any are necessary
    if len(From) == 0:
        return
    else:
        for i in xrange(len(From)):
            Command_String = Generate_Command_String("S", From[i], To[i], str(11), str(Dir[i]))
            Command = np.append(Command, Command_String)

    Command = np.append(Command, "E\r\n")

    if DEBUG_CONSOLE:
        for i, c in enumerate(Command):
            print (c),
        print ""

    return Command




def Recalculate_Piece_Centers(Piece, img):
    """
    Recalculates piece centers from perspective transformed vinila image.
        Input:      Pieces in order of solution, Image of corectly oriented pieces
        Output:     Piece array with corrected centers, Piece detection image of correctly oriented pieces, True if pieces need to be re-rotated
    """

    # Create piece array in order of detection
    Piece_Temp = []
    for i in xrange(len(Piece)):
        for j, p in enumerate(Piece):
            if p.index == i:
                Piece_Temp.append(p)
                break

    # Deep copy image
    img = np.copy(img)

    # Find new piece centers and save them in Piece_Temp
    img_B = F_1.Clear_Background(img)
    img_BIN = F_1.Binarise(img_B)
    img_Detection, piece_cnt = Redetect_Pieces(img_BIN, img, Piece_Temp)
    classify_successful, Piece_Temp = F_1.Classify_Pieces(img_B, piece_cnt)

    # True if pieces need to be re-rotated
    re_rotate_bool = False

    # Assign new center locations to solution order piece array
    for i in xrange(len(Piece)):
        for j, p in enumerate(Piece):
            if p.index == i:
                p.center_location = np.copy(Piece_Temp[i].center_location)

                # Check if pieces were correctly oriented
                angle = np.copy(Piece_Temp[i].angle)

                # Check if pieces are < +- 45 degrees from being straight
                if angle > 45:
                    angle = angle - 90 + 360
                p.angle = (angle - 3*int(angle>180))*(angle >= 5 and angle <= 355)
                if p.angle != 0:
                    re_rotate_bool = True
                if DEBUG_CONSOLE and DEBUG_NEW_ANGLES:
                    if p.angle != 0:
                        print "Piece " , i, " angle = ", p.angle
                break

    if DEBUG_CONSOLE and DEBUG_NEW_ANGLES:
        print ""

    return Piece, img_Detection, re_rotate_bool




def Redetect_Pieces(img_bin, img_c, Piece):
    """
    Finds all the valid, stacked or unstacked, puzzle pieces
        Input:      Binarised puzzle layout image, Image to print piece edge and indexing on, Piece is detection order
        Output:     Piece edge and index image, valid piece contours
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

    piece_cnt = []

##### Min and Max piece areas [Calibration Values] [From line 277 in Functions_1]
    piece_min_area = 15000
    piece_max_area = 22000
    min_wh_ratio = 0.575
    max_wh_ratio = 1.75

    # Order valid contours in order of pieces to preserve piece indices
    for i, p in enumerate(Piece):
        min_dist = np.inf
        min_dist_index = 0
        for j, cnt in enumerate(contours):
            area = int(np.ceil(cv2.contourArea(cnt)))
            x,y,w,h = cv2.boundingRect(cnt)

            # If contour is valid
            if area >= piece_min_area and area <= piece_max_area and float(w)/float(h) < max_wh_ratio and float(w)/float(h) > min_wh_ratio:
                M = cv2.moments(cnt)
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])

                dist = np.sqrt((p.center_location[0]-cx)**2 + (p.center_location[1]-cy)**2)
                if dist < min_dist:
                    min_dist = dist
                    min_dist_index = j

        # Contour with smallest center distance to this piece is most likely its contour
        piece_cnt.append(contours[min_dist_index])

        if DEBUG_CONSOLE and DEBUG_NEW_CENTERS:
            print "Minimum distance for piece " + str(i) + " is " + str(min_dist)


    # Draw contours
    for i, cnt in enumerate(piece_cnt):
        cv2.drawContours(img_DC, [cnt], 0, [0,0,0], 5)
        cv2.drawContours(img_DC, [cnt], 0, color[i%12], 2)

        M = cv2.moments(cnt)
        cx = int(M["m10"]/M["m00"])
        cy = int(M["m01"]/M["m00"])
        cv2.putText(img_DC,str(i), (cx-20*(1+int(i>9)), cy+20), font, 2, [0,0,0], 6)
        cv2.putText(img_DC,str(i), (cx-20*(1+int(i>9)), cy+20), font, 2, color[i%12], 2)

    return img_DC, piece_cnt




def In_Range(Point, Start, Stop):
    """
    Checks if Point is within Start - Stop rectangle.
        Input:      Point to check, Start corner coordinate, Stop corner coordinate
        Output:     True if in rectangle else flase
    """

##### Range to check outside rectangle [Calibration Values]
    Range = 100

    if Point[0] > (Start[0] -Range) and Point[0] < (Stop[0]+ Range) and Point[1] > (Start[1] - Range) and Point[1] < (Stop[1]+ Range):
        return True
    return False




def Has_Opposing_Indent(it):
    """
    Checks if indent/tab class has opposing indents.
        Input:      Indent/Tab class
        Output:     True if indent/tab class contains opposing indents
    """

    return (it[0] + it[2] == -2) or (it[1] + it[3] == -2)



