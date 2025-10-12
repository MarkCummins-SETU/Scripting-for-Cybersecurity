# Python at the Command Line Lab

## Learning Outcomes

By the end of this lab, you will be able to:

- Use **interactive Python (`python3 -q`)** as a quick calculation and exploration tool.  
- Execute **one-liner scripts** with `python3 -c` for automation and scripting.  
- Perform **number, encoding, and hashing operations** relevant to cybersecurity.  
- Use Python for **quick random data generation**, **date/time conversions**, and **lightweight network lookups**.  

---

## 1. Getting Started

### Launching Interactive Mode

```bash
python3 -q
```

The -q flag starts Python quietly (without the banner).
You’ll see the >>> prompt.

```bash
>>> 2 + 2
4
>>> exit()
```

### One-Liners with -c

Run small snippets directly:

```bash
python3 -c "print(2 + 2)"
```

Or multiple statements separated by ;:

```bash
python3 -c "import sys; print(sys.version)"
```

### Exercise:
Try printing your username using an environment variable:

```bash
python3 -c "import os; print(os.getenv('USER'))"
```

## 2. Number Systems and Conversion
Hex, Binary, and ASCII

```bash
>>> int('ff', 16)      # hex → decimal
255
>>> hex(255)           # decimal → hex
'0xff'
>>> bin(42)            # decimal → binary
'0b101010'
>>> chr(65)            # ASCII code → character
'A'
>>> ord('A')           # character → ASCII code
65
```

### One-liner equivalents

```bash
python3 -c "print(int('ff',16))"
python3 -c "print(chr(0x41))"
```

### Exercise:

Convert the binary 0b11110000 to decimal.

What is the hex value of ASCII 'Z'?

## 3. Hashing and Encoding
Using hashlib
```bash
>>> import hashlib
>>> hashlib.md5(b"admin").hexdigest()
'21232f297a57a5a743894a0e4a801fc3'
>>> hashlib.sha256(b"password").hexdigest()
'5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'
```

Base64 Encoding
```bash
>>> import base64
>>> base64.b64encode(b"hello")
b'aGVsbG8='
>>> base64.b64decode(b'aGVsbG8=')
b'hello'
```

One-liners
```bash
python3 -c "import hashlib; print(hashlib.sha1(b'cyber').hexdigest())"
python3 -c "import base64; print(base64.b64encode(b'secret').decode())"
```

### Exercise:

Compute the SHA-256 hash of your name.

Base64-encode the word security.

Decode the string ZmxhZ19pc19saWZlCg== — what does it say?

## 4. Randomness and Secrets
Secure Random Values

```bash
>>> import secrets
>>> secrets.token_hex(8)
'7e9d3c5a2f9e4a20'
>>> ''.join(secrets.choice('abcdef0123456789') for _ in range(12))
'e3b4a9d0c2f1'
```

One-liner Password Generator
```bash
python3 -c "import secrets,string; print(''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(12)))"
```

### Exercise:
Generate 5 random 16-character passwords.

## 5. Time and Date Tricks

```bash
>>> import time, datetime
>>> time.time()  # current Unix timestamp
1728745600.23
>>> datetime.datetime.now()
datetime.datetime(2025, 10, 12, 14, 45, 2)
>>> datetime.datetime.fromtimestamp(1700000000)
datetime.datetime(2023, 11, 14, 22, 13, 20)
```

### Exercise:
Convert your birthday to a Unix timestamp.  

Convert 1700000000 back to a readable date.  

## 6. Strings and Bytes
```bash
>>> s = "Cyber"
>>> s.encode()
b'Cyber'
>>> b"Cyber".hex()
'4379626572'
>>> bytes.fromhex('4379626572')
b'Cyber'
```

XOR Trick (CTF Style)
```bash
>>> msg = b'flag'
>>> key = 0x42
>>> bytes([b ^ key for b in msg])
b'&.7'
```

### Exercise:
XOR the bytes of b'secret' with the key 0x10 and observe the result.

## 7. Network and System Utilities
IP and Hostname Tools

```bash
>>> import socket
>>> socket.gethostbyname('example.com')
'93.184.216.34'
```

IP Address Math
```bash
>>> import ipaddress
>>> net = ipaddress.ip_network('192.168.1.0/24')
>>> list(net.hosts())[:3]
[IPv4Address('192.168.1.1'), IPv4Address('192.168.1.2'), IPv4Address('192.168.1.3')]
```

System Info
```bash
>>> import platform
>>> platform.uname()
uname_result(system='Linux', node='labvm', release='6.1.0', version='#1 SMP', machine='x86_64')
```

### Exercise:
Write a one-liner to print your system’s hostname and kernel version.

## 8. Combining Python with Bash

You can mix Bash loops and Python one-liners for automation.

```bash
for word in admin test guest; do
  python3 -c "import hashlib; print('$word ->', hashlib.md5(b'$word').hexdigest())"
done
```

### Exercise:
Adapt the example above to compute SHA256 hashes for a small password list.

## 9. Challenge Zone

Try these mini-projects using only the interactive Python shell or python3 -c:

Convert the hex string 666c61675f69735f68657265 to ASCII.

Compute the SHA1 hash of "CTF2025".

Generate a random 12-character password containing at least one symbol.

Find the IP of picoctf.com

Create a one-liner that prints the current date and time in ISO format.

## TL;DR

| Task          | Interactive Example                | One-liner Example                                                       |
| ------------- | ---------------------------------- | ----------------------------------------------------------------------- |
| Hex → Dec     | `int('ff',16)`                     | `python3 -c "print(int('ff',16))"`                                      |
| Base64 Encode | `base64.b64encode(b'data')`        | `python3 -c "import base64; print(base64.b64encode(b'data').decode())"` |
| MD5 Hash      | `hashlib.md5(b'data').hexdigest()` | `python3 -c "import hashlib; print(hashlib.md5(b'data').hexdigest())"`  |
| Random Token  | `secrets.token_hex(8)`             | `python3 -c "import secrets; print(secrets.token_hex(8))"`              |
| Unix Time     | `time.time()`                      | `python3 -c "import time; print(time.time())"`                          |


---

