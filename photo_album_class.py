from typing import List

class Photo_album:
    
    def __init__(self, mylist: List) -> None:
        self.i_list = mylist
    
    def next(self) -> List:
        self.i_list = self.i_list[1:] + self.i_list[:1]
        return self.i_list[0]
    
    def prev(self) -> List:
        self.i_list = self.i_list[-1:] + self.i_list[:-1]
        return self.i_list[0]
    
    def __str__(self):
        return self.i_list[0]