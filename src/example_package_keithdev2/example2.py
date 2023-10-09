"""This is the example2 module"""
class KeithMod :
    """A class that keeps track of Keith's moods
    Attributes
        name: description of mood
        level: how big the mood is
        solution: the ideal solution

    """

    def __init__ (self, name, level, solution="chocolate"):
        self.name = name
        self.level = level
        self.solution = solution

    def improve_mood(self, solution):
        print (f"Adding {solution}")
        self.level -=1
        if solution == self.solution: self.level-=1
        print (f"{self.name} is now at level {self.level}")

    def reduce_mood(self):
        print ("Now writing lesson plans...")
        self.level+=1
        print (f"{self.name} is now at level {self.level}")


def square(number) :
    return number ** 2



