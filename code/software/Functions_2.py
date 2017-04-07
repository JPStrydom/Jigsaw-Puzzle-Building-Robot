"""
Created on Wed Jul 27 20:13:16 2016

@author: JP
"""

import numpy as np
import cv2

import Classes as C

DEBUG_CONSOLE = False   # To view console debugging
DEBUG_IMAGE = False     # To view image debugging


def Find_Corners(Piece):
    """
    Extract all corner pieces from piece array into corner piece array
        Input:      Puzzle piece array
        Output:     Corner piece array
    """

    # Array to hold corner pieces
    Corner = []

    # For all pieces
    for i, P in enumerate(Piece):
        if P.is_corner():
            Corner.append(P)

    return Corner




def Solve_Puzzle(Piece):
    """
    Construct a puzzle object from each corner and select the best solution
        Input:      Puzzle piece array
        Output:     Solution successful, Puzzle piece array in solution order and orientation; Solution image
    """

    # Arrays to contain all solution pieces and scores from each solution
    solution_Pieces = []
    solution_Image = []
    solution_Score = []

    for c in xrange(4):
        Puzzle = C.Puzzle(Piece, c)
        S_P, S_I, S_S = Puzzle.Solve_Puzzle()
        if S_P != [] and S_I != [] and S_S != []:
            solution_Pieces.append(S_P)
            solution_Image.append(S_I)
            solution_Score.append(S_S)
            if DEBUG_CONSOLE:
                print "#######################################"
                print "solution", c, "Score = {:<8}".format(solution_Score[len(solution_Score) - 1])
                print "#######################################\n\n\n"
            if DEBUG_IMAGE:
                cv2.imshow("Preliminary solution "+str(c), solution_Image[len(solution_Score) - 1])

    if len(solution_Score) == 0:
        if DEBUG_CONSOLE:
            print "No solution found [line 65]\n"
        return False, [], []

    # Find minimum score
    min_score_index = np.argmin(solution_Score)

    if DEBUG_CONSOLE:
        print "#######################################\n#######################################"
        print "Chosen solution =", min_score_index, ": Score = {:<8}".format(solution_Score[min_score_index])
        print "#######################################\n#######################################\n\n"

    return True, solution_Pieces[min_score_index], solution_Image[min_score_index]




def Draw_Classification(Piece):
    """
    Draw all pieces in a grid
        Input:      Piece object array
        Output:
    """

    if len(Piece) == 0:
        if DEBUG_CONSOLE:
            print "Atempted to classify empty piece array [line 85]"
        return None

    # Colours to use for drawing
    color = np.array([(0,0,255), (0,125,255), (0,255,255), (0,255,125), (0,255,0), (125,255,0),
                  (255,255,0), (255,125,0), (255,0,0), (255,0,125), (255,0,255), (125,0,255)])

    font = cv2.FONT_HERSHEY_SIMPLEX

    img_piece = []

