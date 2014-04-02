# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.clock import Clock
from kivy.graphics import Ellipse, Color, Line
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout

WHITE = Color(1., 1., 1.)


class NodeWidget(Widget):
    def __init__(self, **kwargs):
        node = kwargs.pop('node')
        self.node = node

        super(self.__class__, self).__init__(**kwargs)

        self.size = (10, 10)
        color = Color(*node.color) if node.color else WHITE
        self.circle = Ellipse(pos=self.pos, size=self.size)

        self.canvas.add(color)
        self.canvas.add(self.circle)

    def on_pos(self, obj, new_pos):
        r = 5
        self.circle.pos = new_pos[0] - r, new_pos[1] - r

    def update(self):
        self.pos = self.node.pos.to_tuple()


class BoardWidget(FloatLayout):
    def __init__(self, size, space):
        super(self.__class__, self).__init__(size=size)

        print self.canvas
        self.space = space

        self.widgets = []
        self.lines = []
        for n in space:
            node_widget = NodeWidget(node=n)
            node_widget.pos = n.pos.to_tuple()
            self.widgets.append(node_widget)
            self.add_widget(node_widget)

            for other in space:
                relevance = self.space.connections.get((n, other), 0)
                if other.id >= n.id or relevance == 0:
                    continue

                print relevance
                l = Line(points=[n.pos.x, n.pos.y, other.pos.x, other.pos.y],
                         width=1.0)
                self.canvas.add(Color(relevance, relevance, relevance))
                self.lines.append((n, other, l))
                self.canvas.add(l)

    def update_lines(self):
        for n, other, l in self.lines:
            l.points = [n.pos.x, n.pos.y, other.pos.x, other.pos.y]

    def update(self):
        self.update_lines()
        for w in self.widgets:
            w.update()


class DashBoard(App):
    def __init__(self, space):
        super(self.__class__, self).__init__()

        self.space = space

    def update(self, _):
        self.space.step_forward()
        self.board.update()

    def build(self):

        self.board_size = self.space.size
        Clock.schedule_interval(self.update, .1)
        print 'map size: %s' % (self.board_size,)
        self.board = BoardWidget(self.board_size, self.space)

        return self.board
