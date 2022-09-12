import matplotlib.pyplot as plt

def graph(title, dataTime, dataNumber):
    plt.plot(dataNumber, dataTime , '-ok', color='blue')
    plt.xlabel("Number of blank spaces")
    plt.ylabel("Execution time")
    plt.title(title)
    plt.show()

def graphDouble(title, dataTime, dataNumber, dataTime2, dataNumber2):
    plt.plot(dataNumber, dataTime, '-ok', color='blue')
    plt.plot(dataNumber2, dataTime2, '-ok', color='red')
    plt.xlabel("Number of blank spaces")
    plt.ylabel("Execution time")
    plt.title(title)
    plt.show()