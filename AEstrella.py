from pyamaze import maze,agent
from queue import PriorityQueue
import threading
import time

# Dimensiones para el laberinto
x = 0
y = 0

# Meta del laberinto
goal_x = 1
goal_y = 1

fin = False
movimientos = 0

# Posicion del agente
agent_x = 0
agent_y = 0

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
        configurationMeta()
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

#configuracion de la posiscion de la meta
def configurationMeta():
    print("\n [Defina la posicion de llegada ]\n")
    val_goal_x = input("Valor de llegada en X: ")
    val_goal_y = input("Valor de llegada en Y: ")
    if checkGoal(val_goal_x, val_goal_y):
        configurationAgent()
    else:
        print("\nPosicion no valida\n")
        configurationMeta()
    
def checkGoal(val_goal_x, val_goal_y):
    global goal_x, goal_y
    if val_goal_x.isdigit() and val_goal_y.isdigit():
        goal_x = int(val_goal_x)
        goal_y = int(val_goal_y)
        return ((goal_x > 0 and goal_y > 0) and (goal_x <= x and goal_y <= y))
    else:
        return False
        
#configuracion de la posicion del agente
def configurationAgent():
    print("\n [Defina la posicion del agente ]\n")
    val_agent_x = input("Valor del agente en X: ")
    val_agent_y = input("Valor del agente en Y: ")
    if checkPosAgent(val_agent_x, val_agent_y):
        createMaze()
    else:
        print("\nPosicion no valida\n")
        configurationAgent()

def checkPosAgent(val_agent_x, val_agent_y):
    global agent_x, agent_y
    if val_agent_x.isdigit() and val_agent_y.isdigit():
        agent_x = int(val_agent_x)
        agent_y = int(val_agent_y)
        return ((agent_x != goal_x or agent_y != goal_y) and (agent_x>0 and agent_y>0) and (agent_x <= x and agent_y <= y))
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

    global fin

    exit_event = threading.Event()

    timer_thread = threading.Thread(target=run_timer)
    timer_thread.start()

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
    fin = True
    exit_event.set()  # Asegura que el cronómetro también se detiene cuando la ventana se cierra
    timer_thread.join()  # Espera a que el hilo del cronómetro termine
    return forwardPath

def run_timer():
    start_time = time.time()
    while not fin:
        time.sleep(1)
        current_time = time.time() - start_time
        print( "Algoritmo A*: "+ str(current_time) + " segundos")

def imprimir_hilo():
    for i in range(movimientos):
        print("Duración de recorrido: " + str(i/3.1) + " segundos")
        time.sleep(0.31)

def createMaze():
    global movimientos
    m = maze(x, y)

    # Aqui se definira donde se posicionara la meta
    # Se puede modificar el loopPercent para variar la generacion de laberintos
    m.CreateMaze(goal_x, goal_y,loopPercent=0)
    
    #print(m.maze_map)

    #Aqui donde se posicionara el n
    path = aStar_calculation(m, (agent_x, agent_y))
    movimientos = len(path)
    # Se identifica nuevamente donde se posiciona el agente
    a = agent(m, agent_x, agent_y, footprints=True, filled=True)
    m.tracePath({a:path})
    thread1 = threading.Thread(target=imprimir_hilo)
    thread1.start()
    m.run()
    thread1.join()


if '__main__' == __name__:
    configurationSize()