import random
import math


#-------------------[CLASES]-------------------
class Persona:
    def __init__(self, value):
        self.name = value
        self.ubicacion = [] #Lista con las coordenadas del nodo. Por ej: [2,4]
        self.vecinos = [] #Lista de vecinos de cada nodo, donde cada item de la lista es una LISTA con las coordenadas de sus vecinos
        self.nodos_vecinos = []
        self.objetivo = None
        self.ruta = []
        self.alimentos=[]
        self.cal_consumidas=0
        self.max_calorias = 4000
    def set_objetivo(self,objetivo):
        self.objetivo = objetivo
    def alimentarse(self,comida):
        self.alimentos.append(comida)
        self.cal_consumidas+=comida.calorias
    def __repr__(self):
        return self.name


class Comida:
    def __init__(self, value):
        self.name = 'Comida n° : ' + str(value)
        self.tipo = ""
        self.ubicacion = [] #Lista con las coordenadas del nodo. Por ej: [2,4]
        self.calorias = 0
        self.en_la_mira = False
    def set_calorias(self):
        if self.tipo == 'C':
            self.calorias = 500
        elif self.tipo == 'A':
            self.calorias = 300
        elif self.tipo == 'E':
            self.calorias = 600
        elif self.tipo == 'T':
            self.calorias = 200
    def __repr__(self):
        return self.tipo

class Node:
    def __init__(self,pos_x,pos_y):
        self.name = (pos_x,pos_y)     #(x,y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.costo_g = 0
        self.costo_h = 0
        self.costo_f = 0
        self.caminable = False
        self.antecesor = None
        self.vecinos = []      # casillas adyacentes
        self.contenido = []   # comida y/o personas en la c    def set_vecinos(self,list):
        self.vecinos.append(list)
    def __repr__(self):
        return str(self.name)

