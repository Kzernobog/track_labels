import random


class Colour:
    colours_list = ["#E53935", "#0277BD", "#388E3C", "#6A1B9A", "#FFFF00", "#EF6C00", "#6D4C41"]

    @staticmethod
    def choose_colour(n=None):
        """
        Chooses a color with n matching the position of colors_list.
        However, if n is either too large or too small (or None),
        a random color is chosen.
        :param n: (int)
        :return:
        """
        if type(n) is int and 1 <= n <= len(Colour.colours_list):
            # pick the nth color from the list
            colour_choice = Colour.colours_list[n - 1]
        else:
            # choose a color randomly
            colour_choice = random.choice(Colour.colours_list)

        # convert the color to a tuple
        h = colour_choice.lstrip('#')
        rgb_color = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

        return rgb_color


if __name__ == '__main__':
    for i in range(10):
        print(Colour.choose_colour())
