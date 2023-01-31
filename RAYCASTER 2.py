#Raycaster v2

from random import randint
import tkinter
import time
import math

#classes
class Window():
    def __init__(self,x,y,scale,**kwargs):
        self.x = x
        self.y = y
        self.scale = scale
        self.bg = kwargs.get("colour","white")
        self.shape_list = []
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root,width=x*scale,height=y*scale,background=self.bg)
        self.canvas.pack()

    def update(self):
        self.root.update()

class Rectangle():
    def __init__(self,window,x,y,width,height,**kwargs):
        self.window = window
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colour = kwargs.get("colour","black")
        outline = kwargs.get("outline",True)
        if outline:
            self.shape = self.window.canvas.create_rectangle(x*self.window.scale,y*self.window.scale,(x+width)*self.window.scale,(y+height)*self.window.scale,fill=self.colour) 
        else:
            self.shape = self.window.canvas.create_rectangle(x*self.window.scale,y*self.window.scale,(x+width)*self.window.scale,(y+height)*self.window.scale,fill=self.colour,outline="") 
        self.window.shape_list.append(self)
        
    def move(self,i,j):
        self.x += i
        self.y += j
        self.window.canvas.move(self.shape,i*self.window.scale,j*self.window.scale)  

    def change_colour(self,new_colour):
        self.colour = new_colour
        self.window.canvas.itemconfigure(self.shape,fill=new_colour)

#tkinter binds
def move_left(event):
    global p_vector
    p_vector[0] = 1

def move_right(event):
    global p_vector
    p_vector[0] = -1

def move_forward(event):
    global p_vector
    p_vector[1] = 1
    
def move_backward(event):
    global p_vector
    p_vector[1] = -1

def look_left(event):
    global p_vector
    p_vector[2] = 1

def look_right(event):
    global p_vector
    p_vector[2] = -1

def reset_movement(event):
    global p_vector
    if event.char == "a" and p_vector[0] != -1:
        p_vector[0] = 0
    elif event.char == "d" and p_vector[0] != 1:
        p_vector[0] = 0
    elif event.char == "w" and p_vector[1] != -1:
        p_vector[1] = 0
    elif event.char == "s" and p_vector[1] != 1:
        p_vector[1] = 0
    elif event.char == "o" and p_vector[2] != -1:
        p_vector[2] = 0
    elif event.char == "p" and p_vector[2] != 1:
        p_vector[2] = 0

def button_colour_flip(event):
    global grid
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if button_grid[y][x] == event.widget:
                pos = (x, y)
                break
    if event.widget["bg"] == "black":
        grid[pos[1]][pos[0]] = 0
        event.widget["bg"] = "white"
    else:
        grid[pos[1]][pos[0]] = 1
        event.widget["bg"] = "black"

def size_change(*args):
    global grid, button_grid
    xDIM = int(x_size.get())
    yDIM = int(y_size.get())
    grid = make_grid(xDIM,yDIM)
    for y in range(len(button_grid)):
        for x in range(len(button_grid[0])):
            button_grid[y][x].destroy()
    button_grid = []
    for y in range(len(grid)):
        button_grid.append([])
        for x in range(len(grid[0])):
            if grid[y][x] == 1:
                b = tkinter.Button(button_frame,bg="black",width=2)
            else:
                b = tkinter.Button(button_frame,bg="white",width=2)
            b.bind("<Button-1>",button_colour_flip)
            b.grid(column=x,row=y)
            button_grid[y].append(b)

#functions
def hex_colour(r,g,b,distance):
    r,g,b = round(r),round(g),round(b)
    if r < 0:
        r = 0
    if g < 0:
        g = 0
    if b < 0:
        b = 0
    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255
    r = hex(r)[2:]
    if len(r) == 1:
        r = "0"+r
    g = hex(g)[2:]
    if len(g) == 1:
        g = "0"+g
    b = hex(b)[2:]
    if len(b) == 1:
        b = "0"+b
    num = "#"+r+g+b
    return num

def make_colour(colour,distance):
    if distance == 0:
        x = 255
    else:
        x = 255*(1-(distance/len(grid)))
        r = colour[0]*(x/255)
        g = colour[1]*(x/255)
        b = colour[2]*(x/255)
    return hex_colour(r,g,b,x)

def calculate_distance(c1,c2):
    return abs(math.sqrt((c2[0]-c1[0])**2+(c2[1]-c1[1])**2))

