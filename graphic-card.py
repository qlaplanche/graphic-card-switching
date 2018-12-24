#!/usr/bin/python3

# Graphic Card Status and Switching automation script

import os
import sys

PWR_INDICATOR = "Pwr"
SPLITTING_CHAR = ":"
VGASWITCHEROO_FILEPATH = "/sys/kernel/debug/vgaswitcheroo/switch"


class GraphicCardState():
    ON = "Pwr"
    OFF = "OFF"
    DYN_OFF = "DYN_OFF"
    UNKNOWN = "UNKNOWN"


class GraphicCard():
    def __init__(self, name):
        self.name = name
        self.state = GraphicCardState.UNKNOWN
        self.in_use = False

    def __str__(self):
        partial_state = "{0} card is {1} ".format(self.name, self.state)
        return partial_state + "and in use." if self.in_use else partial_state + "and not in use."


class GraphicCardSwitchingTool():
    def __init__(self, file_status_path):
        self.graphic_cards = []
        self.file_path = file_status_path
        self.load_status()

    def load_status(self):
        with open(self.file_path) as file:
            for line in file.readlines():
                data = line.split(SPLITTING_CHAR)
                tmp_graphcard = GraphicCard(data[1])
                tmp_graphcard.state = GraphicCardState.ON if data[
                    3] == PWR_INDICATOR else GraphicCardState.OFF

                tmp_graphcard.in_use = True if data[2] == "+" else False

                self.graphic_cards.append(tmp_graphcard)

    def get_state(self):
        for graph_card in self.graphic_cards:
            print(graph_card)

def check_super_user():
    if not os.geteuid() == 0:
        sys.exit("This Script must be used by root.")


def main():
    check_super_user()
    tool = GraphicCardSwitchingTool(VGASWITCHEROO_FILEPATH)
    tool.get_state()

if __name__ == "__main__":
    main()
