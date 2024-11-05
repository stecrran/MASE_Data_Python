from CarObj import Car

def main():
    print("Example to demonstrate encapsulation")
    my_car = Car("Toyota", "Corolla")

    print(my_car.get_make())
    my_car.set_make("Honda")
    print(my_car.get_make())

    my_car.update_model("Civic")
    my_car.display_details()

    print(my_car._make)
    print(my_car.__get_model())
    #print(my_car.__model)

if __name__ == "__main__":
    main()