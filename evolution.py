#import numpy as np
import random


class EvolutionSystem:
    # Overarching class that contains the system of evolving objects
    def __init__(self, objects):
        """
        input is a list of the evolving objects that the system contains

        :param objects: list of  `EvolvingObject`s
        """
        self.evo_objects = objects
        self.evo_style = self.one_child_one_parent
        self.generation = 0
        self.generations = {self.generation: self.evo_objects}  # record the first generation
        self.sorted = False

    def list_by_fitness(self):
        """
        Sort the objects by their fitness parameter

        :return: list of `EvolvingObject`s sorted by fitness (highest first)
        """
        if not self.sorted:  # if it's already sorted, do nothing
            self.assess_fitness()
            self.evo_objects = sorted(self.evo_objects, key=lambda x: x.fitness, reverse=True)
            self.sorted = True
        # TODO: make customizable output
        return self.evo_objects

    def assess_fitness(self):
        """
        calls the assess_fitness function of the `EvolvingObject`s

        :return: list of the fitness values
        """
        fit = []
        for obj in self.evo_objects:
            fit.append(obj.determine_fitness())
        return fit

    def iterate_generation(self):
        """
        Takes the current generation of objects and creates the next generation

        :return:
        """
        self.list_by_fitness()
        new_generation = self.evo_style()  # TODO: make this work with parameters?
        self.evo_objects = new_generation
        self.sorted = False  # new generation isn't sorted yet
        self.list_by_fitness()  # sort before adding to self.generations
        self.generations[self.generation] = self.evo_objects  # store the new generation
        self.generation += 1

    def evolution_style(self, keep_parent, num_parents, parents):
        # options are: keep the parent, how many parents, distribution of children per parent, distribution of parents
        # parents maintained + children = total_evos
        raise NotImplementedError

    def one_child_one_parent(self):
        living = self.evo_objects[0:int(len(self.evo_objects) / 2)]  # take first half of objects
        children = []
        for obj in living:
            # add children of each parent evo_object
            children += obj.create_child(1)
        new_generation = living + children
        return new_generation

    def three_child(self):
        parents = self.evo_objects[0:int(len(self.evo_objects)/3)]  # take first third of objects, rounds down
        children = []
        remainder = divmod(len(self.evo_objects), 3)[1]
        for obj in parents[:remainder]:
            children += obj.create_child(4)
        for obj in parents[remainder:]:
            children += obj.create_child(3)
        new_generation = children
        return new_generation

    def weighted_random_no_dup(self, number):
        """
        generates list of parents with length 'number' that is weighted by fitness and contains no duplicates

        :param number: length of list of parents
        :return: list of parents
        """
        weights = [x.fitness + .01 for x in self.evo_objects]
        parents = []
        parent_set = ()
        while len(set(parent_set)) < number:
            choice = random.choices(self.evo_objects, weights)
            parents.append(choice)
            parent_set = set(parents)  # prevent duplicates
        parents = list(parent_set)
        return parents

    def weighted_random_dups(self):
        """
        generates a list of parents weighted by fitness allowing duplicates
        one parent for each member of a new generation of children

        :return: list of parents
        """
        weights = [x.fitness for x in self.evo_objects]
        parents = []
        while len(parents) < len(self.evo_objects):
            choice = random.choices(self.evo_objects, weights)
            parents.append(choice)
        return parents


class EvolvingObject:
    # base class to be used in the `EvolutionSystem`
    def __init__(self):
        """
        should be overwritten in sub-classes
        """
        self.fitness = 0

    def determine_fitness(self):
        """
        function used to determine the fitness of the object
        *Must be overridden by a subclass*

        :return: fitness value
        """
        raise AssertionError("determine_fitness must be overridden by the subclass")

    def create_child(self, count):
        """
        function governing the creation of child objects

        :param count: number of children to create
        :return: list of child `EvolvingObject`s
        """
        raise NotImplementedError

