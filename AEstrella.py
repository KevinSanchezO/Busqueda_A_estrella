from pyamaze import maze,agent

x = 0
y = 0
obstacles = False

def configurationSize():
    global x, y 
    print("\n[ Defina el tamaño del laberinto ]\n")
    val_x = input("Tamaño en X: ")
    val_y = input("Tamaño en Y: ")

    if (checkSizes(val_x, val_y)):
        x = int(val_x)
        y = int(val_y)
        addObstacles()
    else:
        print("\nTamaños no validos")
        configurationSize()

def addObstacles():
    global obstacles
    val = input("\nDesea agregar obstaculos? [Y/N]: ")
    if val == "Y" or val == "y":
        obstacles = True
    elif val == "N" or val == "n":
        obstacles = False
    else:
        print("\n Opción no valida, no se agregaran obstaculos \n")
    createMaze()

def createMaze():
    m=maze(x,y)
    m.CreateMaze(loopPercent=50)
    a=agent(m,filled=True,footprints=True)

    m.tracePath({a:m.path})

    m.run()

def checkSizes(val_x, val_y):
    if val_x.isdigit() and val_y.isdigit():
        val_x = int(val_x)
        val_y = int(val_y)
        return val_x > 0 and val_y > 0
    else:
        return False

if '__main__' == __name__:
    configurationSize()