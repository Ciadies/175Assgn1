'''
Created on Feb. 3, 2024

@author: Sebastian
'''
def findLargestSold(transactions):
    '''
    Identifies the 3 largest sold transactions
    '''
    largest = [transactions[1],transactions[2],transactions[3]]
    for i in range(4,len(transactions)):
        for entry in largest:
            if int(transactions[i][3]) > int(entry[3]):
                j = findSmallestEntry(largest, 3) #finds the index of the smallest entry in the list "largest"
                largest[j] = transactions[i] #replaces the smallest entry with that of the larger entry
                break
    return largest
            
def findSmallestEntry(transactions, compareTo):
    '''
    finds the index of the smallest entry in a given list
    '''
    smallest = 1000000000000 
    smallestEntry = 0
    for i in range(len(transactions)):
        if int(transactions[i][compareTo]) < smallest:
            smallest = int(transactions[i][compareTo])
            smallestEntry = i
    return smallestEntry

def getName(code, product):
    '''
    Takes a product code and list of products and returns the name associated with the code
    '''
    for entry in product:
        if entry[0] == code:
            return entry[1]
        
def convertToList(filename):
    '''
    Takes a file and converts it to a list
    '''
    with open(filename, "r") as file:
        lines = file.readlines()
    for i in range(len(lines)): #removes all new line and whitespace characters that are at the ends of the file and separates each entry into segments
        lines[i] = lines[i].strip()
        lines[i] = lines[i].split(",")
    return(lines)    
    
def findHighestPrice(sales, products, refund):
    '''
    Takes 3 lists and finds the 3 highest priced entries amongst them
    '''
    for j in range(1,len(refund)):
        i = int(refund[j][0]) 
        sales[i][3] = '0' #removes all refunded producst by setting their quantity sold to 0
        
    largest = [[getName(sales[1][2],products), convertToPrice(sales[1], products)],
               [getName(sales[2][2],products), convertToPrice(sales[2], products)],
               [getName(sales[3][2],products), convertToPrice(sales[3], products)]] #each entry contains product name and price
    
    for i in range(4, len(sales)):
        for entry in largest:
            if convertToPrice(sales[i], products) > entry[1]:
                j = findSmallestEntry(largest, 1)
                largest[j] = [getName(sales[i][2],products), convertToPrice(sales[i], products), sales[i]]
                break
    return largest

def convertToPrice(sale, products):
    '''
    Takes a sale and a list of products and returns the total price of the transaction
    '''
    itemId = sale[2]
    price = 0
    for entry in products:
        if entry[0] == itemId:
            price = entry[2]
    return (int(sale[3]) * int(price)) * (1 - float(sale[4]))

def findDiscountAmount(sale, products):
    '''
    Takes a transaction and a list of list of products and returns the total amount discounted
    '''
    itemId = sale[2]
    price = 0
    for entry in products:
        if entry[0] == itemId:
            price = entry[2]
    return (int(sale[3]) * int(price)) * float(sale[4])

def fillDict(dict, product, sale, refund):
    '''
    Takes a dictionary and returns a dictionary with the total sales, average discount, total amount discounted, and total income filled in
    '''
    for j in range(1,len(refund)):
        i = int(refund[j][0]) 
        sale[i][3] = '0' #removes all refunded producst by setting their quantity sold to 0
    
    for i in range(1, len(sale)):
        dict[sale[i][2]][1] += int(sale[i][3])
        dict[sale[i][2]][2] += convertToPrice(sale[i], product)
        dict[sale[i][2]][3] = (dict[sale[i][2]][3] + float(sale[i][4]))/2
        dict[sale[i][2]][4] += findDiscountAmount(sale[i], product)
    
def main():
    product = convertToList("transactions_Products.csv")
    sale = convertToList("transactions_Sales.csv")
    refund = convertToList("transactions_Returns.csv")
    print("Part 1")
    largest = findLargestSold(sale)
    largest.sort(reverse = True, key = lambda x: int(x[3]))
    
    for entry in largest:  #1
        print("%20s %3s"%(getName(entry[2],product), entry[3]))
        
    print("Part 2")
    purchases = findHighestPrice(sale, product, refund)
    purchases.sort(reverse= True, key = lambda x: int(x[1]))
    
    for entry in purchases: #2
        print("%20s $%.2f"%(entry[0], float(entry[1])))
        
    print("Part 3")    
    productDict = {}
    for i in range(1,len(product)):
        productDict[product[i][0]] = [product[i][1],0,0,0,0] #key: name, total sales, total income from product, average discount, total discounted amount
    fillDict(productDict, product, sale, refund)
   
    header = "+---+--------------------+---+-----------+------+-----------+"
    for key in productDict: #3
        print(header)
        
        if str(productDict[key][3]*100).find(".") == 1: #adds the 0 where it belongs
            print("|%3s|%20s|%3s|$%10.2f|0%-4.2f%%|$%10.2f|"%(key,productDict[key][0],productDict[key][1],productDict[key][2],productDict[key][3]*100,productDict[key][4]))
        else: 
            print("|%3s|%20s|%3s|$%10.2f|%5.2f%%|$%10.2f|"%(key,productDict[key][0],productDict[key][1],productDict[key][2],productDict[key][3]*100,productDict[key][4]))
    print(header)
    
    print("Part 4")
    dayDict = {}
    for i in range(1,len(sale)):
        if sale[i][1] in dayDict:
            dayDict[sale[i][1]] += int(sale[i][3])
        else:
            dayDict[sale[i][1]] = int(sale[i][3])
    
    for key in dayDict:
        print("%9s:%3i"%(key,dayDict[key]))
    
    print("Part 5")
    returnDict = {}
    for i in range(1,len(refund)):
        code = sale[int(refund[i][0])][2]
        if code in returnDict:
            returnDict[code] += 1
        else:
            returnDict[code] = 1
    
    for key in returnDict:
        print("%-3s %-20s %3i"%(key, getName(key,product),returnDict[key]))
    
    print("Part 6")
    with open("transactions_units.txt","w") as file:
        for key in productDict:
            file.write(f"%s,%s\n"%(key,productDict[key][1]))
    
if __name__ == "__main__":
    main()