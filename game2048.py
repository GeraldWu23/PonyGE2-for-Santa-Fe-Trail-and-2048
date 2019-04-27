from fitness.base_ff_classes.base_ff import base_ff
from utilities.stats import trackers
import random
import time

class game2048(base_ff): # must have the same name of the file       
    def __init__(self):
        # Initialise base fitness function class.
        super().__init__()
        

    def evaluate(self, ind, **kwargs):
        p = ind.phenotype
        fitness = 0
        fitness_scale = 10  # to enlarge the difference between fitnesses
               
        for trial in range(int(50/fitness_scale)):  # only one example so no need to consider overfitting
            target_biggest = 256  # a total of 90 foods 

            d = {}

            try:
                t0 = time.time()

                """ RUNNING THE TRAINING """
                try:
                    exec(p,d)  # the algorithm is evaluated
                    t1 = time.time()            
                    result = d['return_val']
                    
                    #print('programme successful')
                except:
                    
                    t1 = time.time()
                    result = 2                  
                    print('the programme is not working')                


                """ LENGTH OF PROGRAMME CONTROL 
                try:
                    fitness += len(p)  # avoid bloat and unnecessary if statements
                except:
                    print('length control problem')"""


                """ FITNESS CALCULATION """
                try:
                    v = abs(target_biggest - result) # the scale might need justification
                    if v <= 254:                                                       
                        fitness += v
                    else:
                        fitness = self.default_fitness
                        print('result too bad')
                        break
                except:
                    print('fitness calculation problem')


                """ RUNNING TIME CONTROL 
                try:
                    if t1 - t0 > 5:  # could be in a dead loop
                        fitness = self.default_fitness
                        print('run time too long')
                        break
                    else:
                        fitness += (t1 - t0) * 100

                except:
                    print('time problem')"""


            except:
                fitness = self.default_fitness  # NA
                print('the rest is not working')
                break

        print('\n\n' + str(256 - fitness/(50/fitness_scale)))
        if fitness == 0:
        	print('!!!!!!!! CHECK GENERATIONS !!!!!!!!!')
        print('\n\n')
        return fitness * fitness_scale


def generate_list():
    return [random.randint(0, round(random.random() * 90 + 10, 0)) for i in range(9)]


        



















