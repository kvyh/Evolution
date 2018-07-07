import string_evolution
import numpy as np
import matplotlib.pyplot as plt

# TODO: generate systems that make use of different evolution styles
# TODO: record results and present graphical representations

#string_len = 15
#system_size = 100
#child_style = 'swap_two'

def one_child_one_parent(string_len, system_size, child_style='swap_two'):
    # TODO: test
    system = string_evolution.create_new_system_random_goal(string_len, system_size)
    system.evo_style = system.one_child_one_parent
    if child_style == 'swap_two':  # set the child_style
        for obj in system.evo_objects:
            obj.child_style = obj.swap_two_char_child
    while max(system.assess_fitness()) < string_len:
        system.iterate_generation()
    print(system.generation, max(system.assess_fitness()), system.evo_objects[0].string, system.evo_objects[0].goal)
    record_evo_string_system(system)
    return system


def record_evo_string_system(system):
    # TODO: create header line containing: system evo_style, object child_style, string length, system size
    # TODO: record 'generation, string, fitness' for each object in each generation
    # TODO: test and make sure it outputs strings correctly
    # TODO: prevent over-write
    generations = [[(gen, obj.string, obj.fitness) for obj in objs] for gen, objs in system.generations.items()]
    history = []
    for idx in range(len(generations)):
        history += generations[idx]
    # TODO: make the array not have limited string length
    all_generations = np.array(history, dtype=[('generation', 'i4'), ('string', 'U25'), ('fitness', 'f4')])
    evo_style = str(system.evo_style).split('.')[1].split(' ')[0]
    child_style = str(system.evo_objects[0].child_style).split('.')[1].split(' ')[0]
    np.savetxt('C:\\Users\\Karl\\Documents\\Personal_serious\\Evolution\\evolution_results\\' + 'string_evo' +
               evo_style + '_' + child_style, all_generations, fmt='%s',
               delimiter=',', 
               header='generation, string, fitness',
               comments='# system evo_style: ' + evo_style + 
                        '; object type: string_evolution.EvolvingString' +
                        '; child_style: ' + child_style +
                        '; string length: ' + str(len(system.evo_objects[0].goal)) +
                        '; system size: ' + str(len(system.evo_objects)) + '\n')


def plot_progress(system):
    # TODO: plot the lowest 5, quartiles, and top 5 of each generation
    gen_scores = []
    for gen, objs in system.generations.items():
        scores = [obj.fitness for obj in objs]
        gen_scores.append(scores)
    score_array = np.array(gen_scores)
    plt.plot(system.generations.keys(), score_array.T[-1], )
    plt.plot(system.generations.keys(), score_array.T[-2])
    plt.plot(system.generations.keys(), score_array.T[-3])
    plt.plot(system.generations.keys(), score_array.T[-4])
    plt.plot(system.generations.keys(), score_array.T[-5])
    plt.plot(system.generations.keys(), score_array.T[-1*len(system.evo_objects)//4])
    plt.plot(system.generations.keys(), score_array.T[len(system.evo_objects)//2])
    plt.plot(system.generations.keys(), score_array.T[len(system.evo_objects)//4])
    plt.plot(system.generations.keys(), score_array.T[4])
    plt.plot(system.generations.keys(), score_array.T[3])
    plt.plot(system.generations.keys(), score_array.T[2])
    plt.plot(system.generations.keys(), score_array.T[1])
    plt.plot(system.generations.keys(), score_array.T[0])
    plt.show()
