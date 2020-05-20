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
* agentDecision()

#### Proactive Agent:
 * 

### ToDos:
* uma função para verificar o ultimo movimento/rotate e se a posição se manteve a mesma, para o agente não ficar muito tempo "preso" na mesma posição muito tempo
* isAgentInFront; -> tinha esquecido
* tempo minimo para realizar deliveries disponíveis (?), se acabar antes gerar mais deliveries;
* ver time de execução. já tem o update do paused time.
* comunicação agent/company, company/agent;
* moveTo/sendTo: função que recebe as coordenadas de cada step do agent, quando ele tiver q voltar pra company pra recarregar ou enviar agent para outra coordenada especifica;

Based on [this tutorial](https://github.com/poly451/Tutorials/tree/master/Python:%20Create%20a%20Grid) to create what we have so far. Also, using sprit she uses for the agent.




