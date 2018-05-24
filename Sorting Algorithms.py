from time import time
import random
import sys
sys.setrecursionlimit(10000)

#Generowanie listy liczb

length = 1000
aList = []

#TUTAJ WSTAWIĆ GENERATOR LISTY

number = length
begin = 0
end = length - 1
for i in range(length):
    aList.append(number)
for i in range(length):
    if i%2 == 0:
        aList[begin] = number
        number -= 1
        begin += 1
    else:
        aList[end] = number
        number -= 1
        end -= 1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#zwykły sort
def zwykly_sort(aList):
    startTime = time()
    sorted(aList, reverse = True)
    return ("Built-In Sort: ") + str(time() - startTime)

#Selection Sort
def selection_sort(aList):
    comparisionsCount = 0
    exchangeCount =0
    currentIndex = 0
    startTime = time()
    lastIndex = len(aList) - 1
    while currentIndex != lastIndex:
        max = 0
        index = 0
        for i in range(currentIndex, len(aList)):
            comparisionsCount += 1
            if aList[i] > max:
                max = aList[i]
                index = i
        exchangeCount += 1
        [aList[currentIndex], aList[index]] = [aList[index], aList[currentIndex]]
        currentIndex += 1
    return (("Selection Sort: ") + str(time() - startTime) + "\n" + "   Comparision Count: " + str(comparisionsCount)) \
           + "\n" + "   Exchange Count: " + str(exchangeCount)


#Insertion Sort
def insertion_sort(aList, shellsort=False):
    comparisionsCount = 0
    exchangeCount = 0
    startTime = time()
    for i in range(1, len(aList)):
        currentValue = aList[i]
        index = i
        comparisionsCount += 1
        while index > 0 and aList[index - 1] < currentValue:
            comparisionsCount += 1
            exchangeCount += 1
            aList[index] = aList[index-1]
            index = index-1
        aList[index] = currentValue
    #return aList
    if shellsort:
        return [aList, exchangeCount, comparisionsCount]
    if not shellsort:
        return ("Insertion Sort: ") + str(time() - startTime) + "\n" + "   Exchange Count: " + str(exchangeCount)  + "\n" \
           + "   Comparision Count: " + str(comparisionsCount)



#Shell Sort z przyrostami Knutha
def knuth(aList):
    l = len(aList)                  #wyznaczanie odstępów knutha
    h = 1
    while h < l:
        h = 3*h + 1
    h = int(h/9)
    return h

def shell_sort(aList):
    comparisionCount = 0
    exchangeCount = 0
    startTime = time()
    flag = False
    h = knuth(aList)
    if h == 1:
        flag = True
    while h > 0:
        finalList =[]
        for i in range(h):
            temp = i
            tempList = []
            while temp < len(aList):
                tempList.append(aList[temp])
                temp += h
            [tempList, exch, comp] = insertion_sort(tempList, True)
            exchangeCount += exch
            comparisionCount += comp
            finalList += tempList
        aList = finalList
        h = int(h/3)
        if h == 0 and not flag:
            h = 1
            flag = True
    #return finalList
    return ("Shell Sort: ") + str(time() - startTime) + "\n" + "   Exchange Count: " + str(exchangeCount)  + "\n" \
           + "   Comparision Count: " + str(comparisionCount)

#Quick Sort
compaCount = 0
exCount = 0

def quickSort(aList):
    startTime = time()
    quickSortStep(aList, 0, len(aList)-1)
    return ("Quick Sort: ") + str(time() - startTime) + "\n" + "   Exchange Count: " + str(exCount) + "\n" \
           + "   Comparision Count: " + str(compaCount)

def quickSortStep(aList, startIndex, endIndex):
    if startIndex < endIndex:
        splitpoint = splitPoint(aList, startIndex, endIndex)

        quickSortStep(aList, startIndex, splitpoint-1)
        quickSortStep(aList, splitpoint+1, endIndex)


def splitPoint(aList, startIndex, endIndex):
    global compaCount
    global exCount
    pivot = aList[startIndex]
    left = startIndex + 1
    right = endIndex
    done = False

    while not done:

        while left <= right and aList[left] >= pivot:
            left += 1
            compaCount += 1

        while right >= left and aList[right] <= pivot:
            right -= 1
            compaCount += 1

        if right < left:
            done = True
            compaCount += 1
        else:
            [aList[left], aList[right]] = [aList[right], aList[left]]
            exCount += 1

    [aList[startIndex], aList[right]] = [aList[right], aList[startIndex]]
    exCount += 1
    return right


#Heap Sort
compCount = 0
exchCount = 0

def exchange(n, m, lis):                #zamiana elementów
  global exchCount
  lis[n], lis[m] = lis[m], lis[n]
  exchCount = exchCount + 1
  return lis

def comparison_and_exchange(n, m, lis):   #porównanie i ewentualna zamiana elementów
  global compCount
  compCount = compCount + 1
  if lis[m] > lis[n]:
      exchange(n, m, lis)
      comparison_and_exchange(int((n - 1) / 2), n, lis)
  return lis

def heap_sort(li):
    startTime = time()
    if len(aList) == 1:
        return ("Heap Sort: ") + str(time() - startTime) + "\n" + "   Exchange Count: " + str(exchCount)  + "\n" \
           + "   Comparision Count: " + str(compCount)
    x = 0
    y = 1
    while y <= (len(li)-1):
        y = 2 * x+1
        comparison_and_exchange(x, y, li)
        y = y + 1
        if y <= (len(aList)-1):
            comparison_and_exchange(x,y, li)
        x = x + 1
    return ("Heap Sort: ") + str(time() - startTime) + "\n" + "   Exchange Count: " + str(exchCount)  + "\n" \
         + "   Comparision Count: " + str(compCount)

print(zwykly_sort(list(aList)))
print(selection_sort(list(aList)))
print(insertion_sort(list(aList)))
print(shell_sort(list(aList)))
print(quickSort(list(aList)))
print(heap_sort(list(aList)))
