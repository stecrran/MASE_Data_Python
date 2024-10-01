import csv


def writeToCSVFile(headers, data, nme):
    with open(nme, 'w', encoding="UTF8", newline = '') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(headers)
        # write multiple rows
        writer.writerows(data)


def main():
    # csv file name
    csvFileName = 'students.csv'
    # csv header
    headers = ['ID', 'Name', 'Age', 'Grade']
    # csv data
    data = [[1, "Harmonie", 18, 97],
            [2, "Harry", 17, 75],
            [3, "Ron", 19, 70],
            [4, "Luna", 16, 81],
            [5, "Emily", 15, 85]]

    writeToCSVFile(headers, data, csvFileName)
    readFromCSVFile(csvFileName)


def readFromCSVFile(nme):
    file = open(nme, "r")
    data = list(csv.reader(file, delimiter=","))
    # print (data)
    printCSVContents(data)
    # print([row[2] for row in data])
    # print([float(row[2]) for row in data[1:]])

    # print and calculate information about file
    sum_ages = sum([float(row[2]) for row in data[1:]])
    sum_grades = sum([float(row[3]) for row in data[1:]])
    count_students = len(data)-1
    average_grade = sum_grades / count_students
    average_age = sum_ages / count_students

    print("\n***** Quick Analysis *****")
    print("Total number of students: {0}".format(count_students))
    print("Average grade: {0:.2f}%".format(average_grade))
    print("Average student age: {0:.2f}".format(average_age))



def printCSVContents(data):
    for row in data:
        # To print structure and show data type use:
        #print(row)
        # For printing contents use:
        print(" ".join(row))


if __name__ == "__main__":
    main()

