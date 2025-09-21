# Lab 2-1 — File Handling & Regex in Python (Cheat Sheet)

This cheat sheet summarizes the key commands, functions, and regex patterns introduced in **Lab 2-1**.

---

## File Handling Basics

### Opening a file

```python
with open('filename.txt', 'r') as f:   # read mode
    ...
with open('filename.txt', 'w') as f:   # write mode (overwrites)
    ...
with open('filename.txt', 'a') as f:   # append mode
    ...
```

### Reading lines

```python
for line in f:            # iterate line by line
    print(line)

line.strip()               # removes whitespace and newlines
```

### Writing to files

```python
with open('output.txt', 'w') as f:
    f.write("Hello World\n")
```

### Working with sets (for uniqueness)

```python
ips = ['192.168.0.1', '192.168.0.1', '10.0.0.5']
unique_ips = set(ips)   # {'192.168.0.1', '10.0.0.5'}
```

---

## Regex Basics (using the `re` module)

### Importing

```python
import re
```

### Finding all matches

```python
re.findall(pattern, text)
```

### Common patterns

* `\d` → digit (0–9)
* `\d+` → one or more digits
* `\w` → word character (letters, digits, underscore)
* `\s` → whitespace
* `.` → any character (except newline)
* `+` → one or more
* `*` → zero or more
* `?` → optional
* `(...)` → capture group
* `|` → OR (choice)

### Escaping special characters

* `\.` → literal dot

---

## Regex Examples from the Lab

### Match a word

```python
pattern = r"cat"
text = "The cat sat"
re.findall(pattern, text)   # ['cat']
```

### Match digits

```python
pattern = r"\d+"
text = "Order 123 placed"
re.findall(pattern, text)   # ['123']
```

### Match words

```python
pattern = r"[A-Za-z]+"
text = "Hello 123 World"
re.findall(pattern, text)   # ['Hello', 'World']
```

### Match IP addresses (basic)

```python
pattern = r"\d+\.\d+\.\d+\.\d+"
text = "Login from 192.168.0.1"
re.findall(pattern, text)   # ['192.168.0.1']
```

### Match usernames in auth.log

```python
pattern = r"for (?:invalid user )?(\S+) from"
line = "Failed password for invalid user bob from 10.0.0.5"
re.search(pattern, line).group(1)   # 'bob'
```

---

## Useful Python Functions

* `print()` → display output
* `sorted()` → sort a list or set
* `set()` → remove duplicates
* `list.append(item)` → add item to a list
* `str.strip()` → remove whitespace/newlines
* `str.upper()` → convert to uppercase

---

## Typical Workflow for Log Analysis

1. **Open and read file** → `with open('auth.log', 'r') as f:`
2. **Iterate over lines** → `for line in f:`
3. **Apply regex** → `re.findall(ip_pattern, line)`
4. **Store matches** in a list
5. **Convert to set** for uniqueness
6. **Print or save** results to file

---

This cheat sheet is your quick reference when completing Lab 1.1 or similar tasks in Python.