##### Border crop dimentions [Calibration Values]
    b_width = 48
    b_hight = 53

    # For all pieces
    for i, P in enumerate(Piece):
        img_piece.append(cv2.imread(P.file_name))

        img_width = img_piece[i].shape[0]

        # Draw index
        cv2.putText(img_piece[i], str(P.index), (img_width/2-20*(1+int(P.index>9)), img_width/2+20), font, 2, [0,0,0], 6)
        cv2.putText(img_piece[i], str(P.index), (img_width/2-20*(1+int(P.index>9)), img_width/2+20), font, 2, color[(P.index)%12], 2)

        cv2.putText(img_piece[i], str(P.angle), (img_width-55+20*(int(P.angle<10))-20*(int(P.angle>=100)), img_width-10), font, 1, [0,0,0], 3)
        cv2.putText(img_piece[i], str(P.angle), (img_width-55+20*(int(P.angle<10))-20*(int(P.angle>=100)), img_width-10), font, 1, color[(P.index)%12], 1)

        cv2.putText(img_piece[i], "o", (img_width-15, img_width-30), font, 0.5, [0,0,0], 3)
        cv2.putText(img_piece[i], "o", (img_width-15, img_width-30), font, 0.5, color[(P.index)%12], 1)

        # Draw indent/tab/edge marker for classification
        # Top
        if P.it_class[0] == -1:
             cv2.putText(img_piece[i], "I", (img_width/2-5, img_width/5), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "I", (img_width/2-5, img_width/5), font, 1.5, color[(P.index)%12], 2)
        elif P.it_class[0] == 0:
             cv2.putText(img_piece[i], "E", (img_width/2-10, img_width/5), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "E", (img_width/2-10, img_width/5), font, 1.5, color[(P.index)%12], 2)
        elif P.it_class[0] == 1:
             cv2.putText(img_piece[i], "T", (img_width/2-10, img_width/5), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "T", (img_width/2-10, img_width/5), font, 1.5, color[(P.index)%12], 2)

        # Right
        if P.it_class[1] == -1:
             cv2.putText(img_piece[i], "I", (4*img_width/5+10, img_width/2+15), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "I", (4*img_width/5+10, img_width/2+15), font, 1.5, color[(P.index)%12], 2)
        elif P.it_class[1] == 0:
             cv2.putText(img_piece[i], "E", (4*img_width/5+10, img_width/2+15), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "E", (4*img_width/5+10, img_width/2+15), font, 1.5, color[(P.index)%12], 2)
        elif P.it_class[1] == 1:
             cv2.putText(img_piece[i], "T", (4*img_width/5+10, img_width/2+15), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "T", (4*img_width/5+10, img_width/2+15), font, 1.5, color[(P.index)%12], 2)

        # Bottom
        if P.it_class[2] == -1:
             cv2.putText(img_piece[i], "I", (img_width/2-5, 4*img_width/5+30), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "I", (img_width/2-5, 4*img_width/5+30), font, 1.5, color[(P.index)%12], 2)
        elif P.it_class[2] == 0:
             cv2.putText(img_piece[i], "E", (img_width/2-10, 4*img_width/5+30), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "E", (img_width/2-10, 4*img_width/5+30), font, 1.5, color[(P.index)%12], 2)
        elif P.it_class[2] == 1:
             cv2.putText(img_piece[i], "T", (img_width/2-10, 4*img_width/5+30), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "T", (img_width/2-10, 4*img_width/5+30), font, 1.5, color[(P.index)%12], 2)

        # Left
        if P.it_class[3] == -1:
             cv2.putText(img_piece[i], "I", (img_width/5-30, img_width/2+15), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "I", (img_width/5-30, img_width/2+15), font, 1.5, color[(P.index)%12], 2)
        elif P.it_class[3] == 0:
             cv2.putText(img_piece[i], "E", (img_width/5-30, img_width/2+15), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "E", (img_width/5-30, img_width/2+15), font, 1.5, color[(P.index)%12], 2)
        elif P.it_class[3] == 1:
             cv2.putText(img_piece[i], "T", (img_width/5-30, img_width/2+15), font, 1.5, [0,0,0], 6)
             cv2.putText(img_piece[i], "T", (img_width/5-30, img_width/2+15), font, 1.5, color[(P.index)%12], 2)
             img_piece[i][b_hight:img_width-b_hight, b_width:img_width-b_width]


##### Border crop and piece dimentions [Calibration Values]
    b_width = 5
    p_width = img_width + b_width

    # Image to hold pieces
    img_classification = np.zeros((p_width*3+b_width, p_width*4+b_width, 3), np.uint8)
    img_classification[:, :, :] = 150

    piece_count = 0

    for y in xrange(3):
        for x in xrange(4):
            img_classification[b_width+p_width*y:p_width*(y+1), b_width+p_width*x:p_width*(x+1)] = img_piece[piece_count]
            piece_count += 1

    return img_classification




