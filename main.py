

import pygame
from game import Game

def main():

    g = Game()
    while g.running:
        g.run()

if __name__ == "__main__":
    main()
