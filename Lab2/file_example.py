

# Example 1 / Task 1.1
print ("\n Example 1 / Task 1.1")
with open('sample.txt', 'r') as f:
    for line in f:
        print(line)

# Example 2: Stripping newlines
print ("\n Example 2: Stripping newlines")
with open('sample.txt', 'r') as f:
    for line in f:
        print(line.strip())

# Option task 1.2 - Modify the code so that it prints line numbers, e.g. `1: Hello`.
print ("\n Task 1.2 - print line numbers")
with open('sample.txt', 'r') as f:
    line_number = 1               # start counting at 1
    for line in f:
        print(f"{line_number}: {line.strip()}")  # print with number
        line_number = line_number + 1           # increase counter


### Example 3: Writing to a file
print ("\n Example 3: Writing to a file")
with open('output.txt', 'w') as f:
    f.write("This is a new file.\n")
    f.write("It has two lines.\n")

### Task 1.3: Write a program that copies all lines from `sample.txt` into `copy.txt`.
print ("\n task 1. 3: Copying file")
with open('copy.txt', 'w') as a:
    with open('sample.txt', 'r') as b:
        for line in b:
            a.write(line) 

print ("\n Part 2 ---------------------------------------")
import re


### Example 4: Matching simple text
print ("\n Example 4: Matching simple text")
pattern = r"cat"
text = "The cat sat on the mat."

matches = re.findall(pattern, text)
print(matches)


### Task 2.1 Change the pattern to `r"at"`. What matches do you get?

print ("\n Task 2.1: Matching simple text 'at' ")
pattern = r"at"
text = "The cat sat on the mat."

matches = re.findall(pattern, text)
print(matches)


### Example 5: Matching digits
print ("\n Example 5: Matching digits")

pattern = r"\d+"
text = "Order 123 was placed on 2023-05-01."

print(re.findall(pattern, text))


### Task 2.2 :Modify the regex to match words instead of numbers.
print ("\n Task 2.2 :Modify the regex to match words instead of numbers.")
pattern = r"[A-Za-z]+"
text = "Order 123 was placed on 2023-05-01."

print(re.findall(pattern, text))


### Example 6: Matching IP addresses
print ("\n Example 6: Matching IP addresses")

pattern = r"\d+\.\d+\.\d+\.\d+"
text = "Failed login from 192.168.0.1 at 10:30"

print(re.findall(pattern, text))

### Task 2.3: Add another IP address into the string and check if both are found.
print ("\n Task 2.3: Add another IP address into the string and check if both are found.")
pattern = r"\d+\.\d+\.\d+\.\d+"
text = "Failed login from 192.168.0.1 at 10:30, good login from 6.6.6.6"

print(re.findall(pattern, text))

## Part 3: Putting it together — Analyzing Logs
print ("\n Part 3: Putting it together — Analyzing Logs")
import re
ips=[]

### Step 1: Print the file lines
with open('auth.log', 'r') as f:
    for line in f:
        print(line.strip())

### Step 2: Extract IP addresses
        ip_pattern = r"\d+\.\d+\.\d+\.\d+"
        found_ips = re.findall(ip_pattern,line)
        for ip in found_ips:
            ips.append(ip)
    print (ips)

### Step 3: Get unique IPs
unique_ips = set(ips)

print("\nUnique IPs:")
for ip in unique_ips:
    print(ip)

### Step 4: Save results
with open("unique_ips.txt", "w") as out:
    for ip in unique_ips:
        out.write(ip + "\n")