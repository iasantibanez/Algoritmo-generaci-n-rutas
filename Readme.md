L03 Ivan Santibañez / Pedro Miquel

GRAL. PROGRAMA:
	[INICIALIZACION]
	- Recibe una cantidad de amigos y un mapa cualquiera. Para ambos casos, el programa es capáz de recibir cualquier cantidad de amigos y cualquier mapa,
	  siempre y cuando este último sea rectangular (o cuadrado).
	- se ejecuta funcion crear mapa => crea una clase Tablero
	- se agrega las posiciones del tablero(nodo:"(x,y)") 
	- Se asigna aleatoramente a los amigos en el mapa, sólo en lugares donde puden ser asignados.
	- las comidas y los amigos seran "piezas" que se podran mover/serconsumidas al tablero (y a cada nodo)

		
EPISODIOS:
	mediante la ejecución del metodo run() del programa se ejecutan los ep:
	- Los movimientos se realizan por turno. Se realiza el moviemiento de 1 amigo y cuando termina, parte el movimiento de otro.
	por lo que G0 juega primero antes que G1
	- en cada turno la persona se preguta que hacer (set_objetivo) en donde decide si: mover, comer o quedarse estatico. (todo involucra 1 movimiento) 
	lo primero ocure cuando hay alimento disponible, lo segundo cuando se esta en una misma casilla de alimento y el tercero cuando ya no quedan mas alimentos o supera el limite de calorias a consumir
	- posterior de esto se ejecuta metodo respectivo dependiendo del objetivo
	- Se pregunta si se imprime mapa al final del ep o solo al final de todos los ep
	
	(*)al termino del algoritmo las personas terminan juntas dado que ninguna tiene prioridad en comida, solo deciden por distancia,
		y una vez que esta es consumida las personas tendran que trazar nueva ruta, por lo tanto cuando queda un solo alimento (y aun con capacidad de consumir)
		estos los amigos se dirijen a este obj hasta que el primero que llegue lo consuma.
		
	(**) esto podria ser ineficiente en el recorrido total de los amigos sin embargo permite lograr que cada alimento sea consumido por la persona mas cercana de lo contrario, 
		un amigo con un turno favorecido c/r a otro que elige despues podria fijar dicho objetivo incluso cuando la distancia sea mucho mayor (y solo por que elijio primero)
	
BÚSQUEDA:
	- Se realizaron los 3 algorítmos de búsqueda diferentes, los cuales son utilizados dependiendo de la elección del usuario. Cada uno de ellos
	  realiza la búsqueda de una manera distinta, y funcionan correctamente para cada una de las personas que son includas inicialmente en el mapa. 
	
	- A*: Adaptado según material de clases, construccion de costos f,g,h

	- BFS: recuperado desde el material de clases (Syllabus) y modificado con un break hasta que encuentra alimento

	- DFS: recuperado desde el material de clases (Syllabus) y modificado con un break hasta que encuentra alimento
		
	el procedimiento por ejemplo para la persona G0 es;
	1)buscar cada alimento por separado (segun metodo de busqueda fijo), 
	2)con esto se traza la ruta en base a las casillas exploradas para tener una direccion de movimiento
	3)posteriormente se elige el alimento que demoro menos en encontrar(iteraciones) 
	4)Finalmente el movimiento será según la direccion del mejor_objetivo(es decir siguiente paso en la ruta encontrada) 
	(*) en caso de estar en una casilla con comida los algoritmos dan una ruta con 1 elemento por lo que cuando se verifica el minimo este es elegido
	 y en base a la direccion retorna a la condicion "COMER"
	(**) funciones de utilidad (recuperar ruta) fueron sacados de : https://www.python.org/doc/essays/graphs/
	 
ORDENAMIENTO:

	- Ya resulto el problema de busqueda y comida. Se ejecuta para ordenar la lista. 
	
	- Cabe mencionar que se realizó primeramente un algoritmo propio, peor por temas de eficiencia, finalmente se adaptó el material entregado en clases 
	  para poder realizar el orden de manera eficiente.
	
	- Se entrega una lista de comida (objetos) que fue consumida durante el programa, y se imprime esta misma lista ordenada por calorías. 	 