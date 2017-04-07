"""
Created on Fri Jul 22 14:05:51 2016

@author: JP
"""

import numpy as np
import cv2
import Functions_1 as F_1
import Functions_2 as F_2

DEBUG_CONSOLE = False   # To view console debugging
DEBUG_SCORE = False     # To view colour score information
DEBUG_IMAGE = False     # To view image debugging

class Puzzle_Piece:
    """
    Class representing a puzzle piece and its atrebutes
    """

    def __init__(self, i, c_l, it_c, a, f_n):
        self.index = i              # Piece index
        self.solve_index = -1       # Piece solve index (-1 implies unsolved)
        self.center_location = c_l  # Center location on original puzzle image [x, y]
        self.stack_height = 1        # Hight that the piece has been stacked (1 => no stack)
        self.it_class = it_c        # Indent\tab class
        self.angle = int(a)         # Angle that needs to be applied to actual piece
        self.file_name = f_n        # Filename of piece image




    def print_index(self):
        print "This Is Puzzle Piece ", self.index
    def print_it_class(self):
        print "Puzzle Piece ", self.index,"'s Indent/Tab Class : ",self.it_class
    def print_center_location(self):
        print "Puzzle Piece ", self.index,"'s Center Location  : ",self.center_location
    def print_angle(self):
        print "Puzzle Piece ", self.index,"'s Angle            : ", self.angle, "Degrees"

    def is_corner(self):
        """
        Check if this piece is a corner piece
            Input:
            Output:     True if piece is corner piece
        """

        # Corner if it_class contains 2 zeros
        return 2 == np.count_nonzero(self.it_class)

    def is_edge(self):
        """
        Check if this piece is an edge piece
            Input:
            Output:     True if piece is edge piece
        """

        # Corner piece is not an adge piece
        if self.is_corner():
            return False

        # Edge piece if it_class contains a zero
        return 0 in self.it_class

    def corner_location(self):
        """
        Retrieve the corner location if this piece is a corner piece
            Input:
            Output:     Corner location (0 = TL; 1 = TR; 2 = BR; 3 = BL; -1 = not a corner)
        """

        # If not a corner piece
        if not self.is_corner():
            return -1

        # If top left corner
        if self.it_class[3] == 0 and self.it_class[0] == 0:
            return 0
        # If top right corner
        if self.it_class[0] == 0 and self.it_class[1] == 0:
            return 1
        # If bottom right corner
        if self.it_class[1] == 0 and self.it_class[2] == 0:
            return 2
        # If bottom left corner
        if self.it_class[2] == 0 and self.it_class[3] == 0:
            return 3


    def set_corner(self, location):
        """
        Rotate piece untill corner is at desired location
            Input:      Desired corner location (0 = TL; 1 = TR; 2 = BR; 3 = BL)
            Output:
        """

        # If not a corner piece
        if not self.is_corner():
            return

        # Rotate untill location is reached
        while self.corner_location() != location:
            self.rotate_90_ccw(1)


    def rotate_90_ccw(self, turns):
        """
        Rotates this piece 90 degrees counter-clockwise and update its parameters
            Input:      Number of desired CCW turns
            Output:
        """

######### Max piece width [Calibration Values]
        max_piece_width = 230 # 240 For hulk puzzle

        if turns > 0:
            # To ensure minimal 90 degree turns
            turns = turns%4

            # Open piece image
            img_piece = cv2.imread(self.file_name)

            # Get rotational matrix and perform ratation
            M = cv2.getRotationMatrix2D((max_piece_width/2, max_piece_width/2), 90*turns, 1)
            img_piece = cv2.warpAffine(img_piece, M, (max_piece_width, max_piece_width))

            # Save piece image
            cv2.imwrite(self.file_name, img_piece)

            # Rotate it_class array
            self.it_class = np.roll(self.it_class, -turns)

            # Adjust piece angle
            self.angle = (90*turns + self.angle)%360

    def copy(self, index):
        """
        Performs a deep copy on this piece
            Input:      Index of new piece file
            Output:     New piece
        """

        # New piece image file name
        new_file_name = "pieces\\solution\\S_"+str(index)+"\\sp_"+str(self.index)+".png"

        # Create new image
        img_piece = cv2.imread(self.file_name)
        cv2.imwrite(new_file_name, img_piece)

        return Puzzle_Piece(self.index, self.center_location, self.it_class, self.angle, new_file_name)








