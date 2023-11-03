import random
from collections import namedtuple
import numpy as np
from scipy.special import softmax

facilitators = ["Lock", "Glen", "Banks", "Richards", "Shaw", "Singer", "Uther", "Tyler", "Numen", "Zeldin"]
activities = {
       "SLA100A": {"enrollment": 50, "preferred_facilitators": ["Glen", "Lock", "Banks", "Zeldin"], "other_facilitators": ["Numen", "Richards"]},

    "SLA100B": {"enrollment": 50, "preferred_facilitators": ["Glen", "Lock", "Banks", "Zeldin"], "other_facilitators": ["Numen", "Richards"]},

    "SLA191A": {"enrollment": 50, "preferred_facilitators": ["Glen", "Lock", "Banks", "Zeldin"], "other_facilitators": ["Numen", "Richards"]},

    "SLA191B": {"enrollment": 50, "preferred_facilitators": ["Glen", "Lock", "Banks", "Zeldin"], "other_facilitators": ["Numen", "Richards"]},

    "SLA201":  {"enrollment": 50, "preferred_facilitators": ["Glen", "Banks", "Zeldin", "Shaw"], "other_facilitators": ["Numen", "Richards", "Singer"]},

    "SLA291":  {"enrollment": 50, "preferred_facilitators": ["Lock", "Banks", "Zeldin", "Singer"], "other_facilitators": ["Numen", "Richards", "Shaw", "Tyler"]},

    "SLA303":  {"enrollment": 60, "preferred_facilitators": ["Glen", "Zeldin", "Banks"], "other_facilitators": ["Numen", "Singer", "Shaw"]},

    "SLA304":  {"enrollment": 25, "preferred_facilitators": ["Glen", "Banks", "Tyler"], "other_facilitators": ["Numen", "Singer", "Shaw", "Richards", "Uther", "Zeldin"]},

    "SLA394":  {"enrollment": 20, "preferred_facilitators": ["Tyler", "Singer"], "other_facilitators": ["Richards", "Zeldin"]},

    "SLA449":  {"enrollment": 60, "preferred_facilitators": ["Tyler", "Singer", "Shaw"], "other_facilitators": ["Zeldin", "Uther"]},

    "SLA451":  {"enrollment": 100, "preferred_facilitators": ["Tyler", "Singer", "Shaw"], "other_facilitators": ["Zeldin", "Uther", "Richards", "Banks"]},

}
list_of_activities_ids = ["SLA100A", "SLA100B", "SLA191A", "SLA191B", "SLA201", "SLA291", "SLA303", "SLA304","SLA394","SLA449" , "SLA451" ]

rooms = ["Slater 003","Roman 216","Loft 206","Roman 201","Loft 310","Beach 201","Beach 301","Logos 325","Frank 119"]


rooms_size = {

    "Slater 003": 45,

    "Roman 216": 30,

    "Loft 206": 75,

    "Roman 201": 50,

    "Loft 310": 108,

    "Beach 201": 60,

    "Beach 301": 75,

    "Logos 325": 450,

    "Frank 119": 60,

}


times = ["10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM"]

activity = namedtuple('activity', ['name','Room', 'Time', 'Facilitator'])

shecdule=[] #list of activity namedtuple
def Activity_specific_fitness(act,sections):

    
    specific_fitness=0.0
    
    if(act.name[0:6]=="SLA100"):
        if(abs(int(sections["SLA100A"][1].split(" ")[0])-int(sections["SLA100B"][1].split(" ")[0]))>4):
            specific_fitness=specific_fitness+0.5
        elif(int(sections["SLA100A"][1].split(" ")[0])==int(sections["SLA100B"][1].split(" ")[0])):
            specific_fitness=specific_fitness-0.5
        if(int(sections["SLA191A"][1].split(" ")[0])+1==int(act.Time.split(" ")[0]) or int(sections["SLA191B"][1].split(" ")[0])+1==int(act.Time.split(" ")[0]) or int(sections["SLA191A"][1].split(" ")[0])-1==int(act.Time.split(" ")[0]) or int(sections["SLA191B"][1].split(" ")[0])-1==int(act.Time.split(" ")[0])):
            specific_fitness=specific_fitness+0.5
        elif(int(sections["SLA191A"][1].split(" ")[0])+2==int(act.Time.split(" ")[0]) or int(sections["SLA191B"][1].split(" ")[0])+2==int(act.Time.split(" ")[0]) or int(sections["SLA191A"][1].split(" ")[0])-2==int(act.Time.split(" ")[0]) or int(sections["SLA191B"][1].split(" ")[0])-2==int(act.Time.split(" ")[0])):
                specific_fitness=specific_fitness+0.25
                
    if(act.name[0:6]=="SLA191"):
        if(abs(int(sections["SLA191A"][1].split(" ")[0])-int(sections["SLA191B"][1].split(" ")[0]))>4):
            specific_fitness=specific_fitness+0.5
        elif(int(sections["SLA191A"][1].split(" ")[0])==int(sections["SLA191B"][1].split(" ")[0])):
            specific_fitness=specific_fitness-0.5
        if(int(sections["SLA100A"][1].split(" ")[0])+1==int(act.Time.split(" ")[0]) or int(sections["SLA100B"][1].split(" ")[0])+1==int(act.Time.split(" ")[0]) or int(sections["SLA100A"][1].split(" ")[0])-1==int(act.Time.split(" ")[0]) or int(sections["SLA100B"][1].split(" ")[0])-1==int(act.Time.split(" ")[0])):
            specific_fitness=specific_fitness+0.5
        elif(int(sections["SLA100A"][1].split(" ")[0])+1==int(act.Time.split(" ")[0]) or int(sections["SLA100B"][1].split(" ")[0])+1==int(act.Time.split(" ")[0]) or int(sections["SLA100A"][1].split(" ")[0])-1==int(act.Time.split(" ")[0]) or int(sections["SLA100B"][1].split(" ")[0])-1==int(act.Time.split(" ")[0])):
                specific_fitness=specific_fitness+0.25

    return specific_fitness

        
        
    
            
        
        
