#imporing the necessary libraries
import random
import numpy as np
import re

#defining the global variables
player_board = [["\033[34m☐\033[0m" for _ in range(10)] for _ in range(10)]
cpu_board = [["\033[34m☐\033[0m" for _ in range(10)] for _ in range(10)]

valid_cpu_shots = [(i,j) for j in range(10) for i in range(10)]

letters_to_nums = {"A":1, "B":2, "C":3, "D":4, "E":5, "F":6, "G":7, "H":8, "I":9, "J":10}
nums_to_letters = {value:key for key, value in letters_to_nums.items()}

player_ships_sunk = 0
cpu_ships_sunk = 0
hit_or_miss = ""
consecutive_invalid_ships = 0

cpu_ships = []
player_ships = []
temp_ships = []
ship_lengths = [5, 4, 3, 3, 2]
unsunk_ships_lengths = ship_lengths.copy()

cpu_hits = []
temp_cpu_hits = []
cpu_misses = []
cpu_sunk_ships = []

def print_board(board, board_name):
    """
    print_board prints a board corresponding to the board list it is parsed.

    :board: a 2D list of strings representing the board
    :board_name: the name of the board (player or cpu)
    """ 
    #labels the board with either the player or cpu board
    print(f"\n{board_name} ship board:")
    #prints the column numbers
    print("  1 2 3 4 5 6 7 8 9 10")
    #prints the board with the row letters (prints 10 rows)
    for i in range(10):
        #prints the current row letter from the dictionary
        print(nums_to_letters.get(i+1), end=' ')
        #prints the current row of the board
        for j in range(10):
            print(board[i][j], end=" ")
        #prints a new line after each row
        print('\n', end='')

def print_result():
    """
    print_result prints either hit or miss depending on the result of the current turn.
    """ 
    global initial_player_ships_sunk, initial_cpu_ships_sunk
    #prints a line of 10 "~" before printing the most recent result, following by another line of 10 "~"
    print("\n"+("~" * 10))
    print(f"{hit_or_miss}!")
    if initial_player_ships_sunk != player_ships_sunk:
        print(f"CPU sunk a ship! {player_ships_sunk}/5 ships sunk.")
        initial_player_ships_sunk = player_ships_sunk
    elif initial_cpu_ships_sunk != cpu_ships_sunk:
        print(f"You sunk a ship! {cpu_ships_sunk}/5 ships sunk.")
        initial_cpu_ships_sunk = cpu_ships_sunk
    print("~" * 10)

def wait_for_input():
    """
    wait_for_input prints an input to make sure the user is ready to continue. Sometimes the 
    game can be too fast for the user to keep up, so wait_for_input breaks things up.
    """ 
    #waits for the user to press enter before continuing
    input("\nPress enter to continue...")
    print("")

