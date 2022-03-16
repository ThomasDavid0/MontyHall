from random import randrange
from typing import List


class Box:
    def __init__(self, prize: bool, isopen: bool = False, chosen: bool = False):
        self.prize = prize
        self.chosen = chosen
        self.isopen = isopen

    def open(self):
        """return a new box, identical to self but with the door open

        Returns:
            Box: a copy of self with the door open
        """
        return Box(self.prize, True)
    
    def choose(self):
        """return a new box, identical to self but with chosen

        Returns:
            Box: a copy of self with the chosen flag==True
        """
        return Box(self.prize, False, True)

    def leave_alone(self):
        """return a copy of self

        Returns:
            Box: a new box identical to self
        """
        return Box(self.prize, self.isopen, self.chosen)

class Game:
    def __init__(self, boxes: List[Box]):
        assert len(boxes) == 3
        self.boxes = boxes
    
    def prize_box_id(self):
        """find the id of the box with the prize in it"""
        return [box.prize for box in self.boxes].index(True)

    def n_open_doors(self):
        """count the number of boxes with doors open"""
        return sum([box.isopen for box in self.boxes])

    def chosen_box_id(self):
        """get the id of the box that has been chosen, error if no box chosen"""
        return [box.chosen for box in self.boxes].index(True)

    def state(self):
        """return a string indicating the state of the game. 
            new = a fresh game, user hasnt chosen yet
            chosen = user has made a choice and one door is open
            
            this can be determined by counting the number of open doors.
        """
        return ["new", "chosen"][self.n_open_doors()]

    @staticmethod
    def setup(loc: int):
        """Initial game setup with the specified box full and all doors closed

        Args:
            loc (int): id of the box containing the prize

        Returns:
            Game: a new game ready to play
        """
        assert loc in [0,1,2]
        return Game([Box(loc==i) for i in range(3)])

    @staticmethod
    def random():
        """Initial game setup with a random full box

        Returns:
            Game: a new game ready to play
        """
        return Game.setup(randrange(3)) 


    def choose(self, loc: int):
        """A box is chosen. and the state of the game is updated

        Args:
            loc (int): the id of the chosen box

        Returns:
            Game: a copy of self with new boxes open or chosen as necessary
        """
        assert self.state() == "new"
        new_boxes = []
        one_opened = False
        for i, box in enumerate(self.boxes):
            if i==loc:
                new_boxes.append(box.choose())
            else:
                if box.prize or one_opened:
                    new_boxes.append(box.leave_alone())
                else:
                    new_boxes.append(box.open())
                    one_opened = True
                    
        return Game(new_boxes)
    
    def switch(self):
        assert self.state() == "chosen"
        return not self.prize_box_id() == self.chosen_box_id()

    def stay(self):
        assert self.state() == "chosen"
        return self.prize_box_id() == self.chosen_box_id()



def many_games(count, option):
    """run the game count times with the selected decision, return the number of wins"""
    print(f"{option}ing {count} times")

    res = []
    for _ in range(count):
        res.append(
            getattr(
                Game.random().choose(randrange(3)),option)()
        )
    win_count = sum(res)
    print(f"we have {win_count} winners, {100*win_count/count}%")
    return win_count



if __name__ == "__main__":

    print("how many times do you want to test?")
    count = int(input())

    res_switch = many_games(count, "switch")
    res_stay = many_games(count, "stay")

    print(f"to {'switch' if res_switch > res_stay else 'stay'} is the best option")

