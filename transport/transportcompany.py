import json
import os

class TransportCompany():
    # Статические методы для работы с файлом
    @staticmethod
    def load_data():
        try:
            if os.path.exists("data1.json"):
                with open("data1.json", "r", encoding='utf-8') as file:
                    return json.load(file)
        except Exception as e:
            print(f"Ошибка при загрузке данных: {e}")
        return {"vehicles": [], "clients": []}
    
    @staticmethod
    def save_data(data):
        try: 
            with open('data1.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении данных: {e}")
            return False

    def __init__(self, name=""):
        self.name = name
        self.vehicles = []
        self.clients = []

    def add_vehicle(self, vehicle): 
        self.vehicles.append(vehicle)
        
        data = self.load_data()
        
        vehicle_data = {
            "ID транспортного средства": vehicle.vehicle_id,
            "грузоподъёмность транспорта": vehicle.capacity,
            "текущая загруженность": vehicle.current_load,
        }
        
        # Добавляем клиентов, если они есть
        if hasattr(vehicle, 'clients'):
            vehicle_data["Клиенты"] = [
                {
                    "имя клиента": client.name, 
                    "вес груза клиента": client.cargo_weight, 
                    "VIP": client.is_vip
                } 
                for client in vehicle.clients
            ]
        else:
            vehicle_data["Клиенты"] = []
        
        if hasattr(vehicle, '__class__'):
            class_name = vehicle.__class__.__name__
            vehicle_data["Тип"] = class_name
            
            if class_name == "ship":
                vehicle_data["Название"] = getattr(vehicle, 'name', 'Неизвестно')
            elif class_name == "truck":
                vehicle_data["Цвет"] = getattr(vehicle, 'color', 'Неизвестно')
        
        if "vehicles" not in data:
            data["vehicles"] = []
        
        data["vehicles"].append(vehicle_data)
        
        self.save_data(data)
        return True

    def add_client(self, client): 
        self.clients.append(client)
        
        data = self.load_data()

        if "clients" not in data:
            data["clients"] = []
        
        data["clients"].append({
            "имя клиента": client.name,
            "вес груза клиента": client.cargo_weight,
            "VIP": client.is_vip
        })
        
        self.save_data(data)
        return True

    def cargo_load(self, vehicle, clients_list):
        remaining_clients = []

        for client in clients_list:
            if client.cargo_weight + vehicle.current_load <= vehicle.capacity:
                vehicle.current_load += client.cargo_weight
                
                if not hasattr(vehicle, 'loaded_clients'):
                    vehicle.loaded_clients = []
                vehicle.loaded_clients.append(client)
            else:
                remaining_clients.append(client)

        return vehicle, remaining_clients

    def optimize_cargo_distribution(self):
        sorted_by_weight = sorted(self.clients, key = lambda c: c.cargo_weight, reverse = True)
        sorted_clients = sorted(sorted_by_weight, key = lambda c: not c.is_vip)
        
        sorted_vehicles = sorted(self.vehicles, key = lambda v: v.capacity)
       
        for vehicle in sorted_vehicles:
            vehicle.current_load = 0

            if hasattr(vehicle, 'loaded_clients'):
                vehicle.loaded_clients = []
       
        clients_to_load = sorted_clients.copy()
        used_vehicles = []  
       
        for vehicle in sorted_vehicles:
            if not clients_to_load:  
                break

            loaded_vehicle, remaining = self.cargo_load(vehicle, clients_to_load)

            if loaded_vehicle.current_load > 0:
                used_vehicles.append(loaded_vehicle)

            clients_to_load = remaining
        
        data = self.load_data()
        
        for i, vehicle in enumerate(used_vehicles):
            for v_data in data.get("vehicles", []):
                if v_data.get("ID транспортного средства") == vehicle.vehicle_id:
                    v_data["текущая загруженность"] = vehicle.current_load

        self.save_data(data)
        
        print("Результаты:")
        print(f"Всего клиентов: {len(self.clients)}")
        print(f"Загружено клиентов: {len(self.clients) - len(clients_to_load)}")
        print(f"Осталось незагруженных: {len(clients_to_load)}")
        print(f"Использовано транспорта: {len(used_vehicles)} из {len(self.vehicles)}")
        print("Информация по транспорту:")

        for i, vehicle in enumerate(used_vehicles, 1):
            print(f"  Транспорт {i}:")
            print(f"    Тип: {type(vehicle).__name__}")
            print(f"    Вместимость: {vehicle.capacity} тонн")
            print(f"    Загружено: {vehicle.current_load} тонн")
            if hasattr(vehicle, 'loaded_clients'):
                print(f"    Клиентов загружено: {len(vehicle.loaded_clients)}")
        
        if clients_to_load:
            print(f"Незагруженные клиенты ({len(clients_to_load)}):")
            for client in clients_to_load:
                print(f"  - {client}")

        return used_vehicles, clients_to_load


