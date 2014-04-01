def distance_limiter(min_gravitation_distance, max_repulsion_distance):
    def deco(f):
        def wrapper(space, node_l, node_r):
            r = f(space, node_l, node_r)

            distance = node_l.pos.distance_to(node_r.pos)
            if r > 0 and distance < min_gravitation_distance:
                return -r
            if r < 0 and distance > max_repulsion_distance:
                return 0
            return r

        return wrapper

    return deco


def reverse_strength(f):
    def wrapper(space, node_l, node_r):
        r = f(space, node_l, node_r)
        return space.max_relevance - r

    return wrapper


@distance_limiter(min_gravitation_distance=20, max_repulsion_distance=50)
def const_gravitation(space, node_l, node_r):
    return space.connections.get((node_l, node_r), 0)


@distance_limiter(min_gravitation_distance=20, max_repulsion_distance=100)
def linear_gravitation(space, node_l, node_r):
    'The further, the stronger.'

    fact = node_l.pos.distance_to(node_r.pos)
    return space.connections.get((node_l, node_r), 0) * fact


def natural_gravitation(space, node_l, node_r):
    'Newtonian attraction.'

    fact = (node_l.pos - node_r.pos).length_squared ** -1
    return space.connections.get((node_l, node_r), 0) * fact
