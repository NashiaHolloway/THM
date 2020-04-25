# Scripting

## Intro to Python
Challenge:

Decode a .txt file: 5 times encoded using base16, 5 times encoded using base32, 5 times encoded using base64.

```python
import base64

# open file
file = open("encodedflag.txt", "r+")

string_to_decode = file.read()

# Loop through decoding in base16 (5x), base32 (5x), base64 (5x)

# base16
for i in range (0, 5, 1):
    string_to_decode = base64.b16decode(string_to_decode)
    print(string_to_decode)
# base32
for i in range (0, 5, 1):
    string_to_decode = base64.b32decode(string_to_decode)
    print(string_to_decode)
# base64
for i in range (0, 5, 1):
    string_to_decode = base64.b64decode(string_to_decode)
    print(string_to_decode)

# close file
file.close()
```

## Scripting
1. This file has been base64 encoded 50 times - write a script to retrieve the flag

### Python
```python
import base64

# open file
file = open("b64.txt", "r")

string_to_decode = file.read()

# loop through 50 times, decoding
for i in range(0, 50, 1):
    string_to_decode = base64.b64decode(string_to_decode)

print(string_to_decode)
```

2. You need to write a script that connects to the webserver on the correct port, do an operation on a number and then move onto the next port. Start your original number at 0.

```python

```

3. 

```python 

```

### Resources

[python base64 decode](https://stackoverflow.com/questions/3470546/python-base64-data-decode)

[python socket programming](https://docs.python.org/3/howto/sockets.html)