#!/usr/bin/env python3

# adapted from https://stackoverflow.com/questions/24563513/drawing-a-go-board-with-matplotlib
# and https://stackoverflow.com/questions/2318288/how-to-use-custom-png-image-marker-with-plot

import os
import shutil
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.image as mpimg

class Goban:

    def __init__(self, input_filename):
        self.board_image = mpimg.imread("./board-bg.jpeg")
        self.black_image = mpimg.imread("./black.png")
        self.white_image = mpimg.imread("./white.png")
        self.input_filename = input_filename
        self.output_directory = input_filename[:-4]
        try:
            shutil.rmtree(self.output_directory)
        except Exception:
            pass
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)

        self.output_filename = self.output_directory + "/out"
        self.sgf_to_moves()

    def sgf_to_moves(self):
        self.moves = [(16, 16), (4, 4), (13, 16)]

    def plot_stone(self, xi, yi, image):
        assert xi >= 1 and  yi >= 1 and  xi <= 19 and  yi <= 19, "Given coordinate out of range."
        im = OffsetImage(image, zoom=60/self.ax.figure.dpi)
        im.image.axes = self.ax

        fuzzy_offset_x = np.random.rand() * 0.02
        fuzzy_offset_y = np.random.rand() * 0.02
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

    def play_alternately(self, xi, yi, move_number):
        if move_number % 2 == 0:
            self.play_black(xi, yi)
        else:
            self.play_white(xi, yi)

    def render_as_png(self, highest_move):
        fig = plt.figure(figsize=[8,8])
        # ax = fig.add_subplot(111, xticks=range(19), yticks=range(19), facecolor='none', position=[.1,.1,.8,.8])
        ax = fig.add_subplot(111, facecolor='none', position=[.1,.1,.8,.8])
        ax.tick_params(which='both', top=False, bottom=False, left=False, right=False, labelleft=False, labelbottom=False)
        self.fig = fig
        self.ax = ax
        self.render_board_background()
        self.render_lines()
        self.render_star_points()

        moves = self.moves[:highest_move]
        for i, move in enumerate(moves):
            self.play_alternately(move[0], move[1], i)

        fig.savefig(self.output_filename + "-" + "{:06}".format(len(moves)) + ".png")

    def render_entire_game_as_png(self):
        for i in range(len(self.moves) + 1):
            self.render_as_png(i)

    def render_entire_game(self):
        self.render_entire_game_as_png()
        os.system("magick " + self.output_filename + "* " + self.output_directory + ".gif" )
        shutil.rmtree(self.output_directory)

goban = Goban("../10160932-255-cloud2016-Klingel.sgf")
goban.render_entire_game()
