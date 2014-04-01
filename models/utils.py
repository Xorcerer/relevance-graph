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