def get_grid_pos(pos):
    return [math.floor(pos[0]),math.floor(pos[1])]

def deg_to_rad(angle):
    return (angle/360)*2*pi

def limit_rad(rad):
    if rad < 0:
        rad += ((math.floor(abs(rad)/(2*pi)))+1)*2*pi
    elif rad > (2*pi):
        rad -= (math.floor(rad/(2*pi)))*2*pi
    return rad

def get_angle_list(facing,FOV,ray_count):
    rad = deg_to_rad(FOV)
    ray_count -= 1
    step = rad/ray_count
    array = []
    angle = facing - (rad/2)
    array.append(limit_rad(angle))
    for i in range(ray_count):
        angle += step
        array.append(limit_rad(angle))
    array.reverse()
    return array

def cast_ray(source,angle,grid):
    h_distance,v_distance = 1000000000,1000000000
    pos = list(source)
    #horizontal collisions
    if angle>pi/2 and angle<3*pi/2:
        dy = pos[1]-get_grid_pos(pos)[1]
        pos[1] = round(pos[1]-dy,1)
        pos[0] -= dy * math.tan(angle)
    else:   
        dy = math.ceil(pos[1])-pos[1]
        pos[1] = round(pos[1]+dy,1)
        pos[0] += dy * math.tan(angle)
    while pos[0]>=0 and pos[1]>=0 and pos[0]<len(grid[0]) and pos[1]<len(grid):
        grid_pos = get_grid_pos(pos)
        if grid[grid_pos[1]][grid_pos[0]] != 0 or grid[grid_pos[1]-1][grid_pos[0]] != 0:
            h_hit = list(pos)  
            h_distance = calculate_distance(source,pos)
            break
        else:
            if enable_bird:
                r = Rectangle(bird_window,pos[0],pos[1],0.1,0.1,colour="red")  
            if angle>pi/2 and angle<3*pi/2:
                pos[0] -= math.tan(angle)
                pos[1] -= 1
            else:
                pos[0] += math.tan(angle)
                pos[1] += 1
    pos = list(source)
    #vertical collisions
    if angle==0 or angle==2*pi:
        return h_distance
    if angle>pi and angle<2*pi:
        dx = pos[0]-get_grid_pos(pos)[0]
        pos[0] = round(pos[0]-dx,1)
        pos[1] -= dx / math.tan(angle)
    else:
        dx = math.ceil(pos[0])-pos[0]
        pos[0] = round(pos[0]+dx,1)
        pos[1] += dx / math.tan(angle)
    while pos[0]>=0 and pos[1]>=0 and pos[0]<len(grid[0]) and pos[1]<len(grid):
        grid_pos = get_grid_pos(pos)
        if grid[grid_pos[1]][grid_pos[0]] != 0 or grid[grid_pos[1]][grid_pos[0]-1] != 0:
            v_hit = list(pos)  
            v_distance = calculate_distance(source,pos)
            break
        else:
            if enable_bird:
                r = Rectangle(bird_window,pos[0],pos[1],0.1,0.1,colour="blue")  
            if angle>pi and angle<2*pi:
                pos[0] -= 1
                pos[1] -= 1/math.tan(angle)
            else:
                pos[0] += 1
                pos[1] += 1/math.tan(angle)
    if h_distance < v_distance:
        if enable_bird:
            r = Rectangle(bird_window,h_hit[0],h_hit[1],0.1,0.1,colour="pink")
        return h_distance
    else:
        if enable_bird:
            r = Rectangle(bird_window,v_hit[0],v_hit[1],0.1,0.1,colour="pink")
        return v_distance  

def set_binds(window):
    window.root.bind("<w>",move_forward)
    window.root.bind("<a>",move_left)
    window.root.bind("<s>",move_backward)
    window.root.bind("<d>",move_right)
    window.root.bind("<o>",look_left)
    window.root.bind("<p>",look_right)
    window.root.bind("<KeyRelease>",reset_movement)
    
