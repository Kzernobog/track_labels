import random


class Colour:
    colours_list = ["#dce775", "#f57f17", "#4caf50", "#4dd0e1", "#2e7d32", "#ff5722", "#aeea00", "#18ffff", "#ff8a65"]

    @staticmethod
    def random_colour():
        # choose a color randomly
        colour_choice = random.choice(Colour.colours_list)

        # convert the color to a tuple
        h = colour_choice.lstrip('#')
        rgb_color = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

        return rgb_color


if __name__ == '__main__':
    for i in range(10):
        print(Colour.random_colour())