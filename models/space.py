from models.vector import Vector2D


def fixed_distance_gravitation(space, node_l, node_r):
    relevance = space.connections.get((node_l, node_r), 0)
    diff = space.diff_from_best_distance(node_l, node_r)
    if diff > 0:
        return relevance
    return -1  # return a consistant strong repulsion if too closed.


class Space(object):
    def __init__(self, gravitation_func, size, no_relevance_distance=100,
                 min_relevance=0.0, max_relevance=1.0):
        self.gravitation_func = gravitation_func

        self.size = size
        self.nodes = set()
        self.connections = {}  # (node1, node2): weight

        self.no_relevance_distance = no_relevance_distance
        self.min_relevance = min_relevance
        self.max_relevance = max_relevance

    def add(self, node):
        self.nodes.add(node)

    def add_range(self, nodes):
        for n in nodes:
            self.add(n)

    def best_distance(self, node_l, node_r):
        relevance = self.connections.get((node_l, node_r), 0)
        if not relevance:
            return self.no_relevance_distance

        return (self.no_relevance_distance * (relevance - self.min_relevance) /
                (self.max_relevance - self.min_relevance))

    def diff_from_best_distance(self, node_l, node_r):
        return node_l.pos.distance_to(node_r.pos) - \
            self.best_distance(node_l, node_r)

    def gravitation_between(self, node_l, node_r):
        return self.gravitation_func(self, node_l, node_r)

    def connect(self, node_l, node_r, relevance):
        self.add_range((node_l, node_r))

        # Undirected.
        self.connections[(node_l, node_r)] = relevance
        self.connections[(node_r, node_l)] = relevance

    def __iter__(self):
        for n in self.nodes:
            yield n

    def step_forward(self, step_length=0.1):
        steps = {}  # node: vector

        for n in self.nodes:
            sub_steps = []
            # FIXME: Speed up by enumerate over actually connected nodes only.
            for another in self.nodes:
                if n == another:
                    continue

                grav = self.gravitation_between(n, another)
                direction = (another.pos - n.pos).normalized
                sub_step = direction * grav * step_length
                sub_steps.append(sub_step)

            step = sum(sub_steps, Vector2D(0, 0))
            steps[n] = step

        for n, step in steps.items():
            n.move(step)


class Node(object):
    def __init__(self, id, pos):
        self.id = id
        self.pos = pos

    def __str__(self):
        return 'Node %s(%s, %s)' % (self.id, self.pos.x, self.pos.y)

    def move(self, offset):
        self.pos = self.pos + offset


def test():
    a = Node(1, Vector2D(0, 0))
    b = Node(2, Vector2D(0, 30))
    c = Node(3, Vector2D(0, 60))

    space = Space(gravitation_func=fixed_distance_gravitation, size=(600, 600),
                  no_relevance_distance=20)

    g = 1
    space.connect(a, b, g)
    space.connect(a, c, g)
    space.connect(b, c, g)

    assert space.gravitation_between(a, b) == g

    space.step_forward()
    space.step_forward()

    assert a.pos.y > 0
    assert b.pos.y == 30  # Unmoved.
    assert a.pos.y < 60


if __name__ == '__main__':
    test()
