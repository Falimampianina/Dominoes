import random
import sys
from collections import deque
from operator import itemgetter


current_player = ""


def check_if_same(domino1, domino2):
    """check if the two pieces of domino are the same"""
    if (domino1[0] == domino2[0] and domino1[1] == domino2[1]) or (domino1[0] == domino2[1] and domino1[1] == domino2[0]):
        return True
    else:
        return False


def reverse_domino(domino):
    """reverse the order of number of the domino"""
    reversed_domino = [domino[1], domino[0]]
    return reversed_domino


def is_a_double(domino):
    """check if it is a double"""
    if domino[0] == domino[1]:
        return True
    else:
        return False


def contains_double(dominos_pieces):
    """check if there are double domino in the list"""
    result = False
    for domino in dominos_pieces:
        if is_a_double(domino):
            result = True
            break
    return result


def get_highest_double(dominos_pieces):
    double_dominos = []
    for domino in dominos_pieces:
        if is_a_double(domino):
            double_dominos.append(domino)
    sorted_doubles = sorted(double_dominos, key=itemgetter(0), reverse=True)
    return sorted_doubles[0]


def max_between_double(double_domino1, double_domino2):
    """get the domino with the higher eye value"""
    if double_domino1[0] > double_domino2[0]:
        return double_domino1
    else:
        return double_domino2


def generate_domino_set():
    """generate the set of dominoes"""
    dominos_set = []
    for i in range(7):
        for j in range(7):
            d = [i, j]
            already_there = False
            for domino in dominos_set:
                if check_if_same(d, domino):
                    already_there = True
                    break
            if not already_there:
                dominos_set.append(d)
    return dominos_set


def split_set():
    """split the domino set between the players and the stock """
    dominos_set = generate_domino_set()
    random.shuffle(dominos_set)
    player_pieces = []
    computer_pieces = []
    for i in range(7):
        player_pieces.append(dominos_set.pop())
        computer_pieces.append(dominos_set.pop())
    stock_pieces = dominos_set
    return stock_pieces, player_pieces, computer_pieces


def initialize_game():
    global current_player
    while True:
        stock_pieces, player_pieces, computer_pieces = split_set()
        if contains_double(player_pieces) or contains_double(computer_pieces):
            break
        else:
            continue
    domino_snake = deque()
    if contains_double(player_pieces) and contains_double(computer_pieces):
        starting_piece = max_between_double(get_highest_double(player_pieces), get_highest_double(computer_pieces))
        if starting_piece in player_pieces:
            player_pieces.remove(starting_piece)
            current_player = "computer"
        else:
            computer_pieces.remove(starting_piece)
            current_player = "player"
    elif contains_double(player_pieces) and not contains_double(computer_pieces):
        starting_piece = get_highest_double(player_pieces)
        player_pieces.remove(starting_piece)
        current_player = "computer"
    else:
        starting_piece = get_highest_double(computer_pieces)
        computer_pieces.remove(starting_piece)
        current_player = "player"
    domino_snake.append(starting_piece)
    return stock_pieces, player_pieces, computer_pieces, domino_snake


def print_snake():
    output = ""
    if len(domino_snake) < 6:
        for d in domino_snake:
            output += str(d)
    else:
        for j in range(3):
            output += str(domino_snake[j])
        output += "..."
        for k in range(3):
            output += str(domino_snake[-3 + k])
    print(output)


def show_interface():
    print("=" * 70)
    print("Stock size: ", len(stock_pieces))
    print("Computer pieces: ", len(computer_pieces))
    print()
    print_snake()
    print()
    print("Your pieces:")
    for i in range(len(player_pieces)):
        print(f"{i + 1}:{player_pieces[i]}")
    print()
    if len(player_pieces) == 0:
        print("Status: The game is over. You won!")
        sys.exit(0)
    elif len(computer_pieces) == 0:
        print("Status: The game is over. The computer won!")
        sys.exit(0)
    elif len(stock_pieces) == 0:
        if is_a_draw():
            print("Status: The game is over. It's a draw!")
            sys.exit(0)
    if current_player == "player":
        print("Status: It's your turn to make a move. Enter your command.")
    else:
        print("Status: Computer is about to make a move. Press Enter to continue...")


def get_numbers_to_match():
    # get the left and the right extremity of the domino snake
    numbers_to_match = [domino_snake[0][0], domino_snake[len(domino_snake) - 1][1]]
    return numbers_to_match


