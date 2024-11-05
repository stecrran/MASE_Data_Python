import pandas as pd

def main():

    values = [5, 7, 8, 22, 50]
    theBins = [0, 3, 7, 10, 20, 100]
    theLabels = ['v.small', 'small', 'medium', 'large', 'v.large']

    values_filtered = pd.cut(values, bins = theBins, labels = theLabels)

    print(values_filtered)


    values2 = [5, 7, 8, 8, 22, 50]
    theBins2 = [0, 3, 7, 10, 20, 100]
    theLabels2 = ['small', 'medium', 'large', 'v.large']

    values_filtered2 = pd.qcut(values2, q=4, labels = theLabels2)

    print(values_filtered2)


if __name__=='__main__':
    main()