class Graph:
    def __init__(self):
        self.lista_nodos = []
        self.lista_amigos = []
        self.dicc_comidas = {}
        self.q_comida = 0  # cantidad de comida en el tablero
        self.nodos_map = {}  # dicc[x,y]=nodo
        self.nodos_vecinos={} # dicc[nodo]=vecinos
        self.alimentos_consumidos=[]

    def imprimir_mapa(self):
        for i in self.mapa:
            print(i)


    def agregar_nodo(self,nodo):
        self.nodos_map[nodo.name]=nodo
        self.nodos_vecinos[nodo.name]=self.encontrar_vecinos_pos(nodo.pos_x,nodo.pos_y)

    def agregar_amigos(self,amigo):
        self.lista_amigos.append(amigo)

    def agregar_mapa(self,mapa):
        self.mapa = mapa[:]
        self.largo_mapa = len(mapa)
        self.ancho_mapa = len(mapa[0])
        contador = 0
        contador1 = -1
        for i in self.mapa:
            contador1 += 1
            contador2 = -1
            for m in i:
                contador2 += 1
                pos_x,pos_y = contador1,contador2
                nodo = Node(pos_x,pos_y)
                nodo.vecinos = self.encontrar_vecinos_pos(pos_x,pos_y)
                self.agregar_nodo(nodo)
                self.lista_nodos.append(nodo)
                # agregar contenido (COMIDA) a las posiciones del tablero (nodos).
                if m != 'X' and m != '_':
                    self.q_comida+=1
                    comida = Comida(self.q_comida)
                    comida.tipo = m
                    comida.ubicacion = [pos_x,pos_y]
                    comida.set_calorias()
                    nodo.contenido.append(comida)
                    nodo.caminable = True
                    self.dicc_comidas[(pos_x,pos_y)]= comida
                    #self.lista_comidas.append(comida)

                elif m == '_':
                    nodo.caminable = True
                elif m == 'X':
                    nodo.caminable = False
                contador += 1

    def asignar_amigo_a_mapa(self,n_amigos):
        for i in range(n_amigos):
            nombre='G'+str(i)
            persona=Persona(nombre)
            self.agregar_amigos(persona)
            x=random.randint(0,(len(self.mapa)-1))
            y=random.randint(0,(len(self.mapa[0])-1))
            #verifica posicion valida
            while True :
                if self.mapa[x][y] == '_' :
                    self.mapa[x][y] = str(nombre)
                    break
                elif self.mapa[x][y] == 'X':
                    x=random.randint(0,(len(self.mapa)-1))
                    y=random.randint(0,(len(self.mapa[0])-1))
                else:
                    a=self.mapa[x][y]
                    self.mapa[x][y] = a + ',' +str(nombre)
                    break
            persona.ubicacion = [x,y]
            persona.vecinos = self.encontrar_vecinos_pos(x,y)
            self.nodos_map[x,y].contenido.append(persona)

    def encontrar_vecinos_pos(self, x, y):
        coord = [x,y]
        vecinos = []
        arriba_abajo = [-1, 1]
        for i in range(len(arriba_abajo)):
            x = coord[0]
            y = coord[1] + arriba_abajo[i]
            if y >= 0 and y < len(self.mapa[0]) :
                vecinos.append((x, y))

        for i in range(len(arriba_abajo)):
            x = coord[0] + arriba_abajo[i]
            y = coord[1]
            if x >= 0 and x < len(self.mapa):
                vecinos.append((x, y))
        return (vecinos)
    def comer(self,persona):
        pos_x=persona.ubicacion[0]
        pos_y=persona.ubicacion[1]
        contenido_celda=self.mapa[pos_x][pos_y]
        contenido_celda = contenido_celda.split(',')
        comida = contenido_celda[0]
        # se elimina comida del contenido del nodo y mapa
        contenido_celda.remove(comida)
        pop=self.dicc_comidas[(pos_x,pos_y)]        # se guarda para eliminarlo del contenido del nodo
        self.alimentos_consumidos.append(pop)       # se guarda como alimento "consumido" del tablero (registro)
        self.dicc_comidas.pop((pos_x,pos_y), None) # se elimina del dicc_comidas (disponibles)
        self.nodos_map[pos_x,pos_y].contenido.remove(pop)
        # se alimenta a la persona
        persona.alimentarse(pop)
        #contenido restante a mapa
        self.mapa[pos_x][pos_y]=''
        a=''
        for j in contenido_celda:
            self.mapa[pos_x][pos_y]+= a + j
            a=','

    def moverse(self,persona):
        pos_x=persona.ubicacion[0]
        pos_y=persona.ubicacion[1]
        contenido_celda=self.mapa[pos_x][pos_y]
        contenido_celda = contenido_celda.split(',')
        #eliminar a amigo de posicion pre-mov
        contenido_celda.remove(persona.name)
        #dejar posicion pre-mov ok
        if len(contenido_celda) == 0:
            self.mapa[pos_x][pos_y]='_'
        else:
            self.mapa[pos_x][pos_y]=''
            a=''
            for j in contenido_celda:
                self.mapa[pos_x][pos_y]+=a+j
                a=','
        #modificar posicion siguiente
        next_pos=persona.ruta[1]
        contenido_celda_prox=self.mapa[next_pos[0]][next_pos[1]]
        contenido_celda_prox=contenido_celda_prox.split(',')
        if contenido_celda_prox[0] == '_':
            self.mapa[next_pos[0]][next_pos[1]] = persona.name
        else:
            contenido_celda_prox.append(persona.name)
            self.mapa[next_pos[0]][next_pos[1]]=''
            a=''
            for j in contenido_celda_prox:
                self.mapa[next_pos[0]][next_pos[1]]+= a+j
                a=','
        #setear la posicion actual de la Persona
        persona.ubicacion=[next_pos[0],next_pos[1]]

    def ordenamiento(self):
        lista = self.preordenamiento()
        lista_ordenada = self.merge_sort(lista)
        lista_ordenada_comida = []
        for i in lista_ordenada:
            if i == 200:
                lista_ordenada_comida.append("Terremoto: {} calorías".format(i))
            if i == 300:
                lista_ordenada_comida.append("Anticucho: {} calorías".format(i))
            if i == 500:
                lista_ordenada_comida.append("Choripán: {} calorías".format(i))
            if i == 600:
                lista_ordenada_comida.append("Empanada: {} calorías".format(i))

        print(lista_ordenada_comida)

    def preordenamiento(self):
        lista_a_ordenar = []
        for i in self.alimentos_consumidos:
            lista_a_ordenar.append(i.calorias)
        return lista_a_ordenar

    def merge(self, left, right):
        result = []
        left_idx, right_idx = 0, 0
        while left_idx < len(left) and right_idx < len(right):
            if left[left_idx] <= right[right_idx]:
                result.append(left[left_idx])
                left_idx += 1
            else:
                result.append(right[right_idx])
                right_idx += 1

        if left:
            result.extend(left[left_idx:])
        if right:
            result.extend(right[right_idx:])
        return result

    def merge_sort(self, m):
        if len(m) <= 1:
            return m

        middle = len(m) // 2
        left = m[:middle]
        right = m[middle:]

        left = self.merge_sort(left)
        right = self.merge_sort(right)
        return list(self.merge(left, right))

