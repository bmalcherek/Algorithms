import random
import copy
import math


class BST:

    def __init__(self):
        self.root = None
        self.size = 0

    def __str__(self):
        a_list = self.pre_order()
        result = ""
        for value in a_list:
            node = self.root
            while value != node.value:
                if value < node.value:
                    node = node.leftChild
                else:
                    node = node.rightChild
            result += str(node) + "\n"
        return result

    def insert(self, value):
        if self.root is not None:
            self.__insert_node(value, self.root)
        else:
            self.root = Node(value, root=True)
            self.size += 1

    def __insert_node(self, value, currentNode):
        if value <= currentNode.value:
            if currentNode.leftChild:
                self.__insert_node(value, currentNode.leftChild)
            else:
                currentNode.leftChild = Node(value, currentNode, root=False)
                self.size += 1
        else:
            if currentNode.rightChild:
                self.__insert_node(value, currentNode.rightChild)
            else:
                currentNode.rightChild = Node(value, currentNode, root=False)
                self.size += 1

    def search_max(self):
        track = []
        currentNode = self.root
        done = False
        while not done:
            track.append(currentNode.value)
            if currentNode.rightChild:
                currentNode = currentNode.rightChild
            else:
                done = True
        return "Max value is: " + str(track[-1]) + ", search path: " + str(track)

    def delete_node(self, value):
        self.size -= 1
        node = self.root
        side = 0  # zmienna przechowująca, z której strony dzieckiem jest szukana wartość
        while value != node.value:
            if value < node.value:
                node = node.leftChild
                if node.value == value:
                    side = -1
            else:
                node = node.rightChild
                if node.value == value:
                    side = 1

        root = False
        if node.root:
            root = True

        if not node.is_a_parent():
            if side == -1:
                node.parent.leftChild = None
            elif side == 1:
                node.parent.rightChild = None
            node = None
            if root:
                self.root = None

        elif node.has_left_child() and not node.has_right_child():
            if side == -1:
                node.parent.leftChild = node.leftChild
                node.leftChild.parent = node.parent
            elif side == 1:
                node.parent.rightChild = node.leftChild
                node.leftChild.parent = node.parent
            node = node.leftChild
            if root:
                self.root = node

        elif node.has_right_child() and not node.has_left_child():
            if side == -1:
                node.parent.leftChild = node.rightChild
                node.rightChild.parent = node.parent
            elif side == 1:
                node.parent.rightChild = node.rightChild
                node.rightChild.parent = node.parent
            node = node.rightChild
            if root:
                self.root = node

        else:
            # inOrder = self.in_order()
            # index = inOrder.index(node.value)
            # replacementValue = inOrder[index - 1]
            replacementNode = node.leftChild
            replacementValue = node.leftChild.value
            self.delete_node(replacementValue)
            node.value = replacementValue

    def pre_order(self):
        preOrder = list()
        if self.root is not None:
            self.__pre_order(self.root, preOrder)
        return preOrder

    def __pre_order(self, current_node, preOrder):
        preOrder.append(current_node.value)
        if current_node.has_left_child():
            self.__pre_order(current_node.leftChild, preOrder)
        if current_node.has_right_child():
            self.__pre_order(current_node.rightChild, preOrder)

    def in_order(self):
        inOrder = list()
        if self.root is not None:
            self.__in_order(self.root, inOrder)
        return inOrder

    def __in_order(self, current_node, inOrder):
        if current_node.has_left_child():
            self.__in_order(current_node.leftChild, inOrder)
        inOrder.append(current_node.value)
        if current_node.has_right_child():
            self.__in_order(current_node.rightChild, inOrder)

    def post_order(self):
        postOrder = list()
        if self.root is not None:
            self.__post_order(self.root, postOrder)
        return postOrder

    def __post_order(self, current_node, postOrder):
        if current_node.has_left_child():
            self.__post_order(current_node.leftChild, postOrder)
        if current_node.has_right_child():
            self.__post_order(current_node.rightChild, postOrder)
        postOrder.append(current_node.value)

    def subtree(self, value):
        subtree = list()
        node = self.root
        while value != node.value:
            if value < node.value:
                node = node.leftChild
            else:
                node = node.rightChild
        self.__pre_order(node, subtree)
        return subtree

    def right_rotation(self, value):
        node = self.root
        while value != node.value:
            if value < node.value:
                node = node.leftChild
            else:
                node = node.rightChild
        if node.parent.root:
            node.root = True
            node.parent.root = False
            self.root = node
        if not node.has_right_child():
            node.rightChild = node.parent  # nowy dziecko elementu wokół którego rotujemy
            node.parent.leftChild = None  # usunięcie elementu wokół którego rotujemy jako dziecka dawnego rodzica
            if not node.root:
                if node.parent.parent.value < node.value:
                    node.parent.parent.rightChild = node
                else:
                    node.parent.parent.leftChild = node
                node.parent = node.parent.parent
            else:
                node.parent = None
            node.rightChild.parent = node  # element wokół którego rotujemy staje się nowym rodzicem dawnego rodzica XD
        else:
            node.rightChild.parent = node.parent
            node.parent.leftChild = node.rightChild  # prawe dziecko elementu wokół którego obracamy staje się lewym dzieckiem jego rodzica
            node.rightChild = node.parent
            if not node.root:
                if node.parent.parent.value < node.value:
                    node.parent.parent.rightChild = node
                else:
                    node.parent.parent.leftChild = node
                node.parent = node.parent.parent
            else:
                node.parent = None
            node.rightChild.parent = node

    def left_rotation(self, value):
        node = self.root
        while value != node.value:
            if value < node.value:
                node = node.leftChild
            else:
                node = node.rightChild
        if node.parent.root:
            node.root = True
            node.parent.root = False
            self.root = node
        if not node.has_left_child():
            node.leftChild = node.parent
            node.parent.rightChild = None
            if not node.root:
                if node.parent.parent.value < node.value:
                    node.parent.parent.rightChild = node
                else:
                    node.parent.parent.leftChild = node
                node.parent = node.parent.parent
            else:
                node.parent = None
            node.leftChild.parent = node
        else:
            node.leftChild.parent = node.parent
            node.parent.rightChild = node.leftChild
            node.leftChild = node.parent
            if not node.root:
                if node.parent.parent.value < node.value:
                    node.parent.parent.rightChild = node
                else:
                    node.parent.parent.leftChild = node
                node.parent = node.parent.parent
            else:
                node.parent = None
            node.leftChild.parent = node

    def __binary_searching(self, a_list, b_list):
        index = math.floor(len(a_list) / 2)
        if len(a_list) <= 2:
            for element in a_list:
                b_list.append(element)
        else:
            b_list.append(a_list[index])
            self.__binary_searching(a_list[:index], b_list)
            self.__binary_searching(a_list[index + 1:], b_list)
        print(b_list)

    def avl(self, a_list):
        a_list = sorted(a_list)
        b_list = list()
        if self.root:
            return "This tree already has elements!"
        else:
            self.__binary_searching(a_list, b_list)
            for element in b_list:
                self.insert(element)

    def dsw(self):
        tmp = self.root
        while tmp is not None:
            if tmp.has_left_child():
                tmp = tmp.leftChild
                self.right_rotation(tmp.value)
            elif tmp is None:
                break
            else:
                tmp = tmp.rightChild
        m = int(2 ** math.floor(math.log(self.size + 1, 2)) - 1)  # wzór z https://pl.wikipedia.org/wiki/Algorytm_DSW
        tmp = self.root
        rotations = int(self.size - m)
        for i in range(rotations):
            self.left_rotation(tmp.rightChild.value)
            tmp = tmp.parent.rightChild
        while m > 1:
            m = math.floor(m / 2)
            rotations = int(m)
            tmp = self.root
            for i in range(rotations):
                self.left_rotation(tmp.rightChild.value)
                tmp = tmp.parent.rightChild


