# The following algorithm triangulates convex polygons using
#   minimum weight polygon triangulation. input P is expected to be in
#   either ccw or cw order 
from math import inf
from math import sqrt

# function to calculate the weight of optimal triangulation of a convex polygon
# represented by a given set of vertices
def MWT(P):
 
    # get the number of vertices in the polygon
    n = len(P)
 
    # create a table for storing the solutions to subproblems
    # `T[i][j]` stores the weight of the minimum-weight triangulation
    # of the polygon below edge `ij`
    T = [[0] * n for _ in range(n)]

    # fill the table diagonally using the recurrence relation
    for diagonal in range(n):
        i = 0
        for j in range(diagonal, n):
            # if the polygon has less than 3 vertices, triangulation is not possible
            if j >= i + 2:
                T[i][j] = inf
                # consider all possible triangles `ikj` within the polygon
                for k in range(i + 1, j):
                    # The weight of triangulation is the length of its perimeter
                    weight = dist(P[i], P[j]) +  dist(P[j], P[k]) +  dist(P[k], P[i])
                    # choose vertex `k` that leads to the minimum total weight
                    if (weight + T[i][k] + T[k][j]) < T[i][j]:
                        T[i][j] = weight + T[i][k] + T[k][j]
                        T[j][i] = k

            i += 1
 
    diags = list()
    get_triangulation(P, T, 0, n-1, diags)
    
    return diags
    
# recursively select the resulting diagonals
def get_triangulation(P, T, i, j, diags):

    k = T[j][i]
    # k == j-1 => k and j are neighboring vertices and thus
    # there is no resulting diagonal and no reason to recurse further
    # into their subregion
    if not k == j-1:
        diags.append([P[k], P[j]])
        get_triangulation(P, T, k, j, diags)
    # k == i + 1 => i and k are neighboring vertices and thus
    # there is no resulting diagonal and no reason to recurse further
    if not k == i+1:
        diags.append([P[i], P[k]])
        get_triangulation(P, T, i, k, diags)

# utility function to return the distance between two vertices in a 2–dimensional plane
def dist(x, y):
 
    # The distance between vertices `(x1, y1)` and `(x2, y2)` is
    # `√((x2 − x1) ^ 2 + (y2 − y1) ^ 2)`
    return sqrt((x[0] - y[0]) * (x[0] - y[0]) + (x[1] - y[1]) * (x[1] - y[1]))