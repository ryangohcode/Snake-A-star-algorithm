import turtle
import time
import random 

wn = turtle.Screen()
wn.title("Snake")
wn.bgcolor("black")
wn.setup(width=800, height=600)
wn.tracer(0)
delay = 0

#border
bordertop = turtle.Turtle()
bordertop.speed(0)
bordertop.shape("square")
bordertop.color("white")
bordertop.shapesize(stretch_wid=0.1,stretch_len=41)
bordertop.penup()
bordertop.goto(0, 310)

borderbtm = turtle.Turtle()
borderbtm.speed(0)
borderbtm.shape("square")
borderbtm.color("white")
borderbtm.shapesize(stretch_wid=0.1,stretch_len=41)
borderbtm.penup()
borderbtm.goto(0, -310)

borderlft = turtle.Turtle()
borderlft.speed(0)
borderlft.shape("square")
borderlft.color("white")
borderlft.shapesize(stretch_wid=31,stretch_len=0.1)
borderlft.penup()
borderlft.goto(-410, 0)

borderrght = turtle.Turtle()
borderrght.speed(0)
borderrght.shape("square")
borderrght.color("white")
borderrght.shapesize(stretch_wid=31,stretch_len=0.1)
borderrght.penup()
borderrght.goto(410, 0)

#food
random.seed()
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("green")
food.shapesize(stretch_len= 1,stretch_wid=1)
food.penup()
xfood = random.randrange(-400, 400, 20)
yfood = random.randrange(-300, 300, 20)
food.goto(xfood,yfood)
eat_ammount = 0
segments = []
x1list = []
y1list = [1]

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 200)
pen.write("")
#legend
legend = turtle.Turtle()
legend.speed(0)
legend.shape("square")
legend.color("white")
legend.penup()
legend.hideturtle()
legend.goto(-500, 200)
legend.write("Legend:\nMovement=WASD\nA*Pathfinding=v")


#head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("red")
head.shapesize(stretch_wid=1,stretch_len=1)
head.penup()
head.goto(0, 0)
head.direction = "stop"

# Functions
def snake_head_up():
    if head.direction != "down":
        head.direction = "up"
    
def snake_head_down():
    if head.direction != "up":
        head.direction = "down"

def snake_head_right():
    if head.direction != "left":
        head.direction = "right"

def snake_head_left():
    if head.direction != "right":
        head.direction = "left"

new_segment = turtle.Turtle()
new_segment.speed(0)
new_segment.shape("square")
new_segment.color("white")
new_segment.penup()
segments.append(new_segment)
def auto():
    i = 0
    start = (head.xcor(),head.ycor())
    end = (xfood, yfood)
    path = astar(start, end)
    print(path)
    
    while i != len(path):
        wn.update()
        head.goto(path[i])
        i+=1
        time.sleep(0.1)

        for index in range(len(segments)-1, 0, -1):
           x1 = segments[index-1].xcor()
           y1 = segments[index-1].ycor()
           segments[index].goto(x1, y1)
           x1list.append(x1)
           y1list.append(y1)
           

     # Move segment 0 to where the head is
        if len(segments) > 0:
            segments[0].goto(path[i-2])

    if path[-1][0] > path[-2][0]:
        head.direction =='right'
        
    if path [-1][0] < path[-2][0]:
        head.direction =='left'
        
    if path [-1][1] < path[-2][1]:
        head.direction == 'down'
        
    if path [-1][1] > path[-2][1]:
        head.direction == 'up'
    
        
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y+20)
    if head.direction == "down":
        y = head.ycor()
        head.sety(y-20)
    if head.direction == "left":
        x = head.xcor()
        head.setx(x-20)
    if head.direction == "right":
        x = head.xcor()
        head.setx(x+20)


#keyboard binding
wn.listen()
wn.onkeypress(snake_head_up,"w")
wn.onkeypress(snake_head_down, "s")
wn.onkeypress(snake_head_left, "a")
wn.onkeypress(snake_head_right, "d")
wn.onkeypress(auto, "v")

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
      
        for new_position in [(0, -20), (0, 20), (-20, 0), (20, 0)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            print(node_position)
            # Make sure walkable terrain
            i = 0
            while i != len(x1list) :
                if node_position[0] == x1list[i] and node_position[1] == y1list[i]:
                    i += 1
                    continue  
                else:
                    i+=1
 
            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 20
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)

    

while True:
    wn.update()
    if head.ycor() > 310 or head.ycor() < -310 or head.xcor() > 410 or head.xcor() < -410:
        pen.clear()
        pen.write("GAME OVER!\nCrashed into wall",align="center", font=("Courier", 30, "normal"))
        head.goto (0,0)
        head.direction = "stop"
        eat_ammount=0
        for segment in segments:
            segment.goto(1000,1000)
        segments.clear()
        delay=0.1
        
 
    #food eat
    if (xfood-10)<=head.xcor()<=(xfood+10) and (yfood-10)<=head.ycor()<=(yfood+10):
        pen.clear()
        eat_ammount += 1
        pen.write("Ate: {}  ".format(eat_ammount), align="center", font=("Courier", 20, "normal"))
        xfood = random.randrange(-400, 400, 20)
        yfood = random.randrange(-300, 300, 20)
        food.goto(xfood,yfood)

     #segments
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("white")
        new_segment.penup()
        segments.append(new_segment)
        delay -= 0.001
    #Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x1 = segments[index-1].xcor()
        y1 = segments[index-1].ycor()
        segments[index].goto(x1, y1)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor() 
        y = head.ycor() 
        segments[0].goto(x,y)
    
    move()

    for segment in segments:
        if segment.distance(head) < 19:
            pen.clear()
            pen.write("GAME OVER!\nCrashed into body",align="center", font=("Courier", 30, "normal"))
            head.goto (0,0)
            head.direction = "stop"
            eat_ammount=0
            for segment in segments:
                segment.goto(1000,1000)
            segments.clear()
            delay=0.1

    time.sleep(delay)