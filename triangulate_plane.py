# The following algorithm triangulates x-monotone polygons
#   input P is expected to be the vertices of P in clockwise order,
#   starting with the minimum x-coordinate vertex; if two or such points
#   exist, the starting point is assumed to have the highest y-coordinate 
from math import inf


def triangulate_plane(P):
    
    [upper_hull, lower_hull] = generate_hulls(P)
    
    # a stack to handle points of the polygon's hull
    chain = list()
    # a set of the triangulated edges of the polygon
    triangulations = list()

    # start chain off with first two vertices
    i = 0
    while i < 2:
        p = max(upper_hull, lower_hull)
        chain.append(p)
        i += 1
    active_chain = p[1]

    # proceed through all the points sans the last
    n = len(P)
    while i < n:

        p = max(upper_hull, lower_hull)
        chain.append(p)

        # case 1: the point is not on the same chain as the active
        if i != n-1 and p[1] != active_chain:

            # triangulate the previous vertex; do not remove from stack
            # since it acts as the new invariant
            triangulations.append([p[0], chain[len(chain)-2][0]])

            # diagonalize all remaining vertices but the previous invariant; remove from chain
            while len(chain) > 3:
                triangulations.append([p[0], chain[len(chain)-3][0]])
                chain.pop(len(chain)-3)

            # remove previous invariant from chain
            chain.pop(0)

            # set active chain to that of point p
            active_chain = p[1]

        else:
            # case 2: point is on the same chain and is nonreflexive
            if is_nonreflexive([chain[len(chain)-3][0],chain[len(chain)-2][0]],chain[len(chain)-1][0], active_chain):
            
                # remove the neighboring non-reflexive vertex
                chain.pop(len(chain)-2)

                # go through the stack of vertices and continue diagonalizing until nonreflexivities are resolved
                while len(chain) > 2 and is_nonreflexive([chain[len(chain)-3][0],chain[len(chain)-2][0]],chain[len(chain)-1][0], active_chain):
                    triangulations.append([p[0], chain[len(chain)-2][0]])
                    chain.pop(len(chain)-2)
                
                # if the only remaining vertices are the invariant and the most recent
                # then diagonalize the two
                if i != n-1:
                    triangulations.append([p[0], chain[len(chain)-2][0]])
        
        i += 1
    
    return triangulations

def generate_hulls(P):

    upper_hull = list()
    lower_hull = list()

    max_i = get_max_index(P)
    n = len(P)
    i = 0
    while i < n:
        i1 = (max_i+i)%n
        i2 = (max_i+i+1)%n
        if P[i1][1] > P[i2][1]:
            lower_hull.append(P[i1])
        else:
            upper_hull.insert(0,P[i1])

        i += 1

    return [upper_hull, lower_hull]


    
def get_max_index(P):
    max_y = -inf
    
    i = 0
    n = len(P)
    while i < n:

        v = P[i]
        if v[1] > max_y:
            max_y = v[1]
            max_i = i
        i += 1

    return max_i

def max(upper_hull, lower_hull):

    if len(upper_hull) == 0:
        return [lower_hull.pop(0), 0]
    if len(lower_hull) == 0:
        return [upper_hull.pop(0), 1]

    max = [upper_hull[0], 1]
    if(lower_hull[0][1] > max[0][1]):
        max = [lower_hull[0], 0]
        lower_hull.pop(0)
    else:
        upper_hull.pop(0)
    return max

def is_nonreflexive(s, p, active_hull):
    # align segments along the origin
    s1 = (s[1][0]-s[0][0], s[1][1]-s[0][1])
    s2 = (p[0]-s[0][0], p[1]-s[0][1])

    # since the points are 2D, the cross product is quite trivial
    cross_prod = s1[0]*s2[1] - s2[0]*s1[1]

    # point is to the right and active hull is upper => nonreflexive
    if cross_prod < 0 and active_hull == 1:
        return True
    # point is to the left and active hull is lower => nonreflexive 
    if cross_prod > 0 and active_hull == 0:
        return True
    # point is to the left or inline => reflexive
    return False