import re
import chess.engine
from stockfish import Stockfish


def parse_formal_move(formal_move, player_to_move):

    desc_to_file = {"Q":"d","K":"e","QB": "c", "KB": "f", "QKt": "b", "KKt":"g", "QR":"a","KR":"h", "Q-B": "c", "K-B": "f", "Q-Kt": "b", "K-Kt":"g", "Q-R":"a","K-R":"h"}
    # "B" as key?

    temp_1 = re.compile("([a-zA-Z(-|x)(\s)?]+)\d?")
    #extraction of the first part except number e.g. P-Q4->"P-Q","4"
    part_except_number = temp_1.match(formal_move).groups()

    temp_2 = re.compile("([a-zA-Z]+)(-|x)([a-zA-Z]+)")
    #decomposition of an ordinary move e.g. P-Q->"P","-","Q"
    move = temp_2.match(part_except_number[0]).groups()
    #print(ordinary_move[0])
    #print(ordinary_move[1])
    #print(ordinary_move[2])

    capture = False
    if move[1]=="x":
        source_piece = move[0]
        target_piece = move[2]
        capture = True
        return source_piece,target_piece,capture
    else:
        piece = move[0]

        file = move[2]
        file = desc_to_file[file]

        rank = part_except_number[0]
        rank = rank[-1]
        if player_to_move == "white":
            target_rank = int(rank)
        else:
            target_rank = 8- int(rank)+1

        #return file+str(target_rank)
        return piece, file+str(target_rank),capture

def capture(board,source_piece,target_piece):
    for m in board.legal_moves:
        if 'x' in board.san(m):  # is it a capture?
            # print(board.san(m))
            # current_move = board.parse_san(m)
            from_square = m.from_square
            to_square = m.to_square
            captures = board.piece_at(from_square)
            captured = board.piece_at(to_square)
            if str(captures) == source_piece and str(captured) == target_piece:
                print(str(captures) + "\tcaptures\t" + str(captured))
                board.push(m)
                break

                # end of for loop
    return

def play_move_sequence(move_sequence,initial_board_fen):
    board = chess.Board(initial_board_fen)
    for j in range(len(move_sequence)):
        print(move_sequence[j][1])
        formal_move = parse_formal_move(move_sequence[j][1], "white")
        if formal_move[2] == False:
            if formal_move[0] == "P":
                board.push_san(formal_move[1])
            else:
                if formal_move[0] == "Kt":
                    formal_move[0] = "N"
                board.push_san(formal_move[0] + formal_move[1])
        else:
            capture(board, formal_move[0], formal_move[1].lower())
        print(formal_move)
        print(board)
        if move_sequence[j][2] == "?":
            break
        print(move_sequence[j][2])
        formal_move = parse_formal_move(move_sequence[j][2], "black")
        if formal_move[2] == False:
            if formal_move[0] == "P":
                board.push_san(formal_move[1])
            else:
                if formal_move[0] == "Kt":
                    board.push_san("N" + formal_move[1])
                else:
                    board.push_san(formal_move[0] + formal_move[1])
        else:
            capture(board, formal_move[0].lower(), formal_move[1])
        print(formal_move)
        print(board)
    return


move_sequence = [(' 1. ', 'P-K4', 'P-K4'), (' 2. ', 'P-Q4', 'PxP'), (' 3. ', 'QxP', 'Kt-QB3'), (' 4. ', 'Q-K3', 'Kt-KB3'), (' 5. ', 'P-KR3', '?')]
whole_move_sequence = [(' 1. ', 'P-K4', 'P-K4'), (' 2. ', 'P-Q4', 'PxP'), (' 3. ', 'QxP', 'Kt-QB3'), (' 4. ', 'Q-K3', 'Kt-KB3'), (' 5. ', 'P-KR3', '?'),
(' 5. ', '...', 'B-K2'), (' 6. ', 'P-QR3?', '?'), (' 6. ', '...', 'Castles'), (' 7. ', 'B-B', '4'), (' 7. ', '...', 'R-K1'), (' 8. ', 'Q-QKt', '3'),
(' 8. ', '...', 'P-Q4'), (' 9. ', 'BxP', 'KtxB'), (' 10. ', 'QxKt', 'QxQ'), (' 11. ', 'PxQ', 'B-Kt5'), (' 12. ', 'K-Q1', 'R-K8')]

play_move_sequence(move_sequence,'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')

print(parse_formal_move("P-K4", "white"))
print(parse_formal_move("PxP", "black"))
print(parse_formal_move("P-Q 4", "white"))
print(parse_formal_move("P-K3", "black"))
print(parse_formal_move("B-K2", "black"))
print(parse_formal_move("Kt-K2", "white"))

