import numpy
import pdb

#initial_phase = "lnsgkgsnl/1r5b1/ppppppppp/9/9/9/PPPPPPPPP/1B5R1/LNSGKGSNL w - 0"

class USI_Protocol:

    def __init__(self, initial_phase_, moves_):

        self.__moves            = moves_
        self.__none_piece       = [str(i + 1) for i in range(9)]
        self.__line_str         = ["a", "b", "c", "d", "e", "f", "g", "h", "i"]
        self.__promote          = "+"
        self.__from_piece_stand = "*"

        self.__total_piece = ["K", "R", "B", "G", "S", "N", "L", "P","k", "r", "b", "g", "s", "n", "l", "p"]

        self.__phases = []
        self.__phases.append(list(initial_phase_))

        self.__board           = []
        self.__turn            = []
        self.__piece_stand_str = []
        self.__num_moves       = []

        b, t, ps, nm = self.__Cvt_phase(initial_phase_)

        self.__board.append(b)
        self.__turn.append(t)
        self.__piece_stand_str.append(ps)
        self.__piece_stand_dict = self.__init_piece_stand_dict(ps)
        self.__num_moves.append(nm)

    def __Cvt_phase(self, phase_):

        board, turn, own_piece, num_moves = self.__SplitPhase(phase_)
        cvted_board = numpy.zeros([9, 9], dtype = object)
        for cnt, i in enumerate(board):

            cvted = self.__Cvt_board_line(i)
            cvted_board[cnt, :] = cvted

        return cvted_board, turn, own_piece, num_moves

    def __SplitPhase(self, phase_):

        splited = phase_.split(" ")
        if len(splited) != 4:

            print("invalid phase")
            print(phase)
            pdb.set_trace()

        else:

            board = splited[0].split("/")
            if len(board) != 9:

                print("invalid board")
                print(splited[0])
                pdb.set_trace()

            return board, splited[1], splited[2], int(splited[3])

    def __Cvt_board_line(self, line_):

        cvted = []
        for l in line_:
            if l in self.__none_piece:

                for _ in range(int(l)):

                    cvted.append("")
            else:

                if len(cvted) > 0 and cvted[-1] == self.__promote:

                    cvted[-1] += l
                else:

                    cvted.append(l)

        return numpy.array(cvted)

    def __init_piece_stand_dict(self, piece_stand_):

        if piece_stand_ == "-":

            num_piece_stand = [0 for i in range(len(self.__total_piece))]
            return dict(zip(self.__total_piece, num_piece_stand))

        else:

            print("ToDo: __init_piece_stand_dict")
            pdb.set_trace()

    def GetPhases(self):

        for m in self.__moves:

            if self.__from_piece_stand in m:

                use_piece_, to_line, to_col = self.__Cvt_move_from_piece_stand(m, self.__turn[-1])
                self.__Update_from_piece_stand(use_piece_, to_line, to_col)

            else:

                from_line, from_col, to_line, to_col, is_promote = self.__Cvt_move_not_from_piece_stand(m)
                self.__Update_not_from_piece_stand(from_line, from_col, to_line, to_col, is_promote)

        phases = self.__Create_phase()
        return phases

    def __Cvt_move_not_from_piece_stand(self, move_):

        from_line = int(self.__line_str.index(move_[1]))
        from_col  = 9 - int(move_[0])

        to_line = int(self.__line_str.index(move_[3]))
        to_col  = 9 - int(move_[2])

        is_promote = False
        if self.__promote in move_:

            is_promote = True

        check = [from_line, from_col, to_line, to_col]
        for c in check:

            if not self.__CheckIndex(c):

                print("Invalid index")
                print(c)
                pdb.set_trace()

        return from_line, from_col, to_line, to_col, is_promote

    def __Cvt_move_from_piece_stand(self, move_, turn_):

        splited = move_.split(self.__from_piece_stand)
        piece = splited[0]
        if turn_ == "b":

            piece = piece.swapcase()

        to_line = int(self.__line_str.index(splited[1][1]))
        to_col  = 9 - int(splited[1][0])

        check = [to_line, to_col]
        for c in check:

            if not self.__CheckIndex(c):

                print("Invalid index")
                print(c)
                pdb.set_trace()

        return piece, to_line, to_col

    def __CheckIndex(self, index_):

        if 0 <= index_ and index_ < 9:

            return True
        else:

            return False

    def __Update_not_from_piece_stand(self, from_line_, from_col_, to_line_, to_col_, is_promote_):

        self.__Update_turn()
        self.__Update_num_moves()
        get_piece = self.__Update_board_not_from_piece_stand(from_line_, from_col_, to_line_, to_col_, is_promote_)
        self.__Update_piece_stand(get_piece, None)

    def __Update_from_piece_stand(self, use_piece_, to_line_, to_col_):

        self.__Update_turn()
        self.__Update_num_moves()
        self.__Update_piece_stand(None, use_piece_)
        self.__Update_board_from_piece_stand(use_piece_, to_line_, to_col_)

    def __Update_turn(self):

        if self.__turn[-1] == "w":

            self.__turn.append("b")
        elif self.__turn[-1] == "b":

            self.__turn.append("w")

    def __Update_num_moves(self):

        self.__num_moves.append(self.__num_moves[-1] + 1)

    def __Update_board_not_from_piece_stand(self, from_line_, from_col_, to_line_, to_col_, is_promote_):

        b = numpy.copy(self.__board[-1])
        from_piece = b[from_line_, from_col_]
        to_piece = b[to_line_, to_col_]

        get_piece = None
        if not to_piece == "":

            get_piece = to_piece
            get_piece = get_piece.replace(self.__promote, "")
            get_piece = get_piece.swapcase()

        b[from_line_, from_col_] = ""
        if not is_promote_:

            b[to_line_, to_col_] = from_piece
        else:

            b[to_line_, to_col_] = self.__promote + from_piece

        self.__board.append(b)

        return get_piece

    def __Update_board_from_piece_stand(self, use_piece_, to_line_, to_col_):

        b = numpy.copy(self.__board[-1])
        if b[to_line_, to_col_] == "":

            b[to_line_, to_col_] = use_piece_
        else:

            print("Can not use")
            pdb.set_trace()

        self.__board.append(b)

    def __Update_piece_stand(self, get_piece_, use_piece_):

        if use_piece_ == None:

            if get_piece_ != None:

                for i in self.__piece_stand_dict:

                    if i == get_piece_:

                        self.__piece_stand_dict[i] += 1

                pss = ""
                for i in self.__piece_stand_dict:

                    if self.__piece_stand_dict[i] == 1:

                        pss += i
                    elif self.__piece_stand_dict[i] >= 2:

                        pss += i + str(self.__piece_stand_dict[i])
                self.__piece_stand_str.append(pss)

            else:

                self.__piece_stand_str.append(self.__piece_stand_str[-1])

        else:

            for i in self.__piece_stand_dict:

                if i == use_piece_:

                    self.__piece_stand_dict[i] -= 1

            pss = ""
            for i in self.__piece_stand_dict:

                if self.__piece_stand_dict[i] == 1:

                    pss += i
                elif self.__piece_stand_dict[i] >= 2:

                    pss += i + str(self.__piece_stand_dict[i])
            self.__piece_stand_str.append(pss)

    def __Create_phase(self):

        phase = []

        for cnt, b in enumerate(self.__board):

            NL = ""
            for i in range(9):

                line = list(b[i])
                nl = ""

                for cnt_0, l in enumerate(line):

                    if l == "":

                        end = False
                        num_emp = 0
                        tmp_l = list(line[cnt_0:])
                        for cnt_1, tl in enumerate(tmp_l):

                            if not end:

                                if tl == "":

                                    line[cnt_0 + cnt_1] = "-1"
                                    num_emp += 1
                                else:

                                    end = True
                        nl += str(num_emp)

                    elif l != "-1":

                        nl += l
                NL += nl + "/"

            NL = NL[0: len(NL) - 1] + " " + self.__turn[cnt] + " " + self.__piece_stand_str[cnt] + " " + str(self.__num_moves[cnt]) + "\n"
            phase.append(NL)

        return phase