#-------------------[FUNCIONES]-------------------crear tablero, busqueda, set objetivo       

def crear_tablero(n_amigos,mapa):
    tablero = Graph()
    tablero.agregar_mapa(mapa)
    tablero.asignar_amigo_a_mapa(n_amigos)
    return tablero

def busqueda(opc,origen,destino):
    #-----------Funciones utiles para trazar ruta y distancia entre casillas--------------
    def recuperar_ruta(lista_antecesores):
        ruta=lista_antecesores
        if Tablero.nodos_map[lista_antecesores[-1]].antecesor == None:
            return ruta
        else:
            ant=Tablero.nodos_map[lista_antecesores[-1]].antecesor
            ruta.append(ant)
            recuperar_ruta(ruta)
        return ruta[::-1]

    def find_shortest_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if start not in graph:
            return None
        shortest = None
        for node in graph[start]:
            if node not in path:
                newpath = find_shortest_path(graph, node, end, path)
                if newpath:
                    if not shortest or len(newpath) < len(shortest):
                        shortest = newpath
        return shortest

    def heuristic_cost_estimate(n1, n2):   # distancia_euclidiana   
        (x1, y1) = n1
        (x2, y2) = n2
        #suma= abs(x1 - x2) + abs(y1 - y2)  # distancia_Manhattan 
        return math.hypot(x2 - x1, y2 - y1)

    def distance_between(n1, n2):   # distancia 1 entre adyacentes (ya que solo se mueven en dirección horizontal y vertical) 
        return int(1)
        #return (ruta)
    #-------------funciones de busqueda de obj----------------------
    def a_star(origen,destino):
        #busca ruta segun Aestrella
        hay_ruta=False
        nodo_inicial=origen
        nodo_destino=destino
        lista_abierta = [nodo_inicial]# lista abierta
        lista_cerrada = []# lista vacia cerrada
        dicc_costo ={}
        Tablero.nodos_map[nodo_inicial].costo_g=0
        Tablero.nodos_map[nodo_inicial].costo_h=heuristic_cost_estimate(nodo_inicial,nodo_destino)
        Tablero.nodos_map[nodo_inicial].costo_f= Tablero.nodos_map[nodo_inicial].costo_g + Tablero.nodos_map[nodo_inicial].costo_h
        Tablero.nodos_map[nodo_inicial].antecesor = None
        dicc_costo[nodo_inicial]=Tablero.nodos_map[nodo_inicial].costo_f
        contador=0
        while True:
            contador+=1
            nodo_activo=(min(dicc_costo, key=dicc_costo.get))
            if Tablero.nodos_map[nodo_destino].caminable == False:
                print("no hay rutas")
                break
            if nodo_activo == nodo_destino:
                hay_ruta=True
                break
                return [nodo_activo]
            else:
                vecinos=Tablero.encontrar_vecinos_pos(nodo_activo[0],nodo_activo[1])
                for nodo_vecino in vecinos:
                    if Tablero.nodos_map[nodo_vecino].caminable == True:
                        if nodo_vecino not in lista_abierta:
                            Tablero.nodos_map[nodo_vecino].costo_g=distance_between(nodo_vecino,nodo_activo)+Tablero.nodos_map[nodo_activo].costo_g
                            Tablero.nodos_map[nodo_vecino].costo_h=heuristic_cost_estimate(nodo_inicial,nodo_destino)
                            Tablero.nodos_map[nodo_vecino].costo_f= Tablero.nodos_map[nodo_vecino].costo_g + Tablero.nodos_map[nodo_vecino].costo_h
                            Tablero.nodos_map[nodo_vecino].antecesor = nodo_activo
                            dicc_costo[nodo_vecino]=Tablero.nodos_map[nodo_vecino].costo_f
                            lista_abierta.append(nodo_vecino)
            dicc_costo.pop(nodo_activo, None)
            Limite=Tablero.largo_mapa*Tablero.ancho_mapa
            if contador == Limite: #hacer anchoxlargo it, si esque aun no encuentra
                break
        #metodo recursivo para recuperar ruta_metodo1
        if hay_ruta == True:
            ruta_M1=recuperar_ruta([nodo_destino])
        else:
            ruta_M1=None
        return ruta_M1,contador


    def BFS(origen,destino):
        #busca objetivo segun BFS
        nodo_inicial = origen
        nodo_destino = destino
        dicc_nodos_vecinos = {}
        hay_ruta=False
        visited,queue = list(),[nodo_inicial]
        iteraciones=0
        while queue:
            iteraciones+=1
            vertex = queue.pop(0)
            if vertex not in visited:
                visited.append(vertex)
                for v in Tablero.nodos_vecinos[vertex]:
                    if v not in visited:
                        if Tablero.nodos_map[v].caminable == True:
                            queue.append(v)
            if nodo_destino in visited:
                hay_ruta=True
                break
        #-----------creo dicc_aux con nodos en visited y admisibles para encontrar path----------
        dicc_aux={}
        for i in visited:
            vecinos=Tablero.encontrar_vecinos_pos(i[0],i[1])
            lista_aux=[]
            #vecino factible
            for vecino in vecinos:
                if Tablero.nodos_map[vecino].caminable == True:
                    lista_aux.append(vecino)
            dicc_aux[i]=lista_aux
        #-----------------------------------------------------

        #recupero mejor_ruta
            
        ruta_M2=find_shortest_path(dicc_aux, nodo_inicial, nodo_destino, path=[])
        #print(visited,"caminosrecorridos")
        #print(ruta_M2,"rutaoptima")
        return ruta_M2,len(visited)


    def DFS(origen,destino):
        #busca objetivo segun DFS
        nodo_inicial = origen
        nodo_destino = destino
        dicc_nodos_vecinos = {}
        hay_ruta=False
        visited,stack = list(),[nodo_inicial]
        iteraciones=0
        while stack:
            iteraciones+=1
            vertex=stack.pop()
            if vertex not in visited:
                visited.append(vertex)
                for v in Tablero.nodos_vecinos[vertex]:
                    if v not in visited:
                        if Tablero.nodos_map[v].caminable == True:
                            stack.append(v)
            #BUSCA DFS HASTA ENCONTRAR EL BUSCADO
            if nodo_destino in visited:
                hay_ruta=True
                break
        #-----------creo dicc_aux con nodos admisibles para encontrar path----------
        dicc_aux={}
        for i in visited:
            vecinos=Tablero.encontrar_vecinos_pos(i[0],i[1])
            lista_aux=[]
            #vecino factible
            for vecino in vecinos:
                if Tablero.nodos_map[vecino].caminable == True:
                    lista_aux.append(vecino)
            dicc_aux[i]=lista_aux
        #-----------------------------------------------------

        #recupero mejor_ruta
        ruta_M3=find_shortest_path(dicc_aux, nodo_inicial, nodo_destino, path=[])
        #print(visited,"caminosrecorridos")
        #print(ruta,"rutaoptima")
        return ruta_M3,len(visited)


    if opc==1:
        ruta = a_star(origen,destino)
        #print("metodo1")

    elif opc==2:
        ruta = BFS(origen,destino)
        #print("metodo2")

    elif opc==3:
        ruta = DFS(origen,destino)
        #print("metodo3")

    return ruta 

