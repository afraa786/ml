# u cant chage them by executing a runnign functio on them 
#strings are immutable


friends = ["anjali", "afraa", "anusha"]
# friends[2] = "a"
print(friends[2])
print(friends)

numbers = [54, 2, 34, 4, 3]
numbers.sort()
print(numbers)

# appends(), extends(), insert()

friends.insert(1, "fareed")
friends[0] = "tanushree"
friends[3] = "rehbar"
print(friends)