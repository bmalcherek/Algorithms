import random

f = open("plecak.txt", "w")
sizeOfBackpack = 10
numberOfElements = 6
f.write(str(numberOfElements) + " " + str(sizeOfBackpack) + "\n")
elements = list()
for i in range(numberOfElements):
    size = random.randint(1, int(sizeOfBackpack / 3))
    value = random.randint(1, int(numberOfElements / 2))
    elements.append([size, value])
i = 0
for element in elements:
    if i == 0:
        f.write(str(element[0]))
    else:
        f.write(" " + str(element[0]))
    i += 1
i = 0
f.write("\n")
for element in elements:
    if i == 0:
        f.write(str(element[1]))
    else:
        f.write(" " + str(element[1]))
    i += 1
