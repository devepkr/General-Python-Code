

"""
generator is a special type of iterator that allows you to iterate over
data without storing the entire dataset in memory
1. Memory Efficient: Doesn't store all values in memory.
2. Lazy Evaluation: Values are produced only when requested
"""



import sys



def my_gen():
    cnt = 1
    while cnt < 20:
        yield cnt
        cnt += 1
s = my_gen()
print(next(s))
print(next(s))
print(next(s))




# l = []
# for item in range(1, 21):
#     l.append(item)
# print(sys.getsizeof(l))



