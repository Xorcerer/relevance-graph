# src_node: the source of gravity;
# dest_node: the target of gravity,
# which should be pulled to src, if gravity is positive.


def distance_limiter(min_gravitation_distance, max_repulsion_distance):
    def deco(f):
        def wrapper(space, dest_node, src_node):
            r = f(space, dest_node, src_node)

            distance = dest_node.pos.distance_to(src_node.pos)
            if r > 0 and distance < min_gravitation_distance:
                return 0
            if r < 0 and distance > max_repulsion_distance:
                return 0
            return r

        return wrapper

    return deco


def directional(f):
    'Make the scalar force into vector form.'

    def wrapper(space, dest_node, src_node):
        r = f(space, dest_node, src_node)

        # Gravitation push dest_node to src_node.
        # (src_node.pos - dest_node.pos) => a vector from dest to src.
        return (src_node.pos - dest_node.pos).normalized * r

    return wrapper


def combine_funcs(*funcs):
    def wrapper(*args, **kwargs):
        if not funcs:
            return None

        r = funcs[0](*args, **kwargs)
        for f in funcs[1:]:
            r += f(*args, **kwargs)
        return r

    return wrapper


def log_invoking(f):
    def wrapper(*args, **kwargs):
        print ('%s(*s, *s)' % (f.__name__, args, kwargs))
        return f(*args, **kwargs)

    return wrapper


@directional
def hook_force(space, dest_node, src_node):
    'F = k * r. r stands for distance of nodes.'

    if space.diff_from_best_distance(src_node, dest_node) < 0:
        return 0
    k = space.connections.get((src_node, dest_node), 0)
    return k * dest_node.pos.distance_to(src_node.pos)


@directional
def coulomb_force(space, dest_node, src_node):
    '''Theoretically: F = k / r ^ 2.
       The implementation is a bit DIFFERENT from thoerem.
    '''

    diff = space.diff_from_best_distance(src_node, dest_node)
    if diff >= 0:
        return 0
    k = -.5
    return k * (diff ** 2)


default_force_func = combine_funcs(hook_force, coulomb_force)
