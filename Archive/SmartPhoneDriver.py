from smartphone import Smartphone

def main():
    phone = Smartphone("Apple", "iPhone 14", 128, 100)
    print(phone.show_specs())
    print(phone.upgrade_storage(256))
    print(phone.use_battery(5))
    print(phone.charge_battery())
    print(phone.show_specs())


if __name__ == "__main__":
    main()

