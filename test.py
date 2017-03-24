request = "hello world"
b = None
a = None
for i in range(len(request)):
    if request[i] == " ":
        a = request[:i]
        b = request[i+1 :]
print(b)