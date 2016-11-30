import numpy as np
import matplotlib.pyplot as plt

def draw_scatter_plot():
    links = None
    with open('info.txt', 'r') as f:
        links = f.read()
    links = eval(links)
    internal = [x[1] for x in links]
    external = [x[0] for x in links]
    N = len(internal)
    colors = np.random.rand(N)
    plt.scatter(internal, external, s=15, c=colors, alpha=1)
    plt.xlabel('External Links')
    plt.ylabel('Internal Links')
    plt.show()

def main():
    draw_scatter_plot()

if __name__ == "__main__":
    main()
