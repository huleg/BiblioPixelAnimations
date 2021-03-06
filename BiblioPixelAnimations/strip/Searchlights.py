from bibliopixel import LEDStrip
import bibliopixel.colors as colors
from bibliopixel.animation import BaseStripAnim

import random

class Searchlights(BaseStripAnim):
    """Three search lights sweeping at different speeds"""

    def __init__(self, led, colors=[colors.MediumSeaGreen,colors.MediumPurple,colors.MediumVioletRed], tail=5, start=0, end=-1):

        super(Searchlights, self).__init__(led, start, end)

        self._color = colors
        self._tail = tail + 1
        if self._tail >= self._size / 2:
            self._tail = (self._size / 2) - 1
        self._direction = [1,1,1]
        self._currentpos = [0,0,0]
        self._steps = [1,1,1]
        self._fadeAmt = 256 / self._tail

    def step(self, amt = 1):
        self._ledcolors = [(0,0,0) for i in range(self._size)]
        self._led.all_off()

        for i in range(0,3):
            self._currentpos[i] = self._start + self._steps[i]

            #average the colors together so they blend
            self._ledcolors[self._currentpos[i]] = map(lambda x,y: (x + y)/2, self._color[i], self._ledcolors[self._currentpos[i]])
            for j in range(1,self._tail):
                if self._currentpos[i] - j >= 0:
                    self._ledcolors[self._currentpos[i] - j] = map(lambda x,y: (x + y)/2, self._ledcolors[self._currentpos[i] - j], colors.color_scale(self._color[i], 255 - (self._fadeAmt * j)))
                if self._currentpos[i] + j < self._size:
                    self._ledcolors[self._currentpos[i] + j] = map(lambda x,y: (x + y)/2, self._ledcolors[self._currentpos[i] + j], colors.color_scale(self._color[i], 255 - (self._fadeAmt * j)))
            if self._start + self._steps[i] >= self._end:
                self._direction[i] = -1
            elif self._start + self._steps[i] <= 0:
                self._direction[i] = 1

            # advance each searchlight at a slightly different speed
            self._steps[i] += self._direction[i] * amt * int(random.random() > (i*0.05))

        for i,thiscolor in enumerate(self._ledcolors):
            self._led.set(i, thiscolor)


MANIFEST = [
    {
        "class": Searchlights,
        "controller": "strip",
        "desc": "Three search lights sweeping at different speeds",
        "display": "Searchlights",
        "id": "Searchlights",
        "params": [
            {
                "default": -1,
                "help": "Ending pixel (-1 for entire strip)",
                "id": "end",
                "label": "End",
                "type": "int"
            },
            {
                "default": 0,
                "help": "Starting pixel",
                "id": "start",
                "label": "Start",
                "type": "int"
            },
            {
                "default": 5,
                "help": "Length of the faded pixels at the start and end.",
                "id": "tail",
                "label": "Tail Length",
                "type": "int"
            },
            {
                "default": [colors.MediumSeaGreen,colors.MediumPurple,colors.MediumVioletRed],
                "help": "",
                "id": "colors",
                "label": "Colors",
                "type": "colors"
            }
        ],
        "type": "animation"
    }
]
