import heatDiffusion
import time


def testMultipleTimes():
    nbIterations = 50

    for i in range(10, 110, 10):    #de 10 à 100 inclu
        startTime = time.time()
        heatDiffusion.HDPlot(i, i, nbIterations, False)
        endTime = time.time()

        print("for dimensions :", i, "x", i, "with", nbIterations, "iterations, it took", endTime-startTime, "sec")

def singleTest(n_rows, n_cols, nbIterations):

    startTime = time.time()
    heatDiffusion.HDPlot(n_rows, n_cols, nbIterations, True)
    endTime = time.time()

    print("for dimensions :", n_rows, "x", n_cols, "with", nbIterations, "iterations, it took", endTime - startTime, "sec")

singleTest(10, 10, 500)