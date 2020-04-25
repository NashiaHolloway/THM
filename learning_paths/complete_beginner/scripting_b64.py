import base64

# open file
file = open("b64.txt", "r")

string_to_decode = file.read()

# loop through 50 times, decoding
for i in range(0, 50, 1):
    string_to_decode = base64.b64decode(string_to_decode)

print(string_to_decode)