from pyamaze import maze,agent
from queue import PriorityQueue

#ToDo
'''
* Posicionar meta
* Posicionar agente
* Cronometro
* Obstaculos
* Pruebas
'''

# Dimensiones para el laberinto
x = 0
y = 0

# Meta del laberinto
goal_x = 1
goal_y = 1

# Posicion del agente
#agent_x
#agent_y

# Funcion para indicar el tamaño deseado para el algoritmo
def configurationSize():
    global x, y 
    print("\n[ Defina el tamaño del laberinto ]\n")
    val_x = input("Tamaño en X: ")
    val_y = input("Tamaño en Y: ")

    # Verifica que los tamaños seleccionados para el laberinto son validos y lo crea
    if (checkSizes(val_x, val_y)):
        x = int(val_x)
        y = int(val_y)
        createMaze()
    else:
        print("\nTamaños no validos")
        configurationSize()

# Verifica que los tamaños sean positvos y que se ingresaron enteros
def checkSizes(val_x, val_y):
    if val_x.isdigit() and val_y.isdigit():
        val_x = int(val_x)
        val_y = int(val_y)
        return val_x > 0 and val_y > 0
    else:
        return False

# Calcula el valor heuristico h, en este caso sera la distancia manhatan
# La cantidad de celdas en x más la cantidad de celdas en y que existe
# entre n y la meta
def calculate_h(c1, c2):
    x1,y1 = c1
    x2,y2 = c2

    return abs(x1-x2) + abs(y1-y2)

# Comienza el calculo de el algoritmo A*
def aStar_calculation(maze, start):
    g_score={cell:float('inf') for cell in maze.grid}
    g_score[start] = 0

    f_score={cell:float('inf') for cell in maze.grid}
    f_score[start] = calculate_h(start, maze._goal)

    open = PriorityQueue()
    open.put((calculate_h(start,maze._goal), calculate_h(start,maze._goal), start))

    aPath = {}

    while not open.empty():
        currentCell = open.get()[2]
        if currentCell == maze._goal:
            break
        for d in 'ESNW':
            if maze.maze_map[currentCell][d] == True:
                match d:
                    case "E":
                        childCell = (currentCell[0], currentCell[1]+1)
                    case "W":
                        childCell = (currentCell[0], currentCell[1]-1)
                    case "N":
                        childCell = (currentCell[0]-1, currentCell[1])
                    case "S":
                        childCell = (currentCell[0]+1, currentCell[1])

                temp_g_score = g_score[currentCell] + 1
                temp_f_score = temp_g_score + calculate_h(childCell, maze._goal)

                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open.put((temp_f_score, calculate_h(childCell, maze._goal), childCell))
                    aPath[childCell] = currentCell

    forwardPath = {}
    cell = maze._goal
    while cell != start:
        forwardPath[aPath[cell]] = cell
        cell = aPath[cell]
    return forwardPath


def createMaze():
    m = maze(x, y)

    # Aqui se definira donde se posicionara la meta
    m.CreateMaze(goal_x, goal_y)
    
    print(m.maze_map)

    #Aqui donde se posicionara el n
    path = aStar_calculation(m, (m.rows, m.cols))

    # Se identifica nuevamente donde se posiciona el agente
    a = agent(m, m.rows, m.cols, footprints=True, filled=True)
    m.tracePath({a:path})

    m.run()

if '__main__' == __name__:
    configurationSize()