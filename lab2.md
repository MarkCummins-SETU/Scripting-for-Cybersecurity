# Lab 2 — File Handling & Regex in Python

**Learning outcomes**

* Understand how to open, read, and process text files in Python.
* Practice applying regular expressions (`regex`) to extract structured data.
* Combine both skills to analyze a log file and produce a report.

---

## Background

In Lab 1, we had a very brief intoduction to using Codespaces. Now we're going to jump straight into some python development, we'll be introducing lots of new ideas so don't panic. You should review all of the bits introduced in this lab several time over the next few weeks until you're comfortable with the concepts;. Remember we're introducing some of the skills needed to complete our first assignment in about 3 weeks. 

> ⚠️ This is a huge step up, so take your time and make sure you understand each step and each snippet of code. Feel free to ask people for help, in the labs or on Discord etc.

> 💡 This lab counts as your challenge lab. Make sure to save all your files and it will count towards your extra credit. You don't need to fully solve the lab just make a good effort at it. You don't need to submit anything you will just need to show your github repo later in the term.

## Scenario

Security logs contain valuable information such as IP addresses, usernames, and timestamps. Manually scanning these logs is inefficient. In this lab, you will **build your skills step by step** (working with files, practicing regex) before combining them to complete a real-world task.

---

## Setup

Review the steps from lab 1 if needed and create a new repo called  `lab-02` then open a new codespace for this lab.

## Part 1: File Handling in Python

Python makes it simple to read from and write to text files.

### Example 1: Reading a file line by line

Create a file called `sample.txt` with the following content:

```
Hello
World
Python
```

Then run this code in a new script (`file_example.py`):

```python
with open('sample.txt', 'r') as f:
    for line in f:
        print(line)
```

> ⚠️ Python doesn't use curly brackets to control logic blocks for loops etc. instead it uses indentation. So spaces and indentation matter in python. Look at the give code snippets carefully.


> **Task 1.1**: Run the script and observe the output. Why are there blank lines between each word? (Hint: print adds a newline and the file line already has one.)

**Expected output:**

```
Hello

World

Python

```

---

### Example 2: Stripping newlines

```python
with open('sample.txt', 'r') as f:
    for line in f:
        print(line.strip())
```

> **Task 1.2 Optional task:**:  Modify the code so that it prints line numbers, e.g. `1: Hello`.

**Expected output:**

```
1: Hello
2: World
3: Python
```

---

### Example 3: Writing to a file

```python
with open('output.txt', 'w') as f:
    f.write("This is a new file.\n")
    f.write("It has two lines.\n")
```

> **Task 1.3**: Write a program that copies all lines from `sample.txt` into `copy.txt`.

---

## Part 2: Regular Expressions (Regex)

Regex is a powerful way to search text for patterns.

### Example 4: Matching simple text

```python
import re

pattern = r"cat"
text = "The cat sat on the mat."

matches = re.findall(pattern, text)
print(matches)
```

> **Task 2.1**: Change the pattern to `r"at"`. What matches do you get?

**Expected output:**

```
['at', 'at']
```

---

### Example 5: Matching digits

```python
import re

pattern = r"\d+"
text = "Order 123 was placed on 2023-05-01."

print(re.findall(pattern, text))
```

> **Task 2.2**: Modify the regex to match words instead of numbers.

**Expected output with `r"[A-Za-z]+"`:**

```
['Order', 'was', 'placed', 'on']
```

---

### Example 6: Matching IP addresses

```python
import re

pattern = r"\d+\.\d+\.\d+\.\d+"
text = "Failed login from 192.168.0.1 at 10:30"

print(re.findall(pattern, text))
```

> **Task 2.3**: Add another IP address into the string and check if both are found.

**Expected output:**

```
['192.168.0.1', '10.0.0.5']
```

---

## Part 3: Putting it together — Analyzing Logs

Now that you can:

* Read and write files (Part 1),
* Use regex to find patterns (Part 2),

you are ready to analyze a log file.

Create a file called `auth.log` with the following sample entries:

```
Apr 10 12:34:56 ubuntu sshd[12345]: Accepted password for alice from 192.168.1.10 port 54822 ssh2
Apr 10 12:35:01 ubuntu sshd[12346]: Failed password for invalid user bob from 10.0.0.5 port 51900 ssh2
Apr 10 12:36:22 ubuntu sshd[12347]: Accepted publickey for charlie from 203.0.113.5 port 34567 ssh2
Apr 10 12:37:05 ubuntu sshd[12348]: Failed password for root from 198.51.100.23 port 59876 ssh2
Apr 10 12:38:00 ubuntu sshd[12349]: Connection closed by 127.0.0.1 port 22
```

### Step 1: Print the file lines

Write a Python script (`lab2.py`) that opens `auth.log` and prints each line.

**Expected output:**

```
Apr 10 12:34:56 ubuntu sshd[12345]: Accepted password for alice from 192.168.1.10 port 54822 ssh2
Apr 10 12:35:01 ubuntu sshd[12346]: Failed password for invalid user bob from 10.0.0.5 port 51900 ssh2
Apr 10 12:36:22 ubuntu sshd[12347]: Accepted publickey for charlie from 203.0.113.5 port 34567 ssh2
Apr 10 12:37:05 ubuntu sshd[12348]: Failed password for root from 198.51.100.23 port 59876 ssh2
Apr 10 12:38:00 ubuntu sshd[12349]: Connection closed by 127.0.0.1 port 22
```

### Step 2: Extract IP addresses

Use the regex `r"\d+\.\d+\.\d+\.\d+"` to find all IP addresses. 

**Expected output (all IPs in a list):**

```
['192.168.1.10', '10.0.0.5', '203.0.113.5', '198.51.100.23', '127.0.0.1']
```

### Step 3: Get unique IPs

Convert the list to a set, then print each unique IP.

```
# Convert to a set to remove duplicates
unique_ips = set(ips)

# Print each unique IP
print("Unique IPs:")
for ip in unique_ips:
    print(ip)
```

**Expected output (order may vary):**

```
10.0.0.5
127.0.0.1
192.168.1.10
198.51.100.23
203.0.113.5
```

### Step 4: Save results

Write the unique IPs to a new file `unique_ips.txt`, one per line.

**Expected content of `unique_ips.txt`:**

```
10.0.0.5
127.0.0.1
192.168.1.10
198.51.100.23
203.0.113.5
```

---

## Final Deliverables

* **`lab2.py`**: A Python script that reads `auth.log`, extracts IP addresses using regex, and writes unique IPs into `unique_ips.txt`.
* **`unique_ips.txt`**: Output file with one IP address per line.

---

By completing this lab, you will:

* Be confident opening, reading, and writing files.
* Understand how to construct regex for digits, words, and IP addresses.
* Apply both skills together to solve real-world problems.
