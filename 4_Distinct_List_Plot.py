import random
import matplotlib.pyplot as plt

def generate_random_list(size):
    return [random.randint(1, 10) for _ in range(size)]

def countDistinct(unique, data):
    new_list = list(unique)
    for i in range(len(new_list)):
        print("{0} -> ".format(new_list[i]),data.count(new_list[i]))

    # Create a histogram
    plt.hist(data, bins=20, alpha=1, color='blue')

    # Add labels and title
    plt.xlabel("Set Values")
    plt.ylabel("Occurrences")
    plt.title("Set Items")

    # Show the plot
    plt.show()


def main():
    list_size = 30
    random_list = generate_random_list(list_size)
    print(random_list)
    list_set = set(random_list)
    print(list_set)
    print(countDistinct(list_set, random_list))


if __name__ == "__main__":
    main()