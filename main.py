#!/usr/bin/env python3
from game import PokemonGame

def main():
    """Main function to start the game."""
    print("Starting Pokémon Battle Simulator...")
    game = PokemonGame()
    game.play()

if __name__ == "__main__":
    main() 