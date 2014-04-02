import math
from ui.dashboard import DashBoard
from models.space import Space, Node, Vector2D


def pos_in_circle(center, r, split_count, index):
    radian = 2 * math.pi / split_count * index
    print radian
    x = r * math.cos(radian)
    y = r * math.sin(radian)

    print x, y
    return center + Vector2D(x, y)


def normalize(value):
    value = value.strip()
    return float(value) if value else 0


center = Vector2D(300, 300)
nodes = {i: Node(i, pos_in_circle(center, 200, 50, i)) for i in xrange(1, 51)}


if __name__ == '__main__':
    space = Space(size=(600, 600), step_factor=0.00001)

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

    DashBoard(space).run()
