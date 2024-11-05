class Car:
    def __init__(self, make, model):
        self._make = make #Protected
        self.__model = model #Private


    def get_make(self):
        return self._make


    def set_make(self, make):
        self._make = make


    def __get_model(self):
        return self.__model


    def __set_model(self, model):
        self.__model = model


    def update_model(self, model):
        self.__set_model(model)


    def display_details(self):
        print("Car details: {0}, {1}".format(self._make, self.__model))
