"""This is the example2 module"""
class KeithMood :
    """A class that keeps track of Keith's moods
    Attributes
        name: description of mood
        level: how big the mood is
        solution: the ideal solution

    """

    def __init__ (self, name: str, level: int, solution: str = "chocolate"):
        self.name = name
        self.level = level
        self.solution = solution

    def improve_mood(self, potential_solution: str) -> int:
        """Seriously doc strings and declaring your variable types will make your life so much easier."""
        # print (f"Adding {solution}") You can't print here any more as it's not a script you are running.
        # your prints need to go in the calling script, or be proper logging statements in the flask ap
        if potential_solution == self.solution: # use identation
            self.level = self.level + 1 # keep iteration simple.
        else:
            # Nah Fam.  No Joy
            pass
        # print (f"{self.name} is now at level {self.level}")
        return self.level

    def reduce_mood(self) -> int:
        """"Doc string goes here"""
        print ("Now writing lesson plans...")
        self.level = self.level - 1
        return self.level

# Try and make sure you declare your input types and you returns
def square(number:float) -> float:
    """This is a function outside the scope of the object"""
    return number ** 2
