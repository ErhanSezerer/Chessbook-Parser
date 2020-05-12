import re


def get_target_square_from_formal_move(formal_move, player_to_move):

    desc_to_file = {"Q":"d","K":"e","QB": "c", "KB": "f", "QKt": "b", "KKt":"g", "QR":"a","KR":"h", "Q-B": "c", "K-B": "f", "Q-Kt": "b", "K-Kt":"g", "Q-R":"a","K-R":"h"}

    temp_1 = re.compile("([a-zA-Z-(\s)?]+)([0-9]+)")
    #extraction of the first part except number e.g. P-Q4->"P-Q","4"
    part_except_number = temp_1.match(formal_move).groups()

    temp_2 = re.compile("([a-zA-Z]+)(-)([a-zA-Z]+)")
    #decomposition of an ordinary move e.g. P-Q->"P","-","Q"
    ordinary_move = temp_2.match(part_except_number[0]).groups()
    #print(ordinary_move[0])
    #print(ordinary_move[1])
    #print(ordinary_move[2])

    file = ordinary_move[2]
    file = desc_to_file[file]

    rank = part_except_number[1]
    if player_to_move == "white":
        target_rank = int(rank)
    else:
        target_rank = 8- int(rank)+1

    return file+str(target_rank)

print(get_target_square_from_formal_move("P-Q 4", "white"))
print(get_target_square_from_formal_move("P-K3", "black"))
print(get_target_square_from_formal_move("Kt-KB3", "black"))
print(get_target_square_from_formal_move("B-K2", "black"))
print(get_target_square_from_formal_move("Kt-K2", "white"))
