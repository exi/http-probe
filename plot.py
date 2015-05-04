import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime

MEASURE_FILE = 'measures.txt'
OUTPUT_FILE = 'plot.svg'


def plot():
    with open(MEASURE_FILE, 'r') as f:
        values = [x.split(';') for x in f.readlines()]
    values = [(int(t), int(bps)) for t, bps in values]
    x = [datetime.fromtimestamp(t) for t, bps in values]
    y = [bps for t, bps in values]

    # plot
    plt.plot(x, y)
    # beautify the x-labels
    plt.gcf().autofmt_xdate()

    plt.savefig(OUTPUT_FILE)


if __name__ == '__main__':
    plot()