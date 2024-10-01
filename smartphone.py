class Smartphone:

    def __init__(self, brand, model, storage_capacity, battery_health):
        self.__brand = brand
        self.__model = model
        self.__storage_capacity = storage_capacity
        self.__battery_health = battery_health

    def get_brand(self):
        return self.__brand

    def get_model(self):
        return self.__model

    def get_storage_capacity(self):
        return ("{0}GB".format(self.__storage_capacity))

    def get_battery_health(self):
        return ("{0}%".format(self.__battery_health))

    def upgrade_storage(self, new_capacity):
        if new_capacity > self.__storage_capacity:
            self.__storage_capacity = new_capacity
            return ("Storage upgraded to {0}GB".format(self.__storage_capacity))

    def use_battery(self, hours):
        return (self.__battery_health - (hours*0.5))

    def charge_battery(self):
        self.__battery_health = 100
        return self.__battery_health

    def show_specs(self):
        return ("Brand: {0}, Model: {1}, Storage: {2}, Battery: {3}"
                .format(self.get_brand(), self.get_model(), self.get_storage_capacity(), self.get_battery_health()))