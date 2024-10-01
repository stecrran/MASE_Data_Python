from PartTimeEmployeeObj import PartTimeEmployee
from FullTimeEmployeeObj import FullTimeEmployee

def main():
    employee1 = FullTimeEmployee("John Smith", 1001, 60000)
    employee2 = PartTimeEmployee("Jane Doe", 2002, 15.50, 20)

    print("Full-Time Employee:")
    employee1.display_info()
    print("\nPart-Time Employee:")
    employee2.display_info()

    print("\nPart-Time Employee Pay:")
    print("{0} earned €{1:.2f}".format(employee2.get_employee_name(),employee2.calculate_pay()))

if __name__ == "__main__":
    main()