class Puzzle:
    """
    Class representing a puzzle and its atrebutes
    """

    def __init__(self, Start_Pieces, corner_num):
        self.Puzzle_Matrix = np.empty((5, 6), dtype=object) # Matrix to hold puzzle piece objects
        self.Fit_Matrix = np.zeros((5, 6, 4))               # Fit Matrix used to check for piece fitting
        self.Piece = []                                     # Pieces in puzzle

        # To identify the corner_num corner
        corner_count = 0

        # Make a deep copy of all pieces and set starting corner
        for i, P in enumerate(Start_Pieces):
            self.Piece.append(P.copy(corner_num))
            if self.Piece[i].is_corner():
                if corner_count == corner_num:
                    corner = self.Piece[i]
                corner_count += 1

        # Make sure corner piece is correctly oriented then insert it
        corner.set_corner(0)
        self.Puzzle_Matrix[1, 1] = corner
        self.Puzzle_Matrix[1, 1].solve_index = 0

        # Add corner piece parameters to Fit Matrix
        self.Fit_Matrix[1, 1] = np.copy(corner.it_class)
        self.Fit_Matrix[1, 2, 3] = self.Fit_Matrix[1, 1, 1]
        self.Fit_Matrix[2, 1, 0] = self.Fit_Matrix[1, 1, 2]


    def Update_Fit_Matrix(self):
        """
        Adjust the Fit Matix for all vacant spaces
            Input:
            Output:
        """

        # For entire matrix
        for y in xrange(1, 4):
            for x in xrange(1, 5):
                # Adjust only if the spot is vacant
                if self.Puzzle_Matrix[y, x] == None:
                    self.Fit_Matrix[y, x] = np.zeros(4)
                    # Adjust top value if there is a piece above it
                    if self.Puzzle_Matrix[y-1, x] != None:
                        self.Fit_Matrix[y, x, 0] = self.Fit_Matrix[y-1, x, 2]
                    # Adjust right value if there is a piece to its right
                    if self.Puzzle_Matrix[y, x+1] != None:
                        self.Fit_Matrix[y, x, 1] = self.Fit_Matrix[y, x+1, 3]
                    # Adjust bottom value if there is a piece below it
                    if self.Puzzle_Matrix[y+1, x] != None:
                        self.Fit_Matrix[y, x, 2] = self.Fit_Matrix[y+1, x, 0]
                    # Adjust left value if there is a piece left of it
                    if self.Puzzle_Matrix[y, x-1] != None:
                        self.Fit_Matrix[y, x, 3] = self.Fit_Matrix[y, x-1, 1]


    def Fit(self, y, x, p):
        """
        Calculates if piece p will fit in Puzzle Matrix location [y, x]
            Input:      Y matrix index, X matrix index, Piece p to be fitted
            Output:     True if p fits, Array containing the turns p needs to do in order to fit
        """

        # Piece p can not fit if it is already solved
        if p.solve_index != -1:
            return False, []

        # Piece p can not fit if the location is occupied
        if self.Puzzle_Matrix[y, x] != None:
            return False, []

        # Edges and corner pieces can not fit in the middle
        if y == 2 and (x == 2 or x == 3) and (p.is_corner() or p.is_edge()):
            return False, []

        # Middle piece can not fit on an edge boundary
        if (y == 1 or y == 3) and (x == 1 or x == 4) and not (p.is_corner() or p.is_edge()):
            return False, []

        # Copy p it class to prevent unwanted piece p alterations
        p_it_class = np.copy(p.it_class)

        # Array to hold all the valaid turns that result in a fit
        fit_turns = []

        # For all possible turns (1 turn = 90 degrees)
        for turn in xrange(4):
            # Mask that will ensure non-vacant edges are not compared to vacant ones
            mask = np.in1d(self.Fit_Matrix[y, x], 0)*-1 + 1

            # Adjust mask for edge boundaries as vacant boundaries need to be compared
            if y == 1:
                mask[0] = 1
            elif y == 3:
                mask[2] = 1
            if x == 1:
                mask[3] = 1
            elif x == 4:
                mask[1] = 1

            # Apply mask to copied it class
            temp_p_it_class = np.multiply(p_it_class, mask)

            # Piece p can fit if it matches the location Fit Matrix value
            if np.count_nonzero(np.add(self.Fit_Matrix[y, x], temp_p_it_class)) == 0:
                fit_turns.append(turn)

            # Try next orientation
            p_it_class = np.roll(p_it_class, -1)

        # Piece p can fit if zero or more turns will result in a fit
        if np.shape(fit_turns)[0] !=0:
            return True, fit_turns

        # If no fit is found
        return False, []


    def Insert(self, y, x, p):
        """
        Inserts piece p in Puzzle Matrix location [y, x]
            Input:      Y matrix index, X matrix index, Piece p to be inserted
            Output:
        """

        # Add piece to Puzzle Matrix and update Fit Matrix
        self.Puzzle_Matrix[y, x] = p
        self.Puzzle_Matrix[y, x].solve_index = 0
        self.Fit_Matrix[y, x] = np.copy(p.it_class)
        self.Update_Fit_Matrix()




    def Compare(self, P1, P2, position):
        """
        Calculates an edge colour comparrison value between piece P1 and P2
            Input:      Piece P1, Piece P2, Location of P2 relative to P1 (0 = Right; 1 = Below)
            Output:     Edge colour comparison value
        """

        # Can not compare None pieces
        if P1 == None or P2 == None:
            if DEBUG_CONSOLE and  DEBUG_SCORE:
                print "None piece comparison: Ret", np.inf
            return np.inf

        # Corner can not fit next to corners
        if P1.is_corner() and P2.is_corner():
            if DEBUG_CONSOLE and  DEBUG_SCORE:
                print "Corner vs. Corner comparison: Ret", np.inf
            return np.inf

        # Open each piece image
        img_1 = cv2.imread(P1.file_name)
        img_2 = cv2.imread(P2.file_name)

        # Get image dimentions
        rows, cols, chan = img_1.shape

