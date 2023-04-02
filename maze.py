def random_population():  
    for i in range(popsize):
        pop=[randint(1,row) for j in range(1,column-1)]
        population.append([1]+pop+[row])        
        
def mutation():
    for i in population:
        i[randint(1,column-2)]=randint(1,row)  
      
def crossover():
    cutpoint=randint(0,column-1)
    
    for i in range(0, len(population)//2, 2):
        parent1 = deepcopy(population[i])
        parent2 = deepcopy(population[i+1]) 
        child1 = []
        child2 = []
        for j in range(len(parent1)):
            if j < cutpoint:
                child1.append(parent1[j])
                child2.append(parent2[j])
            else:
                child1.append(parent2[j])
                child2.append(parent1[j])
        population[popsize//2+i] = child1
        population[popsize//2+i+1] = child2

def turns():
    turn=0
    for i in population:
        turn= sum(1 for j in range (column-2) if i[j]!=i[j+1])
        Turns.append(turn+1)
        turn=0            

def fitness_function():
    turns()
    plan=[]
    if row==column:
        for i in population:
            for j in range(row-1):
                if i[j+1]-i[j]>=0:
                    for k in range(i[j],i[j+1]+1):
                        plan.append((k,j+1))
                if i[j+1]-i[j]<0:
                    for k in range(i[j],i[j+1]-1,-1):
                        plan.append((k,j+1))
            plan.append((row,column))
            path.append(plan)            
            plan=[]
    if row<column or row>column:
        for i in population:
            for j in range(column-1):
                if i[j+1]-i[j]>=0:
                    for k in range(i[j],i[j+1]+1):
                        plan.append((k,j+1))
                if i[j+1]-i[j]<0:
                    for k in range(i[j],i[j+1]-1,-1):
                        plan.append((k,j+1))
            plan.append((row,column))
            path.append(plan)            
            plan=[]

    obs=0
    for i in path:
        for j in range(len(i)-1):
            if i[j+1][0]-i[j][0]>=0 and i[j+1][1]==i[j][1] and map[(i[j])]["S"]==0 :
                obs+=1
            if i[j+1][0]-i[j][0]<0 and i[j+1][1]==i[j][1] and map[(i[j])]["N"]==0 :
                obs+=1
            if i[j+1][1]-i[j][1]>=0 and i[j+1][0]==i[j][0] and map[(i[j])]["E"]==0 :
                obs+=1
            if i[j+1][1]-i[j][1]<0 and i[j+1][0]==i[j][0] and map[(i[j])]["W"]==0 :
                obs+=1
        obstacles.append(obs)
        obs=0

    for i in path:
        no_of_steps.append(len(i))
                        
    w_obs,w_turn,w_path=3,2,2
    
    for i in range (popsize):

        ff_obstacle.append (1- ((obstacles[i]-min(obstacles))/(max(obstacles)-min(obstacles))))
        ff_turn.append (1- ((Turns[i]-min(Turns))/(max(Turns)-min(Turns))))
        ff_path.append(1- ((no_of_steps[i]-min(no_of_steps))/(max(no_of_steps)-min(no_of_steps))))
        final_fitness.append((100*w_obs*ff_obstacle[i]) * (((w_path * ff_path[i]) + (w_turn * ff_turn[i])) / (w_path + w_turn)))
     
def parent():
    global population,final_fitness
   
    indices = list(range(popsize))
    indices.sort(key=lambda i: final_fitness[i], reverse=True)
    population = [population[i] for i in indices]
    final_fitness = [final_fitness[i] for i in indices]

    for i in range(popsize):
        print(f'{population[i]}\t {final_fitness[i]}')           

def solution():
       
    for i in range(popsize):
        if final_fitness[i]>=0 and obstacles[i]==0:
            sol=path[i]
            for j in range(len(sol)-1):
                dic.update({sol[j+1]:sol[j]})
            return 1
    return 0            
       
popsize = 400
row,column=10,10
dic={}
population,path,obstacles,no_of_steps,Turns=[],[],[],[],[]
ff_obstacle,ff_turn,ff_path,final_fitness=[],[],[],[]

from pyamaze import maze,agent
from random import randint
from copy import deepcopy 
m=maze(row,column) 
m.CreateMaze(loopPercent=70) 
a=agent(m,filled=True,footprints=True,shape='arrow') 
map=m.maze_map

iteration=1
flag=0
random_population()

while True:
    fitness_function()
    flag=solution()
    if flag:
        print(f'solution is found in iteration {iteration}')
        m.tracePath({a: dic})
        m.run()
        break
    parent()
    crossover()
    mutation()
    iteration+=1

    path,obstacles,no_of_steps,Turns=[],[],[],[]
    ff_obstacle,ff_turn,ff_path,final_fitness=[],[],[],[]
