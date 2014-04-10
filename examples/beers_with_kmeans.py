import os
import sys
import pylab as pl
import math
from numpy import array
from sklearn.cluster import KMeans


sys.path.append(os.path.abspath('.'))

from models.space import Space, Node, Vector2D
from models.utils import StopWatch


def pos_in_circle(center, r, split_count, index):
    radian = 2 * math.pi / split_count * index
    x = r * math.cos(radian)
    y = r * math.sin(radian)

    return center + Vector2D(x, y)


def normalize(value):
    value = value.strip()
    return float(value) if value else 0


center = Vector2D(300, 300)
nodes = {i: Node(i, pos_in_circle(center, 200, 50, i)) for i in range(1, 51)}


def load_space():
    space = Space(size=(600, 600), max_step_length=10)

    with open('examples/fixtures/beers.tsv', 'r') as f:
        f.readline()
        row_index = 1
        for l in f:
            row = l.split('\t')
            node1 = nodes[row_index]

            for i, value in enumerate(row[1:]):
                value = normalize(value)
                if value == 0:
                    continue

                node2 = nodes[i + 1]
                space.connect(node1, node2, value)

            row_index += 1

    return space


def cluster_by_k_means(space, center_count=3):
    node_pos_matrix = array([[n.pos.x, n.pos.y] for n in space.nodes])

    k_means = KMeans(init='k-means++', n_clusters=center_count, n_init=10)
    k_means.fit(node_pos_matrix)
    labels = k_means.labels_
    cluster_centers = k_means.cluster_centers_
    return node_pos_matrix, labels, cluster_centers


def log(*msg):
    print(*msg)


if __name__ == '__main__':

    space = load_space()

    log('Simulating...')
    with StopWatch(log):
        for i in range(500):
            space.step_forward()

    log('Clustering by K means...')
    center_count = 3
    with StopWatch(log):
        nodes_matrix, labels, centers = cluster_by_k_means(space, center_count)

    log(labels, centers)

    log('Preparing plot...')
    colors = ['#4EACC5', '#FF9C34', '#4E9A06']

    fig = pl.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1)

    for i in range(center_count):
        is_member_matrix = labels == i
        ax.plot(nodes_matrix[is_member_matrix, 0],
                nodes_matrix[is_member_matrix, 1], 'o',
                markerfacecolor=colors[i], markersize=6)

    pl.show()
