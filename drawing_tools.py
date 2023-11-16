from simple_polygon import generatePolygon
from triangulate_plane import triangulate_plane
from mw_triangulate_plane import MWT
from tkinter import *

YSIZE = 800
PSIZE = 2

def drawPoints(points):
    for p in points:
        p = (p[0], YSIZE - p[1])
        canvas.create_oval(p[0] - PSIZE, p[1] - PSIZE, p[0] + PSIZE, p[1] + PSIZE, w=2)

def drawLine(p1, p2, color):
    p1 = (p1[0], YSIZE - p1[1])
    p2 = (p2[0], YSIZE - p2[1])
    canvas.create_line(p1, p2, fill=color)

def drawPolygon(points, fill, outline):
    new_points = []
    for p in points:
        new_points.append((p[0], YSIZE - p[1]))
    canvas.create_polygon(new_points, fill=fill, outline=outline)

def DrawHull(event):
    global points
    print(points)
    drawPolygon(points, '', 'black')

def simple_triangulate(points):

    diags = triangulate_plane(points)

    i = 0
    while i < numVerts-1:
        drawLine(points[i], points[i+1], 'black')

        i += 1

    drawLine(points[i], points[0], 'black')

    for diag in diags:
        drawLine(diag[0], diag[1], 'red')

def mw_triangulate(points):

    diags = MWT(points)

    i = 0
    while i < numVerts-1:
        drawLine(points[i], points[i+1], 'black')

        i += 1

    drawLine(points[i], points[0], 'black')

    for diag in diags:
        drawLine(diag[0], diag[1], 'red')


# =========================================
root = Tk()
root.title("Points")
root.geometry(str(YSIZE)+'x'+str(YSIZE))

canvas = Canvas(root, width=2*YSIZE, height=YSIZE, bg='#FFF', highlightbackground="#999")
canvas.bind("<Button-1>", DrawHull)
canvas.grid(row=0, column=0)

# center coordinates for the polygon
ctrX = 400
ctrY = 400
aveRadius = 300
irregularity = 1
spikeyness = 0
numVerts = 10

print(YSIZE)

[points_1, points_2] = generatePolygon(ctrX, ctrY, aveRadius, irregularity, spikeyness, numVerts)

simple_triangulate(points_1)

mw_triangulate(points_2)

root.mainloop()