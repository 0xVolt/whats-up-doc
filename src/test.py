def sum():
    sum = 0
    for i in range(10):
        sum += i

    return sum

def calculate_gravitational_force(mass1, mass2, distance):
    return (mass1 * mass2) / (distance ** 2)

def reverse_string(input_str):
    return input_str[::-1]

import random
import string

def generate_random_password(length=8):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def is_anagram(str1, str2):
    str1_sorted = sorted(str1)
    str2_sorted = sorted(str2)
    return str1_sorted == str2_sorted