def player_move():
    """
    player_move prompts the user to make a move and checks if the move is valid.
    """ 
    while True:
        #try block to catch any errors that may occur
        try:
            #prompts the user to make a move and strips any whitespace
            move = input("Make a Move! (eg, A1): ").strip().upper()
            match = re.match(r"([A-J])(\d+)", move)
            #splits the move into a row and column

            if match:
                row, col = match.groups()
                col = int(col)
                #converts the row to the corresponding number using the dictionary
                row = letters_to_nums.get(row)
                #checks if the column is valid
                if col < 1 or col > 10:
                    raise ValueError("Invalid column. Use numbers 1-10.")
            else:
                raise ValueError("Invalid move. Use letters A-J and numbers 1-10 (eg, A1).")

            #checks if the move is a hit or miss or if the user has already guessed the location
            if cpu_board[row-1][col-1] == "\033[34m☐\033[0m":
                is_hit = check_hit("player", (row-1,col-1), cpu_ships)
                cpu_board[row-1][col-1] = "\033[31mX\033[0m" if is_hit else "0"
                break
            else:
                print("You already guessed here!")

        #catches any errors that may occur
        except ValueError as ve:
            print(f"Invalid move: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def generate_possible_board():
    """
    generate_possible_board generates a possible board for the cpu to make a move.
    """ 
    global temp_ships, consecutive_invalid_ships
    temp_ships = []
    #if cpu_hits contains hits. If true, the cpu will try to create a ship based on the hits and the current board state
    if (cpu_hits):
        hit_ship_created = False
        while not hit_ship_created:
            first_hit = cpu_hits[0]
            #if there are more than 1 hits and the length of the hits is less than the max length of the unsunk ships and the amount consecutive invalid ships is less than 1000
            if len(cpu_hits) > 1 and len(cpu_hits) < max(get_unsunk_ships_lengths(player_ships)) and consecutive_invalid_ships < 1000 :
                hit_ship_length = len(cpu_hits) + 1
                #checks if the rows and columns are the same by placing the hits in a set
                rows = {hit[1] for hit in cpu_hits}
                cols = {hit[0] for hit in cpu_hits}

                #if the rows are the same, the ship is placed horizontally
                if len(rows) == 1:	
                    min_col = min(hit[0] for hit in cpu_hits)
                    max_col = max(hit[0] for hit in cpu_hits)
                    #randomly chooses to extend the ship to the left or right
                    ship_extend = random.choice([-1, 1])
                    ship_coords = [(min_col - 1 + i, first_hit[1]) for i in range(hit_ship_length)] if ship_extend == -1 else [(max_col + 1 - (hit_ship_length - 1) + i, first_hit[1]) for i in range(hit_ship_length)]
                #if the columns are the same, the ship is placed vertically
                elif len(cols) == 1:
                    min_row = min(hit[1] for hit in cpu_hits)
                    max_row = max(hit[1] for hit in cpu_hits)
                    #randomly chooses to extend the ship up or down
                    ship_extend = random.choice([-1, 1])
                    ship_coords = [(first_hit[0], min_row - 1 + i) for i in range(hit_ship_length)] if ship_extend == -1 else [(first_hit[0], max_row + 1 - (hit_ship_length - 1) + i) for i in range(hit_ship_length)]

            elif len(cpu_hits) <= 1:
                #assumes the ship is the length of 2
                hit_ship_length = 2
                #randomly chooses where to place the hit on the hypothetical ship
                coord_position = random.randint(0, 1)
                #randomly chooses to place the ship horizontally or vertically
                ship_direction = random.choice(["horizontal", "vertical"])
                #if the ship is placed horizontally, the ship is created, with the new position to the left or right of the hit
                if ship_direction == "horizontal":
                    start_col = first_hit[1] - coord_position
                    end_col = start_col + hit_ship_length - 1
                    ship_coords = [(first_hit[0], j) for j in range(start_col, end_col + 1)]
                #if the ship is placed vertically, the ship is created, with the new position above or below the hit
                else:
                    start_row = first_hit[0] - coord_position
                    end_row = start_row + hit_ship_length - 1
                    ship_coords = [(i, first_hit[1]) for i in range(start_row, end_row + 1)]
            #if the first two conditions are not met, the cpu assumes that it has hit across multiple ships and must reevaluate the ship placement
            else:   
                #if the temp_cpu_hits list is empty, the cpu assumes adds its first hit from cpu_hits to the list
                if not temp_cpu_hits: 
                    temp_cpu_hits.append(cpu_hits[0])
                if len(temp_cpu_hits) == 1:
                    #assumes the ship is the length of 2
                    hit_ship_length = 2
                    #randomly chooses where to place the hit on the hypothetical ship
                    coord_position = random.randint(0, 1)
                    ship_direction = random.choice(["horizontal", "vertical"])
                    if ship_direction == "horizontal":
                        start_col = first_hit[1] - coord_position
                        end_col = start_col + hit_ship_length - 1
                        ship_coords = [(first_hit[0], j) for j in range(start_col, end_col + 1)]
                    else:
                        start_row = first_hit[0] - coord_position
                        end_row = start_row + hit_ship_length - 1
                        ship_coords = [(i, first_hit[1]) for i in range(start_row, end_row + 1)]
                else:
                    hit_ship_length = len(temp_cpu_hits) + 1
                    rows = {hit[1] for hit in temp_cpu_hits}
                    cols = {hit[0] for hit in temp_cpu_hits}

                    if len(rows) == 1:	
                        min_col = min(hit[0] for hit in temp_cpu_hits)
                        max_col = max(hit[0] for hit in temp_cpu_hits)
                        ship_extend = random.choice([-1, 1])
                        ship_coords = [(min_col - 1 + i, first_hit[1]) for i in range(hit_ship_length)] if ship_extend == -1 else [(max_col + 1 - (hit_ship_length - 1) + i, first_hit[1]) for i in range(hit_ship_length)]
                    elif len(cols) == 1:
                        min_row = min(hit[1] for hit in temp_cpu_hits)
                        max_row = max(hit[1] for hit in temp_cpu_hits)
                        ship_extend = random.choice([-1, 1])
                        ship_coords = [(first_hit[0], min_row - 1 + i) for i in range(hit_ship_length)] if ship_extend == -1 else [(first_hit[0], max_row + 1 - (hit_ship_length - 1) + i) for i in range(hit_ship_length)]
            
            if valid_ship(ship_coords, temp_ships) and not any(coord in cpu_misses for coord in ship_coords) and not any(coord in cpu_sunk_ships for coord in ship_coords):
                if not(temp_cpu_hits):
                    consecutive_invalid_ships = 0 
                temp_ships.append(ship_coords)
                hit_ship_created = True
            else:
                consecutive_invalid_ships += 1
    else:
        for ship_length in get_unsunk_ships_lengths(player_ships):
            ship_created = False
            while not ship_created:
                ship_start = random.choice(valid_cpu_shots)
                ship_direction = random.randint(1,4)

                ship_coords = create_ship(ship_start, ship_direction, ship_length)

                if valid_ship(ship_coords, temp_ships) and not any(coord in cpu_misses for coord in ship_coords) and not any(coord in cpu_sunk_ships for coord in ship_coords):
                    temp_ships.append(ship_coords)
                    ship_created = True


def cpu_move():
    print("Calculating CPU move...")
    heatmap = np.zeros((10,10))
    number_of_runs = 10000
    progress_bar(0, number_of_runs)
    for current_run in range(number_of_runs):
        generate_possible_board()
        
        cpu_test_shot = (random.randint(0,9), random.randint(0,9))

        while cpu_test_shot in cpu_misses or cpu_test_shot in cpu_hits or cpu_test_shot in temp_cpu_hits or cpu_test_shot in cpu_sunk_ships:
            cpu_test_shot = (random.randint(0,9), random.randint(0,9))
            
        for ship in temp_ships:
            if cpu_test_shot in ship:
                heatmap[cpu_test_shot] += 1
        if current_run % 100 == 0:
            progress_bar(current_run, number_of_runs)
    progress_bar(number_of_runs, number_of_runs)
    print("")

    row, col = np.unravel_index(np.argmax(heatmap, axis=None), heatmap.shape)
    valid_cpu_shots.remove((row, col))
    is_hit = check_hit("cpu", (row, col), player_ships)
    if is_hit and player_board[row][col] != "\033[31mX\033[0m":
        player_board[row][col] = "\033[31mX\033[0m"
        if len(temp_cpu_hits) == 0:
            cpu_hits.append((row,col))
        else:
            temp_cpu_hits.append((row,col))
    elif player_board[row][col] not in ["\033[31mX\033[0m", "\033[90mX\033[0m"]:
        player_board[row][col] = "0"
        cpu_misses.append((row,col))
    print_board(player_board, "PLAYER")
    print(f"\nCPU shoots at: {nums_to_letters[row+1]},{col+1}")
    if previous_player_ships_sunk < player_ships_sunk:
        update_hits()
    print_result()


def update_hits():
    global cpu_hits

    cpu_hits = list(set(cpu_hits) | set(temp_cpu_hits))
    temp_cpu_hits.clear()

    sunk_ships = []
    for ship in player_ships_constants:
        if all(hit in cpu_hits for hit in ship):
            sunk_ships.extend(ship)

    cpu_sunk_ships.extend(sunk_ships)
    cpu_hits = [hit for hit in cpu_hits if hit not in sunk_ships]

    cpu_hits = list(set(cpu_hits) - set(cpu_sunk_ships))

def create_ship(ship_start, ship_direction, ship_length):
    row, col = ship_start

    if ship_direction == 1:
        return [(row - i, col) for i in range(ship_length)]
    elif ship_direction == 2: 
        return [(row + i, col) for i in range(ship_length)]
    elif ship_direction == 3:
        return [(row, col - i) for i in range(ship_length)]
    elif ship_direction == 4:
        return [(row, col + i) for i in range(ship_length)]

def valid_ship(ship_coords, ships):

    for row, col in ship_coords:
        if row < 0 or row >= 10 or col < 0 or col >= 10:
            return False
        for ship in ships:
            if (row, col) in ship:
                return False
    
    return True

def check_hit(player_type, move, ships):
    global player_ships_sunk, cpu_ships_sunk, hit_or_miss, consecutive_invalid_ships
    hit_or_miss = "MISS"
    for ship in ships:
        if move in ship:
            hit_or_miss = "HIT"
            ship.remove(move)
            if not ship:
                if player_type == "player":
                    cpu_ships_sunk+=1
                else:
                    player_ships_sunk+=1
                    consecutive_invalid_ships = 0
            return True
    return False

def check_player_ships(ship_name, ship_length):
    ship_created = False
    while not ship_created:
        try:
            ship_start = input(f"\nShip: {ship_name}\nLength: {ship_length}\nEnter Starting Coordinate (eg A1): ").strip().upper()
            if not ship_start:
                raise ValueError("Input cannot be empty.")

            match = re.match(r"([A-J])(\d+)", ship_start)
            #splits the move into a row and column
            if match:
                row, col = match.groups()
                col = int(col)-1
                #converts the row to the corresponding number using the dictionary
                row = letters_to_nums.get(row)-1
                #checks if the column is valid
                if col < 0 or col > 9:
                    raise ValueError("Invalid column. Use numbers 1-10.")
            else:
                raise ValueError("Invalid move. Use letters A-J and numbers 1-10 (eg, A1).")

            ship_direction = int(input("Enter ship direction (1 = Up, 2 = Down, 3 = Left, 4 = Right): "))

            if ship_direction not in [1, 2, 3, 4]:
                raise ValueError("Invalid direction. Choose 1-4.")

            ship_coords = create_ship((row, col), ship_direction, ship_length)

            if valid_ship(ship_coords, player_ships):
                player_ships.append(ship_coords)
                for coord in ship_coords:
                    row, col = coord
                    player_board[row][col] = "\033[90mX\033[0m"
                ship_created = True
            else:
                print("\nThat is not a valid ship placement, try again.")

        except ValueError as ve:
            print(f"Invalid input: {ve}")
        except Exception as e:
            print(f"Unexpected error: {e}")

def get_unsunk_ships_lengths(ships):
    return [ship_lengths[i] for i in range(len(ships)) if ships[i]]  

def progress_bar(progress, total):
    percentage = 100 * (progress/float(total))
    bar = "█" * int(percentage) + "-" * (100 - int(percentage))
    print(f"\r|{bar}| {percentage:.0f}%", end="\r")

def generate_cpu_ships():
    for ship_length in ship_lengths:
        ship_created = False
        while not ship_created:
            ship_start = (random.randint(0,9), random.randint(0,9))
            ship_direction = random.randint(1,4)

            ship_coords = create_ship(ship_start, ship_direction, ship_length)

            if valid_ship(ship_coords, cpu_ships):
                cpu_ships.append(ship_coords)
                ship_created = True

#Title Screen
print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\033[34m Monte Carlo \033[0m|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
print("██████╗░░█████╗░████████╗████████╗██╗░░░░░███████╗░██████╗██╗░░██╗██╗██████╗░░██████╗")
print("██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║░░░░░██╔════╝██╔════╝██║░░██║██║██╔══██╗██╔════╝")
print("██████╦╝███████║░░░██║░░░░░░██║░░░██║░░░░░█████╗░░╚█████╗░███████║██║██████╔╝╚█████╗░")
print("██╔══██╗██╔══██║░░░██║░░░░░░██║░░░██║░░░░░██╔══╝░░░╚═══██╗██╔══██║██║██╔═══╝░░╚═══██╗")
print("██████╦╝██║░░██║░░░██║░░░░░░██║░░░███████╗███████╗██████╔╝██║░░██║██║██║░░░░░██████╔╝")
print("╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░╚══════╝╚══════╝╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░░░░╚═════╝░")
print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\033[34m Jack Preston \033[0m|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
input("\033[33mPress enter to begin...\033[0m")

#User defined ship placement for the player ships
print("PLACE YOUR SHIPS:")
print_board(player_board, "PLAYER")
check_player_ships("Carrier", 5)
print_board(player_board, "PLAYER")
check_player_ships("Battleship", 4)
print_board(player_board, "PLAYER")
check_player_ships("Cruiser", 3)
print_board(player_board, "PLAYER")
check_player_ships("Submarine", 3)
print_board(player_board, "PLAYER")
check_player_ships("Destroyer", 2)
print_board(player_board, "PLAYER")

player_ships_constants = [ship.copy() for ship in player_ships]

#Calls the function to generate the cpu ships
generate_cpu_ships()

initial_player_ships_sunk = player_ships_sunk
initial_cpu_ships_sunk = cpu_ships_sunk

#Game loop
game_over = False
while not game_over:
    print_board(cpu_board, "CPU")
    player_move()
    print_board(cpu_board, "CPU")
    print_result()
    if cpu_ships_sunk == 5:
        game_over = True
        print("\n"+("~" * 10))
        print("You Win!")
        print("~" * 10)
        break
    wait_for_input()
    previous_player_ships_sunk = player_ships_sunk
    cpu_move()
    if player_ships_sunk == 5:
        game_over = True
        print("\n"+("~" * 10))
        print("You Lose!")
        print("~" * 10)
        break
    wait_for_input()