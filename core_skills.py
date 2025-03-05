import random
rand_list = [random.randint(0, 20) for i in range(10)]
print(rand_list) #[5, 9, 7, 8, 1, 18, 8, 6, 10, 6]

list_comprehension_below_10 = [random.ranint(0, 20) for i in range(10) if i < 10]

print(list_comprehension_below_10)

list_comprehension_below_10 = list(filter(lambda num : num < 10, rand_list))

print(list_comprehension_below_10)