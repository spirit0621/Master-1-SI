#try:
#    print(2 / 0)
#except ZeroDivisionError
#   print("Impossible voyons!")


mylist = [1, 2, 3, 4, 28]
#print(mylist[8])

try:
    print(mylist[8])
except IndexError:
        print("doesn't exists bro!")
