import sys

digit_string = sys.argv[1]
string_sum = 0

for i in digit_string[:]:
    string_sum += int(i)

print(string_sum)
