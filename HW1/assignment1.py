# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

# Tutorial sample #7: The Maze Decorator

try:
    from malmo import MalmoPython
except:
    import MalmoPython

import os
import sys
import time
import json
import math
import time
import heapq
from priority_dict import priorityDictionary as PQ

# sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

def GetMissionXML(seed, gp, size=10):
    return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Hello world!</Summary>
              </About>

            <ServerSection>
              <ServerInitialConditions>
                <Time>
                    <StartTime>1000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                </Time>
                <Weather>clear</Weather>
              </ServerInitialConditions>
              <ServerHandlers>
                  <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
                  <DrawingDecorator>
                    <DrawSphere x="-27" y="70" z="0" radius="30" type="air"/>
                  </DrawingDecorator>
                  <MazeDecorator>
                    <Seed>'''+str(seed)+'''</Seed>
                    <SizeAndPosition width="''' + str(size) + '''" length="''' + str(size) + '''" height="10" xOrigin="-32" yOrigin="69" zOrigin="-5"/>
                    <StartBlock type="emerald_block" fixedToEdge="true"/>
                    <EndBlock type="redstone_block" fixedToEdge="true"/>
                    <PathBlock type="diamond_block"/>
                    <FloorBlock type="air"/>
                    <GapBlock type="air"/>
                    <GapProbability>'''+str(gp)+'''</GapProbability>
                    <AllowDiagonalMovement>false</AllowDiagonalMovement>
                  </MazeDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="10000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Survival">
                <Name>CS175AwesomeMazeBot</Name>
                <AgentStart>
                    <Placement x="0.5" y="56.0" z="0.5" yaw="0"/>
                </AgentStart>
                <AgentHandlers>
                    <DiscreteMovementCommands/>
                    <AgentQuitFromTouchingBlockType>
                        <Block type="redstone_block"/>
                    </AgentQuitFromTouchingBlockType>
                    <ObservationFromGrid>
                      <Grid name="floorAll">
                        <min x="-10" y="-1" z="-10"/>
                        <max x="10" y="-1" z="10"/>
                      </Grid>
                  </ObservationFromGrid>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''


def load_grid(world_state):
    """
    Used the agent observation API to get a 21 X 21 grid box around the agent (the agent is in the middle).

    Args
        world_state:    <object>    current agent world state

    Returns
        grid:   <list>  the world grid blocks represented as a list of blocks (see Tutorial.pdf)
    """
    while world_state.is_mission_running:
        #sys.stdout.write(".")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        if len(world_state.errors) > 0:
            raise AssertionError('Could not load grid.')

        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            observations = json.loads(msg)
            grid = observations.get(u'floorAll', 0)
            break
    return grid

def find_start_end(grid):
    """
    Finds the source and destination block indexes from the list.

    Args
        grid:   <list>  the world grid blocks represented as a list of blocks (see Tutorial.pdf)

    Returns
        start: <int>   source block index in the list
        end:   <int>   destination block index in the list
    """
    #------------------------------------
    #
    #   Fill and submit this code
    #
    start = 0
    end = 0
    for i in range(len(grid)):
        if grid[i] == "emerald_block":
            start = i
        elif grid[i] == "redstone_block":
            end = i
    return (start, end)
    #-------------------------------------

def extract_action_list_from_path(path_list):
    """
    Converts a block idx path to action list.

    Args
        path_list:  <list>  list of block idx from source block to dest block.

    Returns
        action_list: <list> list of string discrete action commands (e.g. ['movesouth 1', 'movewest 1', ...]
    """
    action_trans = {-21: 'movenorth 1', 21: 'movesouth 1', -1: 'movewest 1', 1: 'moveeast 1'}
    alist = []
    for i in range(len(path_list) - 1):
        curr_block, next_block = path_list[i:(i + 2)]
        alist.append(action_trans[next_block - curr_block])

    return alist

def distance(coor, end):
    j = math.floor(coor / 21)
    i = coor % 21
    endj = math.floor(end / 21)
    endi = end % 21
    distance = math.sqrt(math.pow(i - endi, 2) + math.pow(j - endj, 2))
    return distance

def next_to(coor1, coor2):
    diff = coor1 - coor2
    if diff == -1 or diff == 1 or diff == -21 or diff == 21:
        return True
    else:
        return False

def inBounds(i, j):
    if i < 0 or i > 20 or j < 0 or j > 20:
        return False
    else:
        return True 

