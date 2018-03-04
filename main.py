from simulator import Simulator
import sys

USAGE_MESSAGE = "Use by executing this file with the .html of your chat log as the argument:\n\tpython main.py FILENAME"

def main():
    if (len(sys.argv) != 2):
        print(USAGE_MESSAGE)
        return

    sim = Simulator(sys.argv[1])
    sim.simulateAll()

if __name__ == "__main__":
    main()
