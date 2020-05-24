# aasma_project

## Delivery World Using Robots

### FILES:
* main.py: create world instance and start. Always check whether it has been paused or not.
* constants.py: auxiliary constants, colors, rotation object, map file.

* world.py: create instances of all objects needed to start the world, all based on the map file. A static number of deliveries is also generated.

* Buildings.py, Cells.py, Company.py, Deliveries.py, Obstacles.py and Walls.py: classes to create world objects.
	- cells, companies, obstacles and agents use sprite images.

* WorldObject.py: class the to assist access/manipulation of world objects.

* utils.py: some functions that are used more than once in different files.
* CompanyAgent.py: Creates company agents. As robots are agents of a company, they are created through this class. It implements a kind of communication with the robot agents: if the agent has a low battery, "ask" the company what to do. For reactives, the company calculates the distance between the drop point and the headquarters and sees what is the best task to be performed.

Use bfs to compute the best path to the nearest point.

Build world with normal cells, walls and a few buildings (simple map used, see a better one and bigger later).
* ESC to quit;
* space key to make the agent move\stop.

* obstacles are static for now (the code to be generated randomly stil works, just need to uncomment);

Agent decision:
* working with sensors and actuators so far;
* updateAgent -> used to update agent when they pick/drop delivery. Useful when checking if agent is carring a delivery;

### DONE:

#### Basic Agent:
* aheadPosition -> update agents direction/orientation;
* move;
* rotate and rotate180;
* pickUpDelivery;
* dropDelivery;
* agentStop;
* prepareRecharge and recharge;
* checkTimeIteraction;
* avoidObstacles;

And detect if there is (Sensors):
* wall (isWall);
* building (isBuilding);
* has delivery in building/pick up point (hasDelivery);
* has obstacle, deflect if there is one (hasObstacle);
* agent has delivery (agentHasDelivery);
* delivery point/drop put point (isDeliveryPoint);
* getBattery;
* isLowBattery;
* isHeadQuarters;

#### Reactive:
* agentDecision();
* same thing as BasicAgents;

### Company Agemt:
* distanceTo: Euclidian distance between two points;
* bfs_map: generate path based on coodinates visited by agent. -> incompleto.
* floodFill: get all positions visited by the agent and and mark each position (has a bug). Not being used.

#### Proactive Ideas:
*
* Criar matrix para armazenar as cells q o agent passou e o buildings q ele encontrou (igual a worldObjects e agents). As cells da company tbm. Se ele estiver carregando uma delivery e encontrar um outro predio com delivery, colocar esse predio em outro array (ou algo assim). Quando terminar a delivery verifica se ainda existe alguma delivery para ser entregue nos predios q ele detectou anteriormente e que tinham delivery.

* checkSurroundings:
	-verifica as cells ao redor do agent para analizar a melhor ação. Se ao redor houver algum prédio já detectado anteriormente e não tem delivery o agente faz rotate ou continua se movendo para outro local. Se tiver a company e a bateria estiver baixa vai carregar.
	-se o agent tiver uma delivery e ao redor houver algum prédio ele vai para este predio.

* moveTo:
	-como o agente vai ter seu propio mapa do mundo ele pode gerar um caminho para um determinado ponto baseado nisso, se necessário.


### ToDos:
* (?) uma função para verificar o ultimo movimento/rotate e se a posição se manteve a mesma, para o agente não ficar muito tempo "preso" na mesma posição muito tempo
* (?) moveTo/sendTo: função que recebe as coordenadas de cada step do agent, quando ele tiver q voltar pra company pra recarregar ou enviar agent para outra coordenada especifica;

Based on [this tutorial](https://github.com/poly451/Tutorials/tree/master/Python:%20Create%20a%20Grid) to create what we have so far. Also, using sprit she uses for the agent.




