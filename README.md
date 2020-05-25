# aasma_project

## Delivery World Using Robots

#### HOW TO RUN:

* É necessário instalar o pygame para correr o projeto!

* In your terminal go to the directory of the main.py file and  run "python main.py" or "python3 main.py"

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

#### HOW TO RUN:

Interface based on [this tutorial](https://github.com/poly451/Tutorials/tree/master/Python:%20Create%20a%20Grid) to create what we have so far. Also, using sprit she uses for the agent.




