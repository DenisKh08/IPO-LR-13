import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
from transport.vehicle import vehicle
from transport.transportcompany import TransportCompany 
from transport.truck import truck
from transport.ship import ship
from transport.client import client

class Client:
    def __init__(self, name, cargo_weight, is_vip=False):
        self.name = name
        self.cargo_weight = cargo_weight
        self.is_vip = is_vip
        self.id = id(self)

class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, capacity, details):
        self.vehicle_id = vehicle_id
        self.type = vehicle_type
        self.capacity = capacity
        self.current_load = 0
        self.clients = []
        self.details = details
    
    @property
    def free_capacity(self):
        return self.capacity - self.current_load

class TransportCompanyGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Транспортная Компания")
        self.root.geometry("1000x600")
        
        self.clients = []
        self.vehicles = []
        
        self.create_menu()
        self.create_interface()
        self.load_data()
        self.update_tables()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Экспорт", command=self.export_data)
        file_menu.add_command(label="Сохранить", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="О программе", command=self.show_about)
        
        menubar.add_cascade(label="Файл", menu=file_menu)
        menubar.add_cascade(label="Справка", menu=help_menu)
        self.root.config(menu=menubar)
    
    def create_interface(self):
        # Панель управления
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)
        
        buttons = [
            ("Клиент", self.add_client),
            ("Транспорт", self.add_vehicle),
            ("Удалить", self.delete_selected),
            ("Загрузить", self.load_cargo),
            ("Распределить", self.optimize),
            ("Экспорт", self.export_data),
        ]
        
        for text, cmd in buttons:
            ttk.Button(toolbar, text=text, command=cmd).pack(side=tk.LEFT, padx=2)
        
        # Таблицы
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Клиенты
        clients_frame = ttk.Frame(notebook)
        notebook.add(clients_frame, text="Клиенты")
        self.create_client_table(clients_frame)
        
        # Транспорт
        vehicles_frame = ttk.Frame(notebook)
        notebook.add(vehicles_frame, text="Транспорт")
        self.create_vehicle_table(vehicles_frame)
        
        # Статус
        self.status = tk.StringVar(value="Готово")
        ttk.Label(self.root, textvariable=self.status, relief=tk.SUNKEN).pack(fill=tk.X, padx=5, pady=5)
    
    def create_client_table(self, parent):
        columns = ("Имя", "Вес (кг)", "VIP")
        self.clients_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.clients_tree.heading(col, text=col)
            self.clients_tree.column(col, width=150, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.clients_tree.yview)
        self.clients_tree.configure(yscrollcommand=scrollbar.set)
        
        self.clients_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.clients_tree.bind("<Double-1>", lambda e: self.edit_client())
    
    def create_vehicle_table(self, parent):
        columns = ("ID", "Тип", "Детали", "Грузоподъемность", "Загружено", "Свободно")
        self.vehicles_tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.vehicles_tree.heading(col, text=col)
            self.vehicles_tree.column(col, width=120, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command=self.vehicles_tree.yview)
        self.vehicles_tree.configure(yscrollcommand=scrollbar.set)
        
        self.vehicles_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.vehicles_tree.bind("<Double-1>", lambda e: self.edit_vehicle())
    
    # Базовые операции
    def add_client(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить клиента")
        dialog.geometry("300x200")
        
        ttk.Label(dialog, text="Имя*:").pack(pady=5)
        name_entry = ttk.Entry(dialog, width=30)
        name_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Вес груза (кг)*:").pack(pady=5)
        weight_entry = ttk.Entry(dialog, width=30)
        weight_entry.pack(pady=5)
        
        vip_var = tk.BooleanVar()
        ttk.Checkbutton(dialog, text="VIP", variable=vip_var).pack(pady=10)
        
        def save():
            name = name_entry.get().strip()
            weight = weight_entry.get().strip()
            
            if not name or len(name) < 2:
                messagebox.showerror("Ошибка", "Имя должно быть минимум 2 символа")
                return
            
            if not re.match(r'^[а-яА-Яa-zA-Z\s]+$', name):
                messagebox.showerror("Ошибка", "Имя должно содержать только буквы")
                return
            
            try:
                weight = float(weight)
                if not 0 < weight <= 10000:
                    messagebox.showerror("Ошибка", "Вес должен быть от 1 до 10000 кг")
                    return
            except:
                messagebox.showerror("Ошибка", "Вес должен быть числом")
                return
            
            self.clients.append(Client(name, weight, vip_var.get()))
            self.save_data()
            self.update_tables()
            dialog.destroy()
            self.status.set(f"Клиент '{name}' добавлен")
        
        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)
        name_entry.focus()
        dialog.bind('<Return>', lambda e: save())
    
    def add_vehicle(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить транспорт")
        dialog.geometry("300x250")
        
        ttk.Label(dialog, text="Тип:").pack(pady=5)
        type_var = tk.StringVar(value="Грузовик")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, values=["Грузовик", "Корабль"], state="readonly")
        type_combo.pack(pady=5)
        
        ttk.Label(dialog, text="ID*:").pack(pady=5)
        id_entry = ttk.Entry(dialog, width=30)
        id_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Детали (цвет/название)*:").pack(pady=5)
        details_entry = ttk.Entry(dialog, width=30)
        details_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Грузоподъемность (кг)*:").pack(pady=5)
        capacity_entry = ttk.Entry(dialog, width=30)
        capacity_entry.pack(pady=5)
        
        def save():
            if not id_entry.get().strip():
                messagebox.showerror("Ошибка", "Введите ID")
                return
            
            if not details_entry.get().strip():
                messagebox.showerror("Ошибка", "Введите детали")
                return
            
            try:
                capacity = float(capacity_entry.get())
                if capacity <= 0:
                    messagebox.showerror("Ошибка", "Грузоподъемность должна быть > 0")
                    return
            except:
                messagebox.showerror("Ошибка", "Грузоподъемность должна быть числом")
                return
            
            vehicle = Vehicle(
                id_entry.get().strip(),
                type_var.get(),
                capacity,
                details_entry.get().strip()
            )
            
            self.vehicles.append(vehicle)
            self.save_data()
            self.update_tables()
            dialog.destroy()
            self.status.set(f"Транспорт '{id_entry.get()}' добавлен")
        
        ttk.Button(dialog, text="Сохранить", command=save).pack(pady=10)
        id_entry.focus()
        dialog.bind('<Return>', lambda e: save())
    
    def edit_client(self):
        selection = self.clients_tree.selection()
        if not selection:
            return
        
        item = self.clients_tree.item(selection[0])
        name = item['values'][0]
        
        for client in self.clients:
            if client.name == name:
                self.clients.remove(client)
                self.update_tables()
                self.add_client()
                break
    
    def edit_vehicle(self):
        selection = self.vehicles_tree.selection()
        if not selection:
            return
        
        item = self.vehicles_tree.item(selection[0])
        vehicle_id = item['values'][0]
        
        for vehicle in self.vehicles:
            if vehicle.vehicle_id == vehicle_id:
                self.vehicles.remove(vehicle)
                self.update_tables()
                self.add_vehicle()
                break
    
    def delete_selected(self):
        selection = self.clients_tree.selection()
        if selection:
            item = self.clients_tree.item(selection[0])
            name = item['values'][0]
            if messagebox.askyesno("Подтверждение", f"Удалить клиента '{name}'?"):
                self.clients = [c for c in self.clients if c.name != name]
                self.save_data()
                self.update_tables()
                self.status.set(f"Клиент '{name}' удален")
            return
        
        selection = self.vehicles_tree.selection()
        if selection:
            item = self.vehicles_tree.item(selection[0])
            vehicle_id = item['values'][0]
            if messagebox.askyesno("Подтверждение", f"Удалить транспорт '{vehicle_id}'?"):
                self.vehicles = [v for v in self.vehicles if v.vehicle_id != vehicle_id]
                self.save_data()
                self.update_tables()
                self.status.set(f"Транспорт '{vehicle_id}' удален")
    
    def load_cargo(self):
        if not self.clients or not self.vehicles:
            messagebox.showwarning("Ошибка", "Добавьте клиентов и транспорт")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Загрузка груза")
        dialog.geometry("350x200")
        
        ttk.Label(dialog, text="Клиент:").pack(pady=5)
        client_var = tk.StringVar()
        client_combo = ttk.Combobox(dialog, textvariable=client_var, 
                                  values=[f"{c.name} ({c.cargo_weight} кг)" for c in self.clients], 
                                  state="readonly")
        client_combo.pack(pady=5)
        client_combo.current(0)
        
        ttk.Label(dialog, text="Транспорт:").pack(pady=5)
        vehicle_var = tk.StringVar()
        vehicle_combo = ttk.Combobox(dialog, textvariable=vehicle_var,
                                    values=[f"{v.vehicle_id} (свободно: {v.free_capacity} кг)" for v in self.vehicles],
                                    state="readonly")
        vehicle_combo.pack(pady=5)
        vehicle_combo.current(0)
        
        def load():
            client_name = client_var.get().split(" (")[0]
            vehicle_id = vehicle_var.get().split(" ")[0]
            
            client = next((c for c in self.clients if c.name == client_name), None)
            vehicle = next((v for v in self.vehicles if v.vehicle_id == vehicle_id), None)
            
            if not client or not vehicle:
                return
            
            if vehicle.current_load + client.cargo_weight <= vehicle.capacity:
                vehicle.current_load += client.cargo_weight
                vehicle.clients.append(client)
                self.save_data()
                self.update_tables()
                dialog.destroy()
                self.status.set(f"Груз загружен")
                messagebox.showinfo("Успех", "Груз загружен")
            else:
                messagebox.showwarning("Ошибка", "Недостаточно места")
        
        ttk.Button(dialog, text="Загрузить", command=load).pack(pady=10)
        dialog.bind('<Return>', lambda e: load())
    
    def optimize(self):
        if not self.clients or not self.vehicles:
            messagebox.showwarning("Ошибка", "Добавьте клиентов и транспорт")
            return
        
        # Сброс загрузки
        for v in self.vehicles:
            v.current_load = 0
            v.clients = []
        
        # Сортировка
        vip_clients = [c for c in self.clients if c.is_vip]
        regular_clients = [c for c in self.clients if not c.is_vip]
        all_clients = sorted(vip_clients, key=lambda x: x.cargo_weight, reverse=True) + \
                     sorted(regular_clients, key=lambda x: x.cargo_weight, reverse=True)
        
        vehicles_sorted = sorted(self.vehicles, key=lambda v: v.capacity, reverse=True)
        
        # Распределение
        for client in all_clients:
            for vehicle in vehicles_sorted:
                if vehicle.current_load + client.cargo_weight <= vehicle.capacity:
                    vehicle.current_load += client.cargo_weight
                    vehicle.clients.append(client)
                    break
        
        self.save_data()
        self.update_tables()
        
        assigned = sum(len(v.clients) for v in self.vehicles)
        total_weight = sum(v.current_load for v in self.vehicles)
        self.status.set(f"Распределено: {assigned}/{len(self.clients)} клиентов, {total_weight} кг")
        messagebox.showinfo("Результат", f"Распределено {assigned} из {len(self.clients)} клиентов")
    
    def update_tables(self):
        # Клиенты
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)
        
        for client in self.clients:
            vip = "Да" if client.is_vip else "Нет"
            self.clients_tree.insert("", tk.END, values=(client.name, client.cargo_weight, vip))
        
        # Транспорт
        for item in self.vehicles_tree.get_children():
            self.vehicles_tree.delete(item)
        
        for vehicle in self.vehicles:
            self.vehicles_tree.insert("", tk.END, values=(
                vehicle.vehicle_id,
                vehicle.type,
                vehicle.details,
                vehicle.capacity,
                vehicle.current_load,
                vehicle.free_capacity
            ))
    
    def save_data(self):
        data = {
            "clients": [{"Имя": c.name, "Вес": c.cargo_weight, "VIP": c.is_vip} for c in self.clients],
            "vehicles": [{"ID": v.vehicle_id, "Тип": v.type, "Детали": v.details,
                         "Грузоподъемность": v.capacity, "Загружено": v.current_load} for v in self.vehicles]
        }
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def load_data(self):
        try:
            with open("data1.json", "r", encoding='utf-8') as f:
                data = json.load(f)
                
                for c in data.get("clients", []):
                    self.clients.append(Client(c["Имя"], c["Вес"], c["VIP"]))
                
                for v in data.get("vehicles", []):
                    vehicle = Vehicle(v["ID"], v["Тип"], v["Грузоподъемность"], v["Детали"])
                    vehicle.current_load = v.get("Загружено", 0)
                    self.vehicles.append(vehicle)
        except:
            pass
    
    def export_data(self):
        if not self.clients and not self.vehicles:
            messagebox.showwarning("Ошибка", "Нет данных для экспорта")
            return
        
        filename = "export.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Клиенты:\n")
            for client in self.clients:
                f.write(f"  {client.name}: {client.cargo_weight} кг\n")
            
            f.write("\nТранспорт:\n")
            for vehicle in self.vehicles:
                f.write(f"  {vehicle.vehicle_id}: {vehicle.current_load}/{vehicle.capacity} кг\n")
        
        self.status.set(f"Данные экспортированы в {filename}")
        messagebox.showinfo("Экспорт", f"Данные сохранены в {filename}")
    
    def show_about(self):
        about_text = "Транспортная компания\nЛабораторная работа\nРазработчик: Хитрик Денис Дмитриевич"
        messagebox.showinfo("О программе", about_text)

def main():
    root = tk.Tk()
    app = TransportCompanyGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()