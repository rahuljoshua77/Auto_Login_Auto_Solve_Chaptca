import re 
  
# Function to extract all the numbers from the given string 
# Driver code 
b = []

ss = [": 6.2", ": 2.2", ": 2.2", ": 2.2", "0"]
jumlah = 0
s = "."

for i in ss:
    for c in range(len(ss), 3):
        array = re.findall(r'[0-9]+', i) 
        join = array[0]+s+array[1]
        b.append(join)

for x in b:
    
    jumlah = jumlah + float(x)
    total = jumlah/len(b)

print(jumlah)
print(total)