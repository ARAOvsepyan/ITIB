from math import sqrt, inf
from colorsys import rgb_to_hsv, hsv_to_rgb

from tkinter import *
from tkinter import Text


# Distances
def Euklidean(p, c):
    return sqrt((p[0]-c[0])*(p[0]-c[0]) + (p[1]-c[1])*(p[1]-c[1]))

def Manhattan(p, c):
    return abs(p[0]-c[0]) + abs(p[1]-c[1])

def Chebyshev(p, c):
    return max(abs(p[0]-c[0]), abs(p[1]-c[1]))

def setDistance(dist):
    global distance
    distance = dist


# Logging clusters info into file
file = open('output.txt', 'w')
def log():
    global k
    file.write(f'K: {k}\n')
    for c in range(len(clusters)):
        file.write(f'  C{c}: ({clusters[c][0]};{clusters[c][1]}) with {len(clusters[c][3])} points\n')


def getHexColorFromArray(array, koeff=1):
    colors = [hex(int(el*koeff))[2:] for el in array]
    res = '#'
    for c in colors:
        c = '0'*(2-len(c)) + c
        res += c
    return res

def setClustersColor():
    N = len(clusters)
    step = 360/N
    HSVs = [[step*i/360, 1, 1] for i in range(N)]
    for c in range(len(clusters)):
        hsv = HSVs[c]
        rgb = hsv_to_rgb(hsv[0], hsv[1], hsv[2])
        rgb = [255*c for c in rgb]
        clusters[c][2] = rgb
    # show new given colors
    redraw()


# Give each point correct cluster
def distributePoints():
    for c in clusters:
        c[3] = []

    for p in points:
        minDistance = inf
        clusterIndex = 0
        for c in range(len(clusters)):
            global distance
            dist = distance(p, clusters[c])

            if minDistance > dist:
                minDistance = dist
                clusterIndex = c

        p[2] = clusters[clusterIndex][2]
        clusters[clusterIndex][3].append(p)
    redraw()

# Calculate new clusters positions
def recenter(c):
    X = [c[3][i][0] for i in range(len(c[3]))]
    Y = [c[3][i][1] for i in range(len(c[3]))]

    if len(c[3]):
        c[0] = sum(X)/len(X)
        c[1] = sum(Y)/len(Y)

    redraw()


# Start method
def start():
    if not len(clusters):
        return

    # give each cluster a color
    setClustersColor()

    global k 
    k = 0
    while True:
        log()
        k += 1

        distributePoints()

        prev = clusters.copy()
        for c in clusters:
            recenter(c)
        ret = True
        for c in range(len(clusters)):
            if prev[c] != clusters[c]:
                ret = False
        if ret:
            break
        

# Draw frame
def redraw(_clear=True, _points=True, _clusters=True):
    if _clear:
        canvas.delete('all')

    if _points:
        for p in points:
            x, y, color = p[0], p[1], p[2]
            colorHex = getHexColorFromArray(color)
            canvas.create_oval(x-5, y-5, x+5, y+5, fill=colorHex, outline='black', width=1)

    if _clusters:
        for c in clusters:
            x, y, color = c[0], c[1], c[2]
            colorHex = getHexColorFromArray(color)
            canvas.create_rectangle(x-6, y-6, x+6, y+6, fill=colorHex, outline='black', width=1)

#  Clear canvas, remove points, clusters
def reset():
    canvas.delete('all')
    global points
    global clusters
    points = []
    clusters = []


# place point/cluster on mouseClick
def placePoint(event):
    x, y = event.x, event.y
    canvas.create_oval(x-5, y-5, x+5, y+5, fill='white', outline='black', width=1)
    points.append([x, y, [255, 255, 255]])

def placeCluster(event):
    x, y = event.x, event.y
    canvas.create_rectangle(x-6, y-6, x+6, y+6, fill='white', outline='black', width=1)
    clusters.append([x, y, [255, 255, 255], []])


root = Tk(className='Ovsepyan IC8-63')
root.geometry('700x710')
root.configure(background='#afbfbf')

global distance
global k
distance = Euklidean
k = 0

points = []
clusters = []

canvas = Canvas(root, width=600, height=600, bg='white')
canvas.bind('<Button-1>', placePoint)
canvas.bind('<Button-3>', placeCluster)
canvas.place(x=50,y=25)

start_btn = Button(text='step', font=("Courier", 9), height=4, width=10, command=start).place(x=55,y=635)
reset_btn = Button(text='reset', font=("Courier", 9), height=4, width=10, command=reset).place(x=155,y=635)

eukl_btn = Button(text='euklidean', font=("Courier", 9), height=4, width=10, command=lambda *args: setDistance(Euklidean)).place(x=255,y=635)
manh_btn = Button(text='manhattgan', font=("Courier", 9), height=4, width=10, command=lambda *args: setDistance(Manhattan)).place(x=355,y=635)
cheb_btn = Button(text='chebyshev', font=("Courier", 9), height=4, width=10, command=lambda *args: setDistance(Chebyshev)).place(x=455, y=635)

text = 'Left click:\nplace point\nRight click:\nplace cluster'
textLabel = Label(root, text=text, font=("Courier", 9), height=4, width=13, justify=LEFT).place(x=555,y=636)

root.mainloop()