def Draw_solution(Piece):
    """
    Draw all solution pieces on a image
        Input:      Piece object array
        Output:
    """

    if len(Piece) == 0:
        if DEBUG_CONSOLE:
            print "Atempted to draw false soltion set [line 185]"
        return None, None

    # Colours to use for drawing
    color = np.array([(0,0,255), (0,125,255), (0,255,255), (0,255,125), (0,255,0), (125,255,0),
                  (255,255,0), (255,125,0), (255,0,0), (255,0,125), (255,0,255), (125,0,255)])

    font = cv2.FONT_HERSHEY_SIMPLEX

    img_piece = []

    # For all pieces
    for i, P in enumerate(Piece):
        img_piece.append(cv2.imread(P.file_name))

        img_width = img_piece[i].shape[0]

        # Draw index
        cv2.putText(img_piece[i], str(P.index), (img_width/2-20*(1+int(P.index>9)), img_width/2+20), font, 2, [0,0,0], 6)
        cv2.putText(img_piece[i], str(P.index), (img_width/2-20*(1+int(P.index>9)), img_width/2+20), font, 2, color[(P.index)%12], 2)


##### Border crop and piece dimentions [Calibration Values]
    b_width = 48
    b_hight = 53
    p_width = img_width - b_width*2
    p_hight = img_width - b_hight*2

    # Image to hold pieces
    img_solution = np.zeros((p_hight*3, p_width*4, 3), np.uint8)

    # Location [0, 0]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[:p_hight+b_hight, :p_width+b_width] = img_piece[0][b_hight:, b_width:]

    img_solution = cv2.bitwise_or(img_solution, img_mask)

    # Location [0, 1]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[:p_hight+b_hight, p_width-b_width:p_width*2+b_width] = img_piece[1][b_hight:, :]

    img_solution = cv2.bitwise_or(img_solution, img_mask)

    # Location [0, 2]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[:p_hight+b_hight, p_width*2-b_width:p_width*3+b_width] = img_piece[2][b_hight:, :]

    img_solution = cv2.bitwise_or(img_solution, img_mask)

    # Location [0, 3]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[:p_hight+b_hight, p_width*3-b_width:] = img_piece[3][b_hight:, :img_width-b_width]

    img_solution = cv2.bitwise_or(img_solution, img_mask)


    # Location [1, 0]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[p_hight-b_hight:p_hight*2+b_hight, :p_width+b_width] = img_piece[4][:, b_width:]

    img_solution = cv2.bitwise_or(img_solution, img_mask)

    # Location [1, 1]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[p_hight-b_hight:p_hight*2+b_hight, p_width-b_width:p_width*2+b_width] = img_piece[5]

    img_solution = cv2.bitwise_or(img_solution, img_mask)

    # Location [1, 2]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[p_hight-b_hight:p_hight*2+b_hight, p_width*2-b_width:p_width*3+b_width] = img_piece[6]

    img_solution = cv2.bitwise_or(img_solution, img_mask)

    # Location [1, 3]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[p_hight-b_hight:p_hight*2+b_hight, p_width*3-b_width:] = img_piece[7][:, :img_width-b_width]

    img_solution = cv2.bitwise_or(img_solution, img_mask)


    # Location [2, 0]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[p_hight*2-b_hight:, :img_width-b_width] = img_piece[8][:img_width-b_hight, b_width:]

    img_solution = cv2.bitwise_or(img_solution, img_mask)

    # Location [2, 1]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[p_hight*2-b_hight:, p_width-b_width:p_width*2+b_width] = img_piece[9][:img_width-b_hight, :]

    img_solution = cv2.bitwise_or(img_solution, img_mask)

    # Location [2, 2]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[p_hight*2-b_hight:, p_width*2-b_width:p_width*3+b_width] = img_piece[10][:img_width-b_hight, :]

    img_solution = cv2.bitwise_or(img_solution, img_mask)

    # Location [2, 3]
    img_mask = np.zeros((p_hight*3, p_width*4, 3), np.uint8)
    img_mask[p_hight*2-b_hight:, p_width*3-b_width:] = img_piece[11][:img_width-b_hight, :img_width-b_width]

    img_solution = cv2.bitwise_or(img_solution, img_mask)

##### Count black border width [Calibration Values]
    cb_b_width = 10

    # Count amount of black pixels within border and use as piece score
    solution_score = np.where(img_solution[cb_b_width:p_hight*3-cb_b_width, cb_b_width:p_width*4-cb_b_width] == [0,0,0])
    solution_score = np.shape(solution_score[0])[0]

    return img_solution, solution_score












