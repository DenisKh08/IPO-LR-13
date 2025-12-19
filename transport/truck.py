from transport.vehicle import vehicle

class truck(vehicle):
    color = ""

    def __init__(self):
        truck_color = input("введите цвет грузовика: ")
        self.color = truck_color
        super().__init__()
        