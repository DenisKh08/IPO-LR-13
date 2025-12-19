class client():
    name = ""
    cargo_weight = -1
    is_vip = True

    def __init__(self):
        self.name = input("введите ваше имя: ")
        self.cargo_weight = float(input("введите вес вашего груза в тоннах: "))
        is_client_vip = input("вы являетесь vip нашей компании(да/нет): ")

        if is_client_vip == "да":
            self.is_vip = True
        else:
            self.is_vip = False

    def __str__(self):
        return f'''
        имя клиента: {self.name}
        вес груза клиента: {self.cargo_weight}
        VIP(?): {self.is_vip}
        '''