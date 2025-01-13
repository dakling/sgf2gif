#!/usr/bin/env python3

# usage: python sgf-to-png.py <path-to-sgf.sgf>
# will generate the output <path-to-sgf.gif>
# dependencies: numpy, matplotlib, sgf

# adapted from https://stackoverflow.com/questions/24563513/drawing-a-go-board-with-matplotlib
# and https://stackoverflow.com/questions/2318288/how-to-use-custom-png-image-marker-with-plot

import sys
import os
import shutil
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.image as mpimg
import sgf


class Goban:

    def __init__(self, input_filename):
        self.board_image = mpimg.imread("./assets/board-bg.jpeg")
        self.black_image = mpimg.imread("./assets/black.png")
        self.white_image = mpimg.imread("./assets/white.png")
        self.input_filename = input_filename
        self.output_directory = input_filename[:-4]
        self.moves = []
        try:
            shutil.rmtree(self.output_directory)
        except Exception:
            pass
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        self.output_filename = self.output_directory + "/out"
        self.sgf_to_moves()

        fig = plt.figure(figsize=[8,8])
        # ax = fig.add_subplot(111, xticks=range(19), yticks=range(19), facecolor='none', position=[.1,.1,.8,.8])
        ax = fig.add_subplot(111, facecolor='none', position=[.1,.1,.8,.8])
        ax.tick_params(which='both', top=False, bottom=False, left=False, right=False, labelleft=False, labelbottom=False)
        self.fig = fig
        self.ax = ax
        self.render_board_background()
        self.render_lines()
        self.render_star_points()


    def sgf_move_to_coordinates(self, move_string):
        assert len(move_string) == 2, "invalid move string."
        x = ord(move_string[0]) - 96
        y = ord(move_string[1]) - 96
        return (x,y)

    def sgf_to_moves(self):
        with open(self.input_filename) as f:
            collection = sgf.parse(f.read())
            for node in collection[0]:
                if 'B' in node.properties or 'W' in node.properties:
                    self.moves.append(node.properties)

    def plot_stone(self, xi, yi, image):
        assert xi >= 1 and  yi >= 1 and  xi <= 19 and  yi <= 19, "Given coordinate out of range."
        im = OffsetImage(image, zoom=60/self.ax.figure.dpi)
        im.image.axes = self.ax

        fuzzyness = 0.0
        fuzzy_offset_x = np.random.rand() * fuzzyness
        fuzzy_offset_y = np.random.rand() * fuzzyness
        ab = AnnotationBbox(im, (xi-1 + fuzzy_offset_x, yi-1 + fuzzy_offset_y), frameon=False, pad=0.0,)
        self.ax.add_artist(ab)

    def render_board_background(self):
        self.ax.imshow(self.board_image, extent=[-0.6, 18.6, -0.6, 18.6])

    def render_lines(self):
        self.ax.vlines(range(19), ymin=0.0, ymax=18, color="k")
        self.ax.hlines(range(19), xmin=0.0, xmax=18, color="k")

    def render_star_points(self):
        # plot star points
        for x in [4, 10, 16]:
            for y in [4, 10, 16]:
                self.ax.plot(x-1, y-1, "ko")

    def play_black(self, xi, yi):
        self.plot_stone(xi, yi, self.black_image)

    def play_white(self, xi, yi):
        self.plot_stone(xi, yi, self.white_image)

    def play_sgf_move(self, move_dict):
        color = list(move_dict.keys())[0]
        move = move_dict[color][0]
        if color == 'B':
            self.play_black(*self.sgf_move_to_coordinates(move))
        elif color == 'W':
            self.play_white(*self.sgf_move_to_coordinates(move))
        else:
            raise Exception("unknown color.")

    def render_as_png(self, highest_move):
        moves = self.moves[:highest_move]
        for i, move in enumerate(moves):
            self.play_sgf_move(move)
        self.fig.savefig(self.output_filename + "-" + "{:06}".format(len(moves)) + ".png")

    def render_entire_game_as_png(self):
        for i in range(len(self.moves) + 1):
            self.render_as_png(i)

    def render_entire_game(self):
        self.render_entire_game_as_png()
        os.system("magick -delay 50 " + self.output_filename + "* " + self.output_directory + ".gif" )
        shutil.rmtree(self.output_directory)

if __name__ == "__main__":


    if len(sys.argv) == 1:
        raise Exception(
            "Please indicate an sgf file to be converted."
        )
    else:
        goban = Goban(sys.argv[1])
        goban.render_entire_game()