def set_objetivo(metodo,persona):
    destinos_tentativos={}
    mejor_destino=''
    mejor_comida=''
    origen=persona.ubicacion
    rutas_tentativas={}
    hay_comida = True
    if len(Tablero.dicc_comidas)>0: # si hay comidas disponibles
        for i in Tablero.dicc_comidas:
            comida=Tablero.dicc_comidas[i]
            if comida.en_la_mira == False: # se intento implementar que obj fueran distintos pero se propone que no es tan eficiente (readme)
                destino=comida.ubicacion
                ruta_metodo,iteraciones=busqueda(metodo,(origen[0],origen[1]),(destino[0],destino[1]))
                rutas_tentativas[(destino[0],destino[1])] = ruta_metodo
                destinos_tentativos[(destino[0],destino[1])]=len(ruta_metodo)
        mejor_destino = (min(destinos_tentativos, key=destinos_tentativos.get))
        mejor_comida = Tablero.dicc_comidas[mejor_destino]
        mejor_ruta=rutas_tentativas[(mejor_destino[0],mejor_destino[1])]
    else:  #no hay comidas disponibles
        mejor_destino = origen
        mejor_comida = None
        mejor_ruta = [mejor_destino[0],mejor_destino[1]]
        hay_comida = False

    # caso 1 : estar en la posicion de algun alimento
    if (origen[0],origen[1]) == mejor_destino and hay_comida:
        obj='comer'
    # caso 2: no estar en posicion pero ya haber consumido las calorias maximas
    elif hay_comida and persona.cal_consumidas + mejor_comida.calorias > persona.max_calorias:
        obj='estatico'
    # Caso 3 : no hay mas comida disponible en tablero
    elif hay_comida == False:
        obj='estatico'
    # Caso 4: hay comida pero tengo que moverme para alcanzarla
    else:
        obj='mover'

    return obj,mejor_ruta



