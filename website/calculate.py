import numpy as np
from scipy import linalg
from ast import literal_eval as le
import json
np.set_printoptions(suppress=True)

nutrients_quantity_dict = json.load(open('nutrients_quantity_dict.txt'))
requirements = json.load(open('requirements_dict.txt'))

def generateMatrix(kind, available_feed):
    A = []
    b = []
    for feed in available_feed:
        temp = []
        for key, value in requirements[kind].items():
            # print(feed, key)
            # print(value)
            temp.append(nutrients_quantity_dict[feed][str(key)])
            b.append(value)
        A.append(temp)
    return A, b

def calculate_feed(animal, age, available_feed):
    # Ax=b
    A, b= generateMatrix('peaking', available_feed)
    A = np.array(A)
    b = np.array(b[:len(A[0])])
    # print('Original -> ', A.shape, b.shape)
    transposed_A = np.transpose(A)
    transposed_b = np.transpose(b)
    # print('Transposed -> ', transposed_A.shape, transposed_b.shape)
    inv_A = np.linalg.pinv(transposed_A)
    output = np.dot(inv_A, transposed_b)
    output = output * 100
    # print(output)
    # print(len(A[0]))
    # print(matrix)
    # requirement = requirements[animal]
    # available_feed1 = []
    # length = len(available_feed)
    # for x in available_feed:
    #     available_feed1.append(db[x][:length])
    # available_feed = np.array(available_feed1)
    # goat1 = requirement[:length]
    # requirement = np.array(goat1)
    # transposed_available_feed = np.transpose(available_feed)
    # inv_transposed_available_feed = np.linalg.pinv(transposed_available_feed)
    # transposed_goat = np.transpose(requirement)
    # output = np.dot(inv_transposed_available_feed, transposed_goat)
    # output = output * 100
    result = []
    for x in output:
        result.append(round(x/(sum(output)/100), 2))
    return result
print(calculate_feed('goat', 1, ['barley_grain', 'peanut_meal_solvent', 'soybeans_full_fat_cooked']))