def dijkstra_shortest_path(grid_obs, source, dest):
    """
    Finds the shortest path from source to destination on the map. It used the grid observation as the graph.
    See example on the Tutorial.pdf file for knowing which index should be north, south, west and east.

    Args
        grid_obs:   <list>  list of block types string representing the blocks on the map.
        source:     <int>   source block index.
        dest:       <int>   destination block index.

    Returns
        path_list:  <list>  block indexes representing a path from source (first element) to destination (last)
    """
    #------------------------------------
    #
    #   Fill and submit this code
    #
    distances = []
    
    for i in range(len(grid_obs)):
        if grid_obs[i] != "air":
            distances.append((distance(i, dest), i))
    #print(distances)

    
    dist = distance(source, dest)
    hp = []
    path = []
    visited = [False for i in range(21 * 21)]
    heapq.heappush(hp, distance(source, dest))

    #pq[300] = [dist-0]
    #print(pq)
    #print(hp)
    dit = heapq.heappop(hp)
    dead = []
    elem = 0
    for i in distances:
        if i[0] == dit:
            elem = i[1]
    #print("Start: " + str(source))
    #print("End: " + str(dest))
    #print(hp)
    #print("Elem: " + str(elem))
    path.append(elem)
    while elem != dest:
        
        #print(grid_obs[elem])
        #print(inBounds(elem % 21 + 1, math.floor(elem/21)) and not visited[elem + 1] and grid_obs[elem + 1] != "air")
        #print(visited[elem - 1])
        #print(inBounds(elem % 21, math.floor(elem/21) + 1) and not visited[elem + 21] and grid_obs[elem + 21] != "air")
        #print(inBounds(elem % 21, math.floor(elem/21) - 1) and not visited[elem - 21] and grid_obs[elem - 21] != "air")
        visited[elem] = True
        #print("0: " + str(elem))
        added = 0
        if inBounds(elem % 21 + 1, math.floor(elem/21)) and not visited[elem + 1] and grid_obs[elem + 1] != "air":
            visited[elem + 1] = True
            #print("1: " + str(elem + 1))
            heapq.heappush(hp, distance(elem + 1, dest))
            added += 1
        if inBounds(elem % 21 - 1, math.floor(elem/21)) and not visited[elem - 1] and grid_obs[elem - 1] != "air":
            visited[elem - 1] = True
            #print("2: " + str(elem - 1))
            heapq.heappush(hp, distance(elem - 1, dest))
            added += 1
        if inBounds(elem % 21, math.floor(elem/21) + 1) and not visited[elem + 21] and grid_obs[elem + 21] != "air":
            visited[elem + 21] = True
            #print("3: " + str(elem + 21))
            heapq.heappush(hp, distance(elem + 21, dest))
            added += 1
        if inBounds(elem % 21, math.floor(elem/21) - 1) and not visited[elem - 21] and grid_obs[elem - 21] != "air":
            visited[elem - 21] = True
            #print("4: " + str(elem - 21))
            heapq.heappush(hp, distance(elem - 21, dest))
            added += 1
        if added == 0:
            dead.append(elem)
        #print(hp)
        dit = heapq.heappop(hp)
        for i in distances:
            if i[0] == dit and added == 0:
                elem = i[1]
            if i[0] == dit and next_to(elem, i[1]) and not i[1] in path:
                elem = i[1]
        #print(hp)
        path.append(elem)
    for i in dead:
        path.remove(i)
    #print("Path: " + str(path))
    
    return path
    #-------------------------------------

# Create default Malmo objects:
agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:',e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)

if agent_host.receivedArgument("test"):
    num_repeats = 1
else:
    num_repeats = 10

for i in range(num_repeats):
    size = int(6 + 0.5*i)
    print("Size of maze:", size)
    my_mission = MalmoPython.MissionSpec(GetMissionXML("0", 0.4 + float(i/20.0), size), True)
    my_mission_record = MalmoPython.MissionRecordSpec()
    my_mission.requestVideo(800, 500)
    my_mission.setViewpoint(1)
    # Attempt to start a mission:
    max_retries = 3
    my_clients = MalmoPython.ClientPool()
    my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available

    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_clients, my_mission_record, 0, "%s-%d" % ('Moshe', i) )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission", (i+1), ":",e)
                exit(1)
            else:
                time.sleep(2)

    # Loop until mission starts:
    print("Waiting for the mission", (i+1), "to start ",)
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        #sys.stdout.write(".")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)

    print()
    print("Mission", (i+1), "running.")

    grid = load_grid(world_state)
    start, end = find_start_end(grid) # implement this
    path = dijkstra_shortest_path(grid, start, end)  # implement this
    action_list = extract_action_list_from_path(path)
    print("Output (start,end)", (i+1), ":", (start,end))
    print("Output (path length)", (i+1), ":", len(path))
    print("Output (actions)", (i+1), ":", action_list)
    # Loop until mission ends:
    action_index = 0
    while world_state.is_mission_running:
        #sys.stdout.write(".")
        time.sleep(0.1)

        # Sending the next commend from the action list -- found using the Dijkstra algo.
        if action_index >= len(action_list):
            print("Error:", "out of actions, but mission has not ended!")
            time.sleep(2)
        else:
            agent_host.sendCommand(action_list[action_index])
        action_index += 1
        if len(action_list) == action_index:
            # Need to wait few seconds to let the world state realise I'm in end block.
            # Another option could be just to add no move actions -- I thought sleep is more elegant.
            time.sleep(2)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)

    print()
    print("Mission", (i+1), "ended")
    # Mission has ended.
