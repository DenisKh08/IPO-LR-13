from transport.vehicle import vehicle

class ship(vehicle):
    name = ""
    
    def __init__(self):
        ship_name = input("имя судна: ")
        self.name = ship_name 
        super().__init__()

    def __str__(self):
        return f'''
        ID судна: {self.vehicle_id}
        название судна: {self.name}
        грузоподъёмность судна: {self.capacity}
        текущая загруженность: {self.current_load}'''