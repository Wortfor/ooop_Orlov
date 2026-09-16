class SingletonFive:
    __count = 0
    __last_instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__count < 5:
            cls.__count += 1
            cls.__last_instance = super().__new__(cls)
        return cls.__last_instance

    def __init__(self, name):
        self.name = name


objs = [SingletonFive(str(n)) for n in range(10)]


for i, obj in enumerate(objs):
    print(i, id(obj), obj.name)