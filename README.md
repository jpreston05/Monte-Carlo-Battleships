# Monte Carlo Battleships
Monte Carlo Battleships is an advanced implementation of the classic game Battleship, utilizing probability-based targeting to optimize gameplay. The program employs Monte Carlo simulations to predict ship locations and improve shot accuracy over time.

# Features

  - Monte Carlo Simulation: Runs multiple simulations to estimate high-probability target areas.

  - Smart Targeting System: Adjusts strategy dynamically based on previous hits and misses.

  - Efficient Search Algorithm: Reduces random shots and focuses on high-likelihood zones.

  - Adaptive Strategy: Identifies ship orientations and refines targeting accordingly.

  - Valid Move Enforcement: Ensures shots remain within the grid and adhere to game rules.

# Installation

Clone the repository:

  git clone https://github.com/jpreston05/monte-carlo-battleships.git

Navigate to the project directory:

  cd monte-carlo-battleships

Install dependencies:

  pip install numpy

Alternatively, you can add numpy to a requirements.txt file and install using:

  pip install -r requirements.txt

# Usage

Run the game with:

  python battleships.py

# How It Works

The program initializes a standard Battleship board.

When the CPU takes a turn, it uses Monte Carlo simulations to determine the most probable ship locations based on previous hits and misses.

The CPU refines its targeting strategy, shifting from probability-based selection to direct pursuit of detected ships.

The game continues until all ships are sunk.

# Future Improvements

Improving the generate_possible_board function to work faster under specific edge cases

# License

This project is licensed under the MIT License. See the LICENSE file for details.

# Contributing

Contributions are welcome! If you have ideas for improvements or find bugs, feel free to open an issue or submit a pull request.

# Author

Jack Preston