class Node:
    def __init__(self, value, parent=None, left=None, right=None, root=None):
        self.value = value
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.root = root

    def __str__(self):
        ret = "Value = " + str(self.value)
        if self.leftChild is not None:
            ret += ", Left Child = " + str(self.leftChild.value)
        else:
            ret += ", Left Child = None"
        if self.rightChild is not None:
            ret += ", Right Child = " + str(self.rightChild.value)
        else:
            ret += ", Right Child = None"
        if self.parent is not None:
            ret += ", Parent = " + str(self.parent.value)
        else:
            ret += ", Parent = None"
        return ret

    def has_left_child(self):
        if self.leftChild:
            return True
        else:
            return False

    def has_right_child(self):
        if self.rightChild:
            return True
        else:
            return False

    def is_a_parent(self):
        if self.has_right_child() or self.has_left_child():
            return True
        else:
            return False


def menu():
    print("MENU")
    print(
        " 1.Sciezka do maks elementu \n 2.Usun element \n 3.In-order \n 4.Pre-order \n 5.Post-order(usuwa całe drzewo) \n 6.Poddrzewo \n 7.Równoważenie \n 8.KONIEC")
    wybor = input("Wybierz liczbe od 1 do 8:")
    if int(wybor) == 1:
        print(tree.search_max())
        menu()
    elif int(wybor) == 2:
        print("USUWANIE")
        ile = input("Ile elementow chcesz usunac?:")
        for e in range(int(ile)):
            klucz = int(input("Podaj klucz"))
            tree.delete_node(klucz)
            print(tree.pre_order())
        menu()
    elif int(wybor) == 3:
        print("IN ORDER")
        print(tree.in_order())
        menu()
    elif int(wybor) == 4:
        print("PRE ORDER")
        print(tree.pre_order())
        menu()
    elif int(wybor) == 5:
        print("POST ORDER")
        print(tree.post_order())
        menu()
    elif int(wybor) == 6:
        print("PODDRZEWO")
        klcz = int(input("Podaj klucz którego poddrzewo chcesz wyswietlic "))
        print(tree.subtree(klcz))
        menu()
    elif int(wybor) == 7:
        print("RÓWNOWAŻENIE")
        tree.dsw()
        print(tree.pre_order())
        menu()
    elif int(wybor) == 8:
        return 0


tree = BST()
length = 10
test = [5, 10, 3, 12, 1, 7, 30, 25, 9, 40, 2]
# test = [5, 7, 3, 2, 4, 6, 8]
for new in test:
    tree.insert(new)
# for i in range(length):
#     number = random.randint(1, 2000)
#     tree.insert(number)
# a_list = list()
# for i in range(length):
#     a_list.append(random.randint(1, 2000))
# tree.avl(test)
tree.delete_node(5)
print(tree.pre_order())
menu()