def update_display():
    if enable_bird:
        if enable_editor:
            bird_window.canvas["width"] = int(x_size.get())*bird_window.scale
            bird_window.canvas["height"] = int(y_size.get())*bird_window.scale
        bird_window.canvas.delete("all")
        draw_grid(bird_window,grid)
        r = Rectangle(bird_window,p_pos[0],p_pos[1],0.1,0.1,colour="lime")
    angles = get_angle_list(p_facing,FOV,ray_count)
    distances = []
    for a in angles:
        d = cast_ray(p_pos,a,grid)
        distances.append(d)
    w.canvas.delete("all")
    ceiling = Rectangle(w,0,0,window_width,window_height/2,colour="grey40",outline=False)
    floor = Rectangle(w,0,window_height/2,window_width,window_height/2,colour="grey90",outline=False)
    line_width = window_width/ray_count
    for i in range(ray_count):
        line_height = (1/distances[i]) * window_height
        r = Rectangle(w,i*line_width,(window_height/2)-(line_height/2),line_width,line_height,colour=make_colour(wall_colour,distances[i]),outline=False)

def draw_grid(window,grid):
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            if grid[y][x] == 1:
                r = Rectangle(window,x,y,1,1,colour="gray60")
            else:
                r = Rectangle(window,x,y,1,1,colour="grey90")

def make_grid(xDIM,yDIM):
    grid = []
    for y in range(yDIM):
        grid.append([])
        for x in range(xDIM):
            if y == 0 or y == yDIM-1 or x == 0 or x == xDIM-1:
                grid[y].append(1)
            else:
                grid[y].append(0)
    return grid

#game loop
def game_step():
    global p_pos, p_facing
    p_pos[0] += move_speed*math.cos(p_facing) * p_vector[0]
    p_pos[1] -= move_speed*math.sin(p_facing) * p_vector[0]
    p_pos[0] += move_speed*math.sin(p_facing) * p_vector[1]
    p_pos[1] += move_speed*math.cos(p_facing) * p_vector[1]
    p_facing += look_speed * p_vector[2]
    p_facing = limit_rad(p_facing)
    
def game_loop():
    game_state = True
    while game_state == True:
        try:
            update_display()
            w.update()
            if enable_bird:
                bird_window.update()
            game_step()
            time.sleep(1/FPS)
        except tkinter.TclError:
            print("Window Closed.")
            game_state = False

#grid
global grid
grid = [
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,1],
    [1,1,0,0,0,1,1,0,0,0,1],
    [1,0,0,0,0,1,1,0,0,0,1],
    [1,1,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,1,0,1],
    [1,1,0,0,0,0,0,1,1,0,1],
    [1,0,0,0,1,1,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1]
    ]

#constants

FPS = 60
FOV = 75 #in degrees
ray_count = 120
pi = 3.14159
window_height = 90
window_width = 160
window_scale = 6

size_options = {"6","8","10","12","15"}

#optional windows

enable_bird = True
enable_editor = True

#starting values

global p_pos, p_facing, p_vector
p_pos = [3.6,4.6]
p_facing = 5
p_vector = [0,0,0]
move_speed = 0.08
look_speed = 0.1
wall_colour = (randint(155,255),randint(155,255),randint(155,255))
wall_colour = (200,200,200)

#run code

if enable_editor:
    editor_window = tkinter.Tk()
    editor_window.title("Level Editor")
    options_frame = tkinter.Frame(editor_window)
    options_frame.pack(side=tkinter.TOP)

    x_size = tkinter.StringVar(editor_window)
    x_size.set("10")
    x_menu = tkinter.OptionMenu(options_frame,x_size,*size_options)
    x_menu.pack(side=tkinter.LEFT)
    x_size.trace("w",size_change)

    y_size = tkinter.StringVar(editor_window)
    y_size.set("10")
    y_menu = tkinter.OptionMenu(options_frame,y_size,*size_options)
    y_menu.pack(side=tkinter.LEFT)
    y_size.trace("w",size_change)

    grid = make_grid(int(x_size.get()),int(y_size.get()))
    
    button_frame = tkinter.Frame(editor_window)
    button_frame.pack(side=tkinter.BOTTOM)
    global button_grid
    button_grid = []
    for y in range(len(grid)):
        button_grid.append([])
        for x in range(len(grid[0])):
            if grid[y][x] == 1:
                b = tkinter.Button(button_frame,bg="black",width=2)
            else:
                b = tkinter.Button(button_frame,bg="white",width=2)
            b.bind("<Button-1>",button_colour_flip)
            b.grid(column=x,row=y)
            button_grid[y].append(b)

w = Window(window_width,window_height,window_scale)
w.root.title("Raycaster")
set_binds(w)

if enable_bird:
    bird_window = Window(len(grid[0]),len(grid),60)
    bird_window.root.title("Bird View")
    draw_grid(bird_window,grid)

game_loop()

