#!/usr/bin/python3

# Graphic Card Status and Switching automation script

import os
import sys
from time import sleep
import argparse

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

    def _switch_card(self):
        pass
    
    def turn_off_unused_card(self):
        with open(self.file_path,"w") as vga_file:
            vga_file.write("OFF")
    
    def turn_on_unused_card(self):
        with open(self.file_path,"w") as vga_file:
            vga_file.write("ON")

    def get_state(self):
        for graph_card in self.graphic_cards:
            print(graph_card)

def check_super_user():
    if not os.geteuid() == 0:
        sys.exit("This Script must be used by root.")



def setup_parser():
    parser = argparse.ArgumentParser(description="Tool to interact with dual graphic cards using vga_switcheroo on linux.")
    subparser = parser.add_subparsers(dest='command')
    subparser.add_parser('status', help='Will print Graphic cards state')
    switch_subparser = subparser.add_parser(
        'switch', help="Will help you turn one card ON or OFF")
    switch_subparser.add_argument('desired_state', choices=['on', 'off'])
    return parser.parse_args()


def main():
    check_super_user()
    tool = GraphicCardSwitchingTool(VGASWITCHEROO_FILEPATH)
    args = setup_parser()
    if args.command == 'status':
        tool.get_state()
    elif args.command == 'switch':
        if args.desired_state == 'off' :
            tool.turn_off_unused_card()
        elif args.desired_state == 'on' :
            tool.turn_on_unused_card()

if __name__ == "__main__":
    main()
