# aasma_project

## Delivery World Using Robots

Build world with normal cells, walls and a few buildings (simple map used, see a better one and bigger later).
* ESC to quit;
* space key to make the agent move\stop.

* obstacles are static for now (the code to be generated randomly stil works, just need to uncomment);

Agent decision:
* working with sensors and actuators so far;
* updateAgent -> used to update agent when they pick/drop delivery. Useful when checking if agent is carring a delivery;

It has initially one agent (reactive) with simple movemente:
* aheadPosition -> update agents direction/orientation;
* move;
* rotate;
* pickUpDelivery;
* dropDelivery;

And detect if there is (Sensors):
* wall (isWall);
* building (isBuilding);
* has delivery in building/pick up point (hasDelivery);
* has obstacle, deflect if there is one (hasObstacle);
* agent has delivery (agentHasDelivery);
* delivery point/drop put point (isDeliveryPoint);

Based on [this tutorial](https://github.com/poly451/Tutorials/tree/master/Python:%20Create%20a%20Grid) to create what we have so far. Also, using sprit she uses for the agent.