def is_a_draw():
    # check if the left or the right extremity of the snack appears eight times, if so it's a draw
    draw = False
    count_0 = 0
    count_1 = 0
    for domino in domino_snake:
        if get_numbers_to_match()[0] in domino:
            count_0 += 1
    for domino in domino_snake:
        if get_numbers_to_match()[1] in domino:
            count_1 += 1
    if count_0 == 8 or count_1 == 8:
        draw = True
    return draw


def is_legal_move_right(domino):
    # check if the chosen piece is matching the right extremity of the snake
    legal = False
    for i in domino:
        if i == get_numbers_to_match()[1]:
            legal = True
            break
    return legal


def is_legal_move_left(domino):
    # check if the chosen piece is matching the left extremity of the snake
    legal = False
    for i in domino:
        if i == get_numbers_to_match()[0]:
            legal = True
            break
    return legal


def make_a_move(command):
    if current_player == "player":
        if command == 0:
            if stock_pieces:
                player_pieces.append(stock_pieces.pop())
        # if the command is a negative number, it means that the player put his piece on the left extremity
        elif command < 0:
            if player_pieces[(command * (-1)) - 1][0] == get_numbers_to_match()[0]:
                domino_snake.appendleft(reverse_domino(player_pieces[(command * (-1)) - 1]))
            else:
                domino_snake.appendleft(player_pieces[(command * (-1)) - 1])
            player_pieces.remove(player_pieces[(command * (-1)) - 1])
        else:
            if player_pieces[command - 1][1] == get_numbers_to_match()[1]:
                domino_snake.append(reverse_domino(player_pieces[command - 1]))
            else:
                domino_snake.append(player_pieces[command - 1])
            player_pieces.remove(player_pieces[command - 1])


def change_player():
    global current_player
    if current_player == "player":
        current_player = "computer"
    else:
        current_player = "player"


def player_play():
    """the player plays in which he takes a piece from the stock or take a piece from
       his pieces and put it on an extremity of the domino snake"""
    global current_player
    # show_interface()
    while True:
        try:
            command = int(input())
            # if the command doesn't match a valid option, the program wait for another input
            if command < (0 - len(player_pieces)) or command > len(player_pieces):
                print("Invalid input. Please try again.")
                continue
            elif command == 0:
                break
            else:
                if command < 0 and is_legal_move_left(player_pieces[abs(command) - 1]):
                    break
                elif command > 0 and is_legal_move_right(player_pieces[abs(command) - 1]):
                    break
                else:
                    print("Illegal move. Please try again.")
                    continue
        except ValueError:
            print("Invalid input. Please try again.")
    make_a_move(command)
    change_player()


def count_occurrence(number):
    # count the occurrence of every number from 0 to 6 in computer's pieces and the snake
    count = 0
    for domino in domino_snake:
        if number in domino:
            count += 1
    for d in computer_pieces:
        if number in d:
            count += 1
    return count


def get_score_of_dominos():
    # get the score of all pieces from computer combined with the stock
    number_score = []
    for i in range(7):
        # assuming that the list of score has always 7 value and the key is the index
        # while the value is the value at this index
        number_score.append(count_occurrence(i))
    domino_score = []
    for d in computer_pieces:
        domino_score.append([d, number_score[d[0]] + number_score[d[1]]])
    return domino_score


def computer_play():
    # show_interface()
    # the computer chooses the best domino piece to play
    input()
    sorted_domino_by_score = sorted(get_score_of_dominos(), key=itemgetter(1), reverse=True)
    for item in sorted_domino_by_score:
        if is_legal_move_left(item[0]):
            if item[0][0] == get_numbers_to_match()[0]:
                domino_snake.appendleft(reverse_domino(item[0]))
            else:
                domino_snake.appendleft(item[0])
            computer_pieces.remove(item[0])
            change_player()
            return
        elif is_legal_move_right(item[0]):
            if item[0][0] == get_numbers_to_match()[1]:
                domino_snake.append(item[0])
            else:
                domino_snake.append(reverse_domino(item[0]))
            computer_pieces.remove(item[0])
            change_player()
            return
        else:
            continue
    if len(stock_pieces) > 0:
        computer_pieces.append(stock_pieces.pop())
    change_player()


def play():
    if current_player == "player":
        player_play()
    elif current_player == "computer":
        computer_play()


stock_pieces, player_pieces, computer_pieces, domino_snake = initialize_game()
# print("Stock pieces: ", stock_pieces)
# print("Computer pieces: ", computer_pieces)
# print("Player pieces: ", player_pieces)
# print("Domino snake: ", domino_snake)
# print("Status: ", current_player)

while True:
    show_interface()
    play()
