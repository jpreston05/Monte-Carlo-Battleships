import random

player_board = [["☐" for _ in range(10)] for _ in range(10)]
letters_to_nums = {"A":1, "B":2, "C":3, "D":4, "E":5, "F":6, "G":7, "H":8, "I":9, "J":10}
nums_to_letters = {value:key for key, value in letters_to_nums.items()}

sunk_ships = 0

opponent_ships = []
ship_lengths = [5, 4, 3, 3, 2, 2]

def print_board():
    print("  1 2 3 4 5 6 7 8 9 10")
    for i in range(10):
        print(nums_to_letters.get(i+1), end=' ')
        for j in range(10):
            print(player_board[i][j], end=" ")
        print('\n', end='')

def player_move():
    try:

        move = input("Make a Move! (eg: A,1): ").strip()
        row, col = move.split(",")
        col = int(col)
        row = letters_to_nums.get(row.upper())

        if row is None:
            raise ValueError("Invalid row. Use letters A-J.")
        if col < 1 or col > 10:
            raise ValueError("Invalid column. Use numbers 1-10.")

        if player_board[row-1][col-1] == "☐":
            is_hit = check_hit((row-1,col-1))
            player_board[row-1][col-1] = "\033[31mX\033[0m" if is_hit else "0"
        else:
            print("You already guessed here!")

    except ValueError as ve:
        print(f"Invalid move: {ve}")
    except Exception as e:
        print(f"Unexpected error: {e}")

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

def check_hit(player_move):
    global sunk_ships
    for ship in opponent_ships:
        if player_move in ship:
            print("\n~~~~~~~~~~")
            print("HIT!")
            ship.remove(player_move)
            if not ship:
                sunk_ships+=1
                print(f"The ship is sunk! {sunk_ships}/6 ships sunk")
            print("~~~~~~~~~~\n")
            return True
    print("\n~~~~~~~~~~")
    print("MISS!")
    print("~~~~~~~~~~\n")
    return False

for ship_length in ship_lengths:
    ship_created = False
    while not ship_created:
        ship_start = (random.randint(0,9), random.randint(0,9))
        ship_direction = random.randint(1,4)

        ship_coords = create_ship(ship_start, ship_direction, ship_length)

        if valid_ship(ship_coords, opponent_ships):
            opponent_ships.append(ship_coords)
            ship_created = True

#for i, ship in enumerate(opponent_ships, start=1):
#   print(f"Ship {i}: {ship}")

print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\033[34m Monte Carlo \033[0m|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
print("██████╗░░█████╗░████████╗████████╗██╗░░░░░███████╗░██████╗██╗░░██╗██╗██████╗░░██████╗")
print("██╔══██╗██╔══██╗╚══██╔══╝╚══██╔══╝██║░░░░░██╔════╝██╔════╝██║░░██║██║██╔══██╗██╔════╝")
print("██████╦╝███████║░░░██║░░░░░░██║░░░██║░░░░░█████╗░░╚█████╗░███████║██║██████╔╝╚█████╗░")
print("██╔══██╗██╔══██║░░░██║░░░░░░██║░░░██║░░░░░██╔══╝░░░╚═══██╗██╔══██║██║██╔═══╝░░╚═══██╗")
print("██████╦╝██║░░██║░░░██║░░░░░░██║░░░███████╗███████╗██████╔╝██║░░██║██║██║░░░░░██████╔╝")
print("╚═════╝░╚═╝░░╚═╝░░░╚═╝░░░░░░╚═╝░░░╚══════╝╚══════╝╚═════╝░╚═╝░░╚═╝╚═╝╚═╝░░░░░╚═════╝░")
print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|\033[34m Jack Preston \033[0m|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
input("\033[33mEnter any key/s to begin...\033[0m")
print("")

game_over = False
while not game_over:
    print_board()
    player_move()
    if sunk_ships == 6:
        game_over = True
        print_board()
        print("You Win!")