##-------------------[CLASE MAESTRA]-------------------  (para ejecutar turnos,episodios,creacion de tablero y outputs pedidos)

class Programa():
    def __init__(self, n_amigos, mapa):
        print("INICIALIZACION")
        self.n_amigos = n_amigos
        self.mapa = mapa
        self.tablero_aux = crear_tablero(n_amigos,mapa)
        self.tipo_busqueda=1       # A* default, de igual se modifica dicho atributo segun elección.
        self.limite_episodios=200  # it maximas de ep, para comerse toda la comida en tablero
        #Muestra mapa inicial
        print("Tablero Inicial")
        self.tablero_aux.imprimir_mapa()
        print("________________________")
        self.imprimir = 1
        self.eventos= {} #guarda acciones y posiciones de c/persona segun episodio (turnos)  self.eventos[n_episodio]=lista[N° persona_GX] 
        self.tupla_pos = [] # lista que guarda tupla de pos en k-esimo episodio (parte de 0 como el ep n°0)

    def run(self):
        #pos inicial
        for i in range(self.n_amigos):
            self.tupla_pos.append([])
            pos_0_x=self.tablero_aux.lista_amigos[i].ubicacion[0]
            pos_0_y=self.tablero_aux.lista_amigos[i].ubicacion[1]
            self.tupla_pos[i].append((pos_0_x,pos_0_y))
            
        #comienzo de los turnos y episodios
        contador_ep=0
        while len(Tablero.dicc_comidas)>0:  # se ejecuta hasta que no hayan comidas
            contador_ep+=1
            lista_E_episodio=[]
            #turnos por amigo
            for i in Tablero.lista_amigos:
                #setear objetivo a realizar segun metodo de busqueda y posición
                i.objetivo_actual,i.ruta=set_objetivo(self.tipo_busqueda,i) # se setea el mejor objetivo según la opc
                #verificar si objetivo es comer o caminar o quedarse.
                if i.objetivo_actual == 'comer' and i.cal_consumidas < 4000 :    
                    #print("[COMER]",i,i.ubicacion)
                    Tablero.comer(i)
                    aux=str(i)+"[COMER]"+str(i.ubicacion)
                    lista_E_episodio.append(aux)
                    id=int(i.name[1])
                    self.tupla_pos[id].append((i.ubicacion[0],i.ubicacion[1]))

                elif i.objetivo_actual == 'mover':
                    ant=i.ubicacion
                    Tablero.moverse(i)
                    aux=str(i)+"[MOVERSE]"+str(ant)+"----->"+str(i.ubicacion)
                    #print("[MOVERSE]",i,ant,"----->",i.ubicacion)
                    lista_E_episodio.append(aux)
                    id=int(i.name[1])
                    self.tupla_pos[id].append((i.ubicacion[0],i.ubicacion[1]))
                else:
                    #print("[ESTATICO]",i,i.ubicacion)
                    aux=str(i)+"[ESTATICO]"+str(i.ubicacion)
                    lista_E_episodio.append(aux)
                    id=int(i.name[1])
                    self.tupla_pos[id].append((i.ubicacion[0],i.ubicacion[1]))

                
            # guarda eventos por episodio
            self.eventos[contador_ep]=lista_E_episodio
                
            if contador_ep == self.limite_episodios: #contador limite de it en caso de no encontrar comida en demasiados turnos (DEFAULT:300 epsodios)
                print("\nSe ha alcanzado el limite de episodios antes de consumir el total de comidas")				
                break
            
            # pregunta por impresion mapa 
            if self.imprimir == 1:
                while True:
                    print("Siguiente episodio: \n1)imprimir el episodio \n2)imprimir episodio final")
                    self.imprimir = input("ingresa opcion: ")
                    if self.imprimir == '1':
                        self.imprimir = int(self.imprimir)
                        self.impresion(1,contador_ep)
                        break
                    elif self.imprimir =='2':
                        self.imprimir = int(self.imprimir)
                        break
                    else:
                        print("opc invalida, intenta de nuevo")
                        print("________________________")

            else: # si la opc es 2, no hacer nada hasta que termine.
                pass

        self.impresion(2,contador_ep)
        
        #revision de alimentos consumidos al estado final (se mutea porque esta incluido en el estado 2 de impresion)
                
        #self.alimentos_consumidos()
        
    def alimentos_consumidos(self):
        for i in Tablero.lista_amigos:
            print(i.name,"\ncalorias consumidas:",i.cal_consumidas,'\nalimentos consumidos:',i.alimentos)

    def impresion(self,opc,contador_ep):
        if opc == 1: #Tablero x episodio en particular 
            print("\nEpisodio N:",contador_ep)
            Tablero.imprimir_mapa()
            print("\nEVENTOS: \nPersona [TIPO] [ubicacion] ")     # MUTEAR ACA PARA OMITIR IMPRESION DE EVENTOS X EP 
            self.imprimir_eventos(contador_ep)                    # MUTEAR  "
            print("________________________")
        else: # Tablero final
            print("\nTablero Final")
            print("Episodio N:",contador_ep)
            Tablero.imprimir_mapa()
            print("\n[FINAL CONSUMIDO]")
            self.alimentos_consumidos()
            print("\n[TUPLAS POSICION]")
            self.imprimir_tuplas_pos()
            print("________________________")
            
    def imprimir_eventos(self,contador_ep):  # se usa como info adicional para la impresion x ep
        for i in self.eventos[contador_ep]:
           print(i)
           
    def imprimir_tuplas_pos(self):  #parte desde la posicion inicial = episodio 0
        for i in range(self.n_amigos):
            print('G'+str(i),'\n'+str(self.tupla_pos[i]))
        #print("hola")
        #print(self.tablero_aux.alimentos_consumidos)
            








