import evolution
import random
import string
import copy


class EvolvingString(evolution.EvolvingObject):
    def __init__(self, string, goal_string, lineage=[]):
        self.fitness = 0
        self.string = string
        self.goal = goal_string
        self.lineage = lineage + [self.string]
        self.child_style = self.swap_two_char_child

    def determine_fitness(self):
        self.fitness = 0
        for i, char in enumerate(self.string):
            if i < len(self.goal):  # prevent index out of range
                if char == self.goal[i]:
                    self.fitness += 1
        return self.fitness

    def create_child(self, count):
        """
        creates children equal to 'count' with the function described by 'self.child_style'

        :param count: int number of children
        :return: list of children
        """
        children = []
        for x in range(count):
            child = self.child_style()
            children.append(child)
        return children

    def swap_two_char_child(self):
        """
        swaps two of the characters in the string for random characters

        :return: child `EvolvingString`
        """
        """child = copy.copy(self)
        index = random.randint(0, len(child.goal))
        child.string = child.string[0:index] + create_randstring(1) + child.string[index + 1:]
        index = random.randint(0, len(child.goal))
        child.string = child.string[0:index] + create_randstring(1) + child.string[index + 1:]
        child.lineage.append(child.string)
        return child """
        index = random.randint(0, len(self.goal)-1)
        new_string = self.string[0:index] + create_randstring(1) + self.string[index + 1:]
        index = random.randint(0, len(self.goal)-1)
        new_string = new_string[0:index] + create_randstring(1) + new_string[index + 1:]
        if self.fitness == 0:
            new_string = create_randstring(len(self.goal))
        child = EvolvingString(new_string, self.goal, self.lineage)
        return child


def create_randstring(length):
    return ''.join(random.choices(string.ascii_letters + "_.!'[]{}() ", k=length))


def create_new_system_random_goal(length, set_size):
    """

    :param length: (int) length of goal string
    :param set_size: (int) size of each generation of the system
    :return: `EvolutionSystem`
    """
    initial_set = []
    goal = create_randstring(length)
    for x in range(set_size):
        initial_set.append(EvolvingString(create_randstring(length), goal))
    system = evolution.EvolutionSystem(initial_set)
    return system
