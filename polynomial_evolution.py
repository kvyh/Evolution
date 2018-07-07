# -*- coding: utf-8 -*-
"""
Evolving object parameters

Created on Sun Jun 10 18:49:38 2018

@author: Karl
"""
import numpy as np
from scipy.misc import derivative
import string
import random


class EvolutionSystem:
    # the system containing the population that will be evolved
    def __init__(self, evolution_bases):
        for base in evolution_bases:
            if not isinstance(base, EvolutionBase):
                raise TypeError
        self.evo_bases = evolution_bases
        self.generation = 0
        self.progress = {}

    def list_by_fitness(self):
        self.evo_bases = sorted(self.evo_bases, key=lambda x: x.fitness, reverse=True)
        # TODO: make customizable output
        print("top 5: " + str([e.string for e in self.evo_bases[:5]]))

    def assess_fitness(self):
        fit = []
        for base in self.evo_bases:
            fit.append(base.determine_fitness())
        print(max(fit))

    def iterate_generation(self):
        # TODO: make some of this custom in the EvolutionBase, just works for EvolvingString
        self.assess_fitness()
        self.list_by_fitness()
        living = self.evo_bases[0:int(len(self.evo_bases)/2)]
        children = []
        for base in living:
            # change 2 characters in the string to produce a child
            index = random.randint(0, 18)
            new_string = base.string[0:index] + create_randstring(1) + base.string[index+1:]
            index = random.randint(0, 18)
            new_string = new_string[0:index] + create_randstring(1) + new_string[index+1:]
            if base.fitness == 0:
                new_string = create_randstring(19)
            child = EvolvingString({'string': new_string, 'parent': base.lineage})
            children.append(child)
        self.evo_bases = living + children
        self.generation +=1
        if np.mod(self.generation, 10) == 0:
            self.progress[self.generation] = [base.string for base in self.evo_bases[:5]]


class EvolutionBase:
    # base class for objects that will be evolved by an `EvolutionSystem`
    def __init__(self, starting_parameters_dict):
        self.fitness = 0
        self.generate_parameters(starting_parameters_dict)

    def generate_parameters(self, parameters):
        # set the parameters, will likely be overridden by subclasses
        self.parameters = parameters

    def determine_fitness(self):
        # for the function calculating fitness
        pass
#####################################################################################


class EvolvingStartPointX(EvolutionBase):
    # Evolving class for system which has
    def generate_parameters(self, parameters):
        self.starting_x = parameters['x']
        self.function_to_solve = parameters['function']

    def determine_fitness(self):
        self.fitness = 0
        derivative(self.function_to_solve, 1.0, dx=1e-6)
        return self.fitness


def initial_function(x):
    return


#####################################################################################
class EvolvingString(EvolutionBase):
    # to produce "Happy Father's Day!"
    def generate_parameters(self, parameters):
        # TODO: add checks and assertions?
        self.string = parameters['string'] # should be 19 characters long
        self.target = "Happy Father's Day!"
        self.lineage = parameters['parent']
        self.lineage.append(self.string)

    def determine_fitness(self):
        self.fitness = 0
        for i, l in enumerate(self.string):
            # print(self.string, len(self.string))
            if l == self.target[i]:
                self.fitness += 1
        return self.fitness


def create_evolving_string(string_length, string_number):
    bases = []
    for x in range(0, string_number):
        param = {'string': create_randstring(string_length), 'parent': []}
        bases.append(EvolvingString(param))
    system = EvolutionSystem(bases)
    return system

def create_randstring(length):
    return ''.join(random.choices(string.ascii_letters + ".!'[]{}() ", k=length))

system = create_evolving_string(19, 100)
system.iterate_generation()