lista2 = \
    [['E', '_', '_', '_', '_', 'X', 'C' ],
    ['_', '_', '_' , '_', 'E', 'X', '_' ],
    ['X', 'X', 'X' , 'X', '_', 'X', '_' ],
    ['_', 'T', '_' , 'X', '_', 'X', '_' ],
    ['_', '_', '_' , 'X', '_', 'X', '_' ],
    ['_', 'X', '_' , '_', '_', '_', '_' ],
    ['_', 'X', '_' , '_', '_', '_', 'C']]

lista = \
    [['C','_', 'E', 'X' , '_', '_','C', 'X', '_', 'C', 'T' , 'X', '_'],
    ['_','X', '_', 'X' , 'A', 'X','_', 'X', '_', 'X', '_' , 'X', 'C'],
    ['_','X', 'C', 'X' , '_', 'X','C', 'X', '_', 'X', '_', 'X', '_'],
    ['C','X', '_', 'G1', '_', 'X','_', '_', 'T', 'X', '_' , '_', 'C']]



print("porfavor eliga un metodo de busqueda de comidas")
print("1) A* \n2) BFS \n3) DFS")
while True:
	metodo_busqueda=input("inserte metodo de resolucion:")
	if metodo_busqueda == '1':
		break
	elif metodo_busqueda == '2':
		break
	elif metodo_busqueda == '3':
		break
	else:
		print("inserte metodo de resolucion valido")
#-----------busqueda_comida--------------
programa = Programa(4, lista)
Tablero=programa.tablero_aux
programa.tipo_busqueda = int(metodo_busqueda)
programa.run()
#-----------ordenamiento-----------------
print("[ALIMENTOS CONSUMIDOS ORDENADOS]")
programa.tablero_aux.ordenamiento() 
