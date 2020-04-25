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