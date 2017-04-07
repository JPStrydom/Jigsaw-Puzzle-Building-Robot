"""
Created on Wed Jul 20 11:03:07 2016

@author: JP
"""

import numpy as np
import cv2
import time

import Functions_1 as F_1
import Functions_2 as F_2

Recalc_PT_bool = True

Recalc_PT_num = 10
Recalc_PT_count = 0

PT_bool = False         # Perform Perspective Transform
DP_bool = False         # Detect Pieces
CP_bool = False         # Clasify Pieces
SO_bool = False         # Seperate Overlapping Pieces
CP_bool = False         # Classify Pieces
SOLVE_bool = False      # Solve Puzzle

pts_min = [[0, 0], [np.inf, 0], [np.inf, np.inf], [0, np.inf]]

while(True):
    frame = cv2.imread("images\\original-1.png")
    img = np.copy(frame)

    if Recalc_PT_bool:
        pts = F_1.Perspective_Transform_Points(frame)
        pts_min = F_1.Minimise_Perspective_Transform_Points(pts_min, pts)
        pts = np.copy(pts_min)
        if Recalc_PT_count >= Recalc_PT_num:
            Recalc_PT_bool = False
        else:
            Recalc_PT_count += 1

    if PT_bool:
        img_C = F_1.Perspective_Transform(frame, pts)
        img = np.copy(img_C)
        if DP_bool:
            img_B = F_1.Clear_Background(img_C)
            img_BIN = F_1.Binarise(img_B)
            img_DP, piece_cnt, overlap_cnt = F_1.Detect_Pieces(img_BIN, img_C)
            img = np.copy(img_DP)
            if SO_bool and np.shape(overlap_cnt)[0] != 0:
                img_SO, From, To, Dir = F_1.Separate_Overlap(img_BIN, img_DP, overlap_cnt)
                img = np.copy(img_SO)
            elif CP_bool and np.shape(overlap_cnt)[0] == 0 and np.shape(piece_cnt)[0] == 12:
                CP_time = time.clock()
                classify_successful, Piece = F_1.Classify_Pieces(img_B, piece_cnt)
                CP_time = time.clock() - CP_time
                if classify_successful:
                    CP_bool = False
                    img_CLA = F_2.Draw_Classification(Piece)
                    cv2.imshow("Classification", img_CLA)
                    print "\nClassification Time = ", CP_time*1000, " ms\n"
                    if SOLVE_bool:
                        SOLVE_time = time.clock()
                        solution_successful, Solution_Piece, img_Solution = F_2.Solve_Puzzle(Piece)
                        SOLVE_time = time.clock() - SOLVE_time
                        if solution_successful:
                            SOLVE_bool = False
                            cv2.imshow("Puzzle Solution", img_Solution)
                            print "\nSolution Time = ", SOLVE_time*1000, " ms\n"
                        else:
                            CP_bool = True
        else:
            img = F_1.Draw_Perspective_Transform_Points(frame, pts)

    # Display the resulting frame
    cv2.imshow("Puzzle",img)

    k = cv2.waitKey(1)
    if k == ord("q"):       # Quit
        break
    elif k == ord("1"):     # Recalclculate Points
        pts_min = [[0, 0], [np.inf, 0], [np.inf, np.inf], [0, np.inf]]
        Recalc_PT_bool = True
        Recalc_PT_count = 0
    elif k == ord("2"):     # Perform Perspective Transform
        PT_bool = not PT_bool
        DP_bool = False
        SO_bool = False
        CP_bool = False
        SOLVE_bool = False
    elif k == ord("3"):     # Detect Pieces
        PT_bool = True
        DP_bool = not DP_bool
        SO_bool = False
        CP_bool = False
        SOLVE_bool = False
    elif k == ord("4"):     # Seperate Overlapping Pieces
        PT_bool = True
        DP_bool = True
        SO_bool = not SO_bool
        CP_bool = False
        SOLVE_bool = False
    elif k == ord("5"):     # Classify Pieces
        PT_bool = True
        DP_bool = True
        SO_bool = True
        CP_bool = not CP_bool
        SOLVE_bool = False
    elif k == ord("6"):     # Solve Puzzle
        PT_bool = True
        DP_bool = True
        SO_bool = True
        CP_bool = True
        SOLVE_bool = not SOLVE_bool
    elif k == ord("k"):     # Capture Images
        folder = "images"
        cv2.imwrite(folder+"\\OG.png",frame)
        if DP_bool:
            cv2.imwrite(folder+"\\PT.png",img_C)
            cv2.imwrite(folder+"\\B.png",img_B)
            cv2.imwrite(folder+"\\BIN.png",img_BIN)
            cv2.imwrite(folder+"\\DP.png",img_DP)
            if img_SO != []:
                cv2.imwrite(folder+"\\SO.png",img_SO)
            if img_CLA != []:
                cv2.imwrite(folder+"\\CLA.png",img_CLA)
            if img_Solution != []:
                cv2.imwrite(folder+"\\SOL.png",img_Solution)

# When everything done, release the capture
cv2.destroyAllWindows()