def fitness_funcation_of_a_activity(activit,schedule): #activit is named tuple activity
    fitness=0.0
    fac_oversee_on_act=0
    faculty_scheduled_at_sametime=False
    x=0
    dic_sections={}
    #print(activit.name)
    other_facilitator= activities[activit.name]["other_facilitators"]
    preferred_facilitator= activities[activit.name]["preferred_facilitators"]
    if rooms_size[activit.Room] < activities[activit.name]["enrollment"]:
        fitness=fitness-0.5
    
    elif rooms_size[activit.Room] > 3*activities[activit.name]["enrollment"]:
        fitness=fitness-0.2
    elif rooms_size[activit.Room] > 6*activities[activit.name]["enrollment"]:
        fitness=fitness-0.4

    else:
         fitness=fitness+0.3
    if activit.Facilitator in preferred_facilitator:
        fitness=fitness+0.5
    elif activit.Facilitator in other_facilitator:
        fitness=fitness+0.2
    else:
        #print(fitness)
        fitness=fitness-0.1
        

    for i in schedule:
        if i.Room==activit.Room and i.Time==activit.Time and i.name!=activit.name: #cumalitive if 3 activities in same time slot -1.0

            fitness=fitness-0.5
        if i.Facilitator==activit.Facilitator:
            fac_oversee_on_act=fac_oversee_on_act+1
        if(len(i.name)==7):
            dic_sections[i.name]=[i.Room,i.Time]
    for i in schedule:
        if i.Facilitator==activit.Facilitator and i.Time==activit.Time and i.name!=activit.name:
            fitness=fitness-0.2
            break
    else:
        fitness=fitness+0.2           
    if fac_oversee_on_act > 4:
        fitness=fitness-0.5
    elif fac_oversee_on_act < 3 and activit.Facilitator!="Tyler":
        fitness=fitness-0.4
    if(len(activit.name)==7):
        x=Activity_specific_fitness(activit,dic_sections)
    return round(fitness+x,2)

def fitness_funcation_of_a_schedule(s):
    fitness_of_schedule=0
    for act in s:
        fitness_of_act=fitness_funcation_of_a_activity(act,s)
        fitness_of_schedule=fitness_of_schedule + fitness_of_act
    return fitness_of_schedule

def random_activity(id): #create random gene
    global rooms
    global times
    global facilitators
    room=random.choice(rooms)
    time=random.choice(times) 
    facilitator=random.choice(facilitators) 
    return activity(id,room,time,facilitator)

def initial_random_population(n): #create random population of schedule return list of list containing actvities ie actvities->schedule->population
    rand_pop=[] 
    for i in range(n):
        rand_schedule=[]
        for a in list_of_activities_ids:
            rand_act=random_activity(a)
            rand_schedule.append(rand_act)
        rand_pop.append(rand_schedule)
    return rand_pop

def crossover(parent1,parent2):
    a1=parent1
    a2=parent2
    crossover_point = random.randint(1, len(a1) - 1)
    offspring1 = a1[:crossover_point] + a2[crossover_point:]
    offspring2 = a2[:crossover_point] + a1[crossover_point:]
    return offspring1, offspring2 

def mutation(offspring, mutation_rate):
    for i in range(len(offspring)):
        if random.random() < mutation_rate:
            offspring[i] = random_activity(offspring[i].name)
    return offspring
  
def selection(population):
    global fitness_scores
    fitness_scores = [fitness_funcation_of_a_schedule(a) for a in population]
    probabilities = softmax(fitness_scores)
    return random.choices(population, probabilities, k=2)


def genetic_algorithim():
    n=500
    mutation_Rate=0.005
    population=initial_random_population(n)
    count=0
    for i in range(100):
        new_population=[]
        for i in range(125):
            count=count+1
            print(count)
            p1,p2=selection(population)
            o1,o2=crossover(p1,p2)
            m1=mutation(o1,mutation_Rate)
            m2=mutation(o2,mutation_Rate)
            new_population.append(p1)
            new_population.append(p2)            
            new_population.append(m1)
            new_population.append(m2)
        population=new_population
    max_fit=max(fitness_scores)
    print(max_fit)
    index_of_best_shedule=fitness_scores.index(max_fit)
    return population[index_of_best_shedule]


if __name__ == "__main__":
    best_schedule=genetic_algorithim()
    file1 = open("schedule.txt", "w")
    for i in best_schedule:
        print(i)
        file1.write("\n")
        file1.write(str(i))
    file1.close()



    
        
    
    


