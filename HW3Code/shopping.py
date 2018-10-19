
# Jason Hoffman
# C325, Homework 3
# October 14, 2018



# Memoized recursive knapsack function, with table k
# used to store data
def knapsack(capacity, weights, costs, n, k):
    if k[n-1][capacity-1] == -1:
      result = k[n-1][capacity-1]
    if n == 0 or capacity == 0:
        result = 0
    elif weights[n-1] > capacity:
        result = knapsack(capacity, weights, costs, n - 1, k)
    else:
        result = max(
            costs[n-1] + knapsack(capacity - weights[n - 1], weights, costs, n -1, k),
            knapsack(capacity, weights, costs, n -1, k)
        )
    k[n-1][capacity-1] = result
    return result


# This function loops backward through the table k to find
# which items each member holds
def extractItems(sack, capacity, weight):
    items = []
    # Get the final item in the first row
    p = capacity - 1
    # If first == last than one item was selected
    if (sack[0][p] == sack[len(sack) - 1][p]):
        items.append(1)
    else:
        # Loop backward through sack
        for i in reversed(range(len(sack))):
            # Find first instance of when item was selected to get its index in weight array
            if (sack[i][p] != sack[i - 1][p]) and sack[i][p] > 0 and sack[i - 1][p] >= 0 and p > 0:
                items.append(i + 1)
                # We can subtract this weight and start from the point where the prevous
                # selection would have been made
                p = p - weight[i]
    # Return array of indexes
    return items




out = open("shopping.out", "w")

with open("shopping.txt") as f:
    # Get number of test cases
    tc = int(f.readline().strip())
    # Loop through each test case
    for i in range(tc):
        out.write("\nTest case: " + str(i+1) + "\n")
        # Get item count for test cases
        itemCount = int(f.readline().strip())
        items = []
        # Loop to get each item from test case
        for j in range(itemCount):
            # Append items as tuples with price/weight
            items.append(tuple(map(int, f.readline().split())))
        # Get number of family members
        famCount = int(f.readline().strip())
        fam = []
        # Loop through family members
        for c in range(famCount):
            fam.append(int(f.readline().strip()))
        # Get two arrays from price/weight tuples
        price, weight = list(map(list, zip(*items)))
        total = 0
        # Create array to show carried items for each family member
        carriedItems = [0 for i in range(itemCount)]
        # Loop through family members
        for x in range(len(fam)):
            # Create table
            sack = [[-1 for i in range(fam[x])] for j in range(itemCount)]
            # Get total from knapsack function
            res = knapsack(fam[x], weight, price, len(items), sack) 
            # Add to family total
            total = total + res
            # Get items carried by current family member
            carriedItems[x] = extractItems(sack, fam[x], weight)
        out.write("Total price: " + str(total) + "\n")
        out.write("Member items:\n")
        # Write items carried
        for i in range(len(fam)):
                result = ""
                # Reverse to write in order they appear in data
                for j in reversed(range(len(carriedItems[i]))):
                    result =  result + " " + str(carriedItems[i][j])
                out.write(str(i + 1) + ": " + str(result) + "\n")

out.close()