######### Search perameters [Calibration Values]
        edge_depth = rows/2 # 120 # 80
        edge_width = rows/2 # 120 # 100

        # Histogram masks
        mask_1_upper = np.zeros(img_1.shape[:2], np.uint8)
        mask_1_lower = np.zeros(img_1.shape[:2], np.uint8)
        mask_2_upper = np.zeros(img_1.shape[:2], np.uint8)
        mask_2_lower = np.zeros(img_1.shape[:2], np.uint8)

        # If P2 is to the right of P1
        if position == 0:
            # Split edges up into two segments and use only the boundary colours
            mask_1_upper[:edge_width, cols-edge_depth:] = 255
            mask_1_lower[rows-edge_width:, cols-edge_depth:] = 255
            mask_2_upper[:edge_width, :edge_depth] = 255
            mask_2_lower[rows-edge_width:, :edge_depth] = 255

            # Extract only the foreground image segments
            img_1_upper = cv2.bitwise_and(img_1, img_1, mask = mask_1_upper)
            img_1_lower = cv2.bitwise_and(img_1, img_1, mask = mask_1_lower)
            img_2_upper = cv2.bitwise_and(img_2, img_2, mask = mask_2_upper)
            img_2_lower = cv2.bitwise_and(img_2, img_2, mask = mask_2_lower)

            # Extend mask to ignore background
            mask_1_upper = F_1.Binarise(img_1_upper)
            mask_1_lower = F_1.Binarise(img_1_lower)
            mask_2_upper = F_1.Binarise(img_2_upper)
            mask_2_lower = F_1.Binarise(img_2_lower)
        else:
            # Split edges up into two segments and use only the boundary colours
            mask_1_upper[cols-edge_depth:, :edge_width] = 255
            mask_1_lower[cols-edge_depth:, rows-edge_width:] = 255
            mask_2_upper[:edge_depth, :edge_width] = 255
            mask_2_lower[:edge_depth, rows-edge_width:] = 255

            # Extract only the foreground image segments
            img_1_upper = cv2.bitwise_and(img_1, img_1, mask = mask_1_upper)
            img_1_lower = cv2.bitwise_and(img_1, img_1, mask = mask_1_lower)
            img_2_upper = cv2.bitwise_and(img_2, img_2, mask = mask_2_upper)
            img_2_lower = cv2.bitwise_and(img_2, img_2, mask = mask_2_lower)

            # Extend mask to ignore background
            mask_1_upper = F_1.Binarise(img_1_upper)
            mask_1_lower = F_1.Binarise(img_1_lower)
            mask_2_upper = F_1.Binarise(img_2_upper)
            mask_2_lower = F_1.Binarise(img_2_lower)


######### Histogram bins [Calibration Values]
        bins = 8

        # Calculat histograms
        hist_1_upper = cv2.calcHist([img_1], [0, 1, 2], mask_1_upper, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
        hist_1_lower = cv2.calcHist([img_1], [0, 1, 2], mask_1_lower, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
        hist_2_upper = cv2.calcHist([img_2], [0, 1, 2], mask_2_upper, [bins, bins, bins], [0, 256, 0, 256, 0, 256])
        hist_2_lower = cv2.calcHist([img_2], [0, 1, 2], mask_2_lower, [bins, bins, bins], [0, 256, 0, 256, 0, 256])

        # Flatten and normalise histograms
        hist_1_upper = cv2.normalize(hist_1_upper).flatten()
        hist_1_lower = cv2.normalize(hist_1_lower).flatten()
        hist_2_upper = cv2.normalize(hist_2_upper).flatten()
        hist_2_lower = cv2.normalize(hist_2_lower).flatten()

        # Compare histograms
        CV_upper = cv2.compareHist(hist_1_upper, hist_2_upper, cv2.cv.CV_COMP_BHATTACHARYYA)
        CV_lower = cv2.compareHist(hist_1_lower, hist_2_lower, cv2.cv.CV_COMP_BHATTACHARYYA)

        if DEBUG_IMAGE:
            cv2.imshow("Compare Piece 1", img_1)
            cv2.imshow("Compare Piece 2", img_2)
            cv2.imshow("1", img_1_upper)
            cv2.imshow("2", img_1_lower)
            cv2.imshow("3", img_2_upper)
            cv2.imshow("4", img_2_lower)

        if DEBUG_CONSOLE and  DEBUG_SCORE:
            if position == 0:
                print "L Comp : HEll = T {:<8.4f}".format(CV_upper), " B {:<8.4f}".format(CV_lower), " Ret {:<8.4f}".format(CV_upper + CV_lower)
            else:
                print "T Comp : HEll = L {:<8.4f}".format(CV_upper), " R {:<8.4f}".format(CV_lower), " Ret {:<8.4f}".format(CV_upper + CV_lower)

        return CV_upper + CV_lower




    def Rotate_Matrix(self):
        """
        To ensure that a completed puzzle is 3 by 4, it has to be rotated if a 4 by 3 case arises
            Input:
            Output:
        """

        # Rotate all pieces
        for x in xrange(1, 4):
            self.Puzzle_Matrix[1, x].rotate_90_ccw(1)

        # Reorganise pieces
        for i in xrange(1, 4):
            self.Insert(4-i, 1, self.Puzzle_Matrix[1, i])
            self.Puzzle_Matrix[1, i] = None

        # Update Fit_Matrix
        self.Update_Fit_Matrix()




    def Solve_Puzzle(self):
        """
        Claculate a sullution for this puzzle
            Input:
            Output:     solution pieces in solution order, solution score
        """

        Left_Compare_Piece = self.Puzzle_Matrix[1, 1]
        Top_Compare_Piece = []

        if DEBUG_CONSOLE and DEBUG_SCORE:
            print "Piece \tLocation   \tFit  Turns"

        # For all puzzle locations
        for y in xrange(1, 4):
            # Use while loop for x coordinates so they may be altered mid-loop
            x = 1
            while x < 5:
                # Array to hold pieces that can fit in lacation [y, x]
                Fit_Piece = []

                # Set compare pieces
                Left_Compare_Piece = self.Puzzle_Matrix[y, x-1]
                Top_Compare_Piece = self.Puzzle_Matrix[y-1, x]
                if DEBUG_IMAGE:
                    if Left_Compare_Piece != None:
                        cv2.imshow("Left Compare", cv2.imread(Left_Compare_Piece.file_name))
                    if Top_Compare_Piece != None:
                        cv2.imshow("Top Compare", cv2.imread(Top_Compare_Piece.file_name))

                # For all pieses
                for i, P in enumerate(self.Piece):
                    # Check if piece P will fit in location [y, x] and, if so, what orientation it needs to be
                    fit, turns = self.Fit(y, x, P)

                    # If piece P fits in location [y, x]
                    if fit:
                        if DEBUG_CONSOLE and DEBUG_SCORE:
                            print "P[" + str(i) + "]:\t[y, x] = [" + str(y) + "," + str(x) + "]\t", fit, turns

                        # If piece P only fits in one way
                        if np.shape(turns)[0] == 1:
                            # Rotate piece P to fit in location [y, x]
                            P.rotate_90_ccw(turns[0])

                            # Add piece P to Fit_Piece array
                            Fit_Piece.append(P)

                        # If piece P fits in more than one way
                        else:
                            # Array to hold piece fit values
                            Fit_Value = []

                            if DEBUG_CONSOLE and DEBUG_SCORE:
                                print "Multi Fit!"

                            for o in xrange(np.shape(turns)[0]):
                                # Rotate piece P to fit in location [y, x]
                                P.rotate_90_ccw(turns[o])

                                if y == 1 and x != 1:
                                    # Calculate fit value using left piece
                                    Fit_Value.append(self.Compare(Left_Compare_Piece, P, 0))

                                elif x == 1:
                                    # Calculate fit value using above piece
                                    Fit_Value.append(self.Compare(Top_Compare_Piece, P, 1))

                                else:
                                    # Calculate fit value using above and left piece
                                    Fit_Value.append((self.Compare(Top_Compare_Piece, P, 1) + self.Compare(Left_Compare_Piece, P, 0))/2.0)

                                # Rotate piece back before next fit value calculation
                                P.rotate_90_ccw(4-turns[o])

                            if DEBUG_CONSOLE and DEBUG_SCORE:
                                print "TURN", turns[0], "= Fit Value {:<8.4f}".format(Fit_Value[0])
                                print "TURN", turns[1], "= Fit Value {:<8.4f}".format(Fit_Value[1]), "\n"

                            # Find the smallest fit value
                            fit_index = np.argmin(Fit_Value)

                            # Rotate piece P to most likely orientation to fit in location [y, x]
                            P.rotate_90_ccw(turns[fit_index])

                            # Add piece P to Fit_Piece array
                            Fit_Piece.append(P)


                # For all possible neighboring pieces
                if np.shape(Fit_Piece)[0] > 1:
                    # Array to hold piece fit values
                    Fit_Value = []

                    # Find colour fit value for all pieces that can fit
                    for f, F_P in enumerate(Fit_Piece):
                        if y == 1 and x != 1:
                            # Calculate fit value using left piece
                            Fit_Value.append(self.Compare(Left_Compare_Piece, F_P, 0))

                        elif x == 1:
                            # Calculate fit value using above piece
                            Fit_Value.append(self.Compare(Top_Compare_Piece, F_P, 1))

                        else:
                            # Calculate fit value using above and left piece
                            Fit_Value.append((self.Compare(Top_Compare_Piece, F_P, 1) + self.Compare(Left_Compare_Piece, F_P, 0))/2.0)


                    # Find the smallest fit value
                    fit_index = np.argmin(Fit_Value)

                    # Insert piece with smallest fit value
                    self.Insert(y, x, Fit_Piece[fit_index])
                    if DEBUG_CONSOLE:
                        print "======================================="
                        print "Piece", Fit_Piece[fit_index].index, "inserted at location [", y, ",", x, "]"
                        print "=======================================\n"

                # If only one piece can fit
                elif np.shape(Fit_Piece)[0] == 1:
                    self.Insert(y, x, Fit_Piece[0])
                    if DEBUG_CONSOLE:
                        print "======================================="
                        print "Piece", Fit_Piece[0].index, "inserted at location [", y, ",", x, "]"
                        print "=======================================\n"

                # Check if Puzzle_Matrix rotation is necessary
                if y == 1 and x == 3 and self.Puzzle_Matrix[y, x].is_corner():
                    # TODO
                    self.Rotate_Matrix()
                    if DEBUG_CONSOLE:
                        print "Matrix Rotated\n"
                    x = 1

                x += 1

        # Correctly order solution pieces
        solution_Piece = self.Index_solution()

        # If solution is not complete return []
        if solution_Piece == None:
            return [], [], []

        # Draw solution image and retrieve solution score
        img_solution, solution_score = F_2.Draw_solution(solution_Piece)

        return solution_Piece, img_solution, solution_score




    def Index_solution(self):
        """
        Lable all the solved pieces sequentially as they are to be solved
            Input:
            Output:     Array containing pieces in solution order
        """

        index = 0

        # Array to hold pieces in solution order
        solution_Piece = []

        # For entire matrix
        for y in xrange(1, 4):
            for x in xrange(1, 5):
                if self.Puzzle_Matrix[y, x] == None:
                    return None
                self.Puzzle_Matrix[y, x].solve_index = index
                index += 1

                solution_Piece.append(self.Puzzle_Matrix[y, x])

        return solution_Piece










