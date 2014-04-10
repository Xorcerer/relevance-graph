from ui.dashboard import DashBoard
from models.space import Space, Node, Vector2D


if __name__ == '__main__':
    space = Space(size=(600, 600), no_relevance_distance=100,
                  step_factor=0.0003)

    center = Node(0, Vector2D(100, 300), color=(1.0, 1.0, 0.5))
    a = Node(1, Vector2D(100, 110))
    b = Node(2, Vector2D(200, 220))
    c = Node(3, Vector2D(300, 400))
    d = Node(4, Vector2D(400, 333))
    e = Node(5, Vector2D(500, 550))

    value = 1.0
    space.connect(center, a, value)
    space.connect(center, b, value)
    space.connect(center, c, value)
    space.connect(center, d, value)
    space.connect(center, e, value)

    DashBoard(space).run()
