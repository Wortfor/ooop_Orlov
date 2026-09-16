class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def clone(self):
        return Point(self.x, self.y)


pt = Point(3, 5)
pt_clone = pt.clone()

print(pt.x, pt.y)          
print(pt_clone.x, pt_clone.y)  
print(pt is pt_clone)      