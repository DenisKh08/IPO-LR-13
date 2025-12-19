import random

class vehicle():
    vehicle_id = random.randint(1000, 9999)
    capacity = -1
    current_load = 0
    clients_list = []

    def load_cargo(self,client):
        if self.capacity >= client.cargo_weight:
            self.current_load += client.cargo_weight
            self.clients_list.append(client)

    def __str__(self):
        return f'''
        ID транспорта: {self.vehicle_id}
        грузоподъёмность транспорта: {self.capacity}
        текущая загруженность: {self.current_load}'''
 
    def __init__(self):
        vehicle.vehicle_id = self.vehicle_id+1
        self.vehicle_id = vehicle.vehicle_id
        self.capacity = float(input("грузоподъемность вашего транспорта в тоннах: "))
