import json

# Save File
# data = {
#     'Germany' : 'Berlin',
#     'UK' : 'London',
#     'China' : 'Beijing',
#     'Gato' : '123' }
# with open('test_data.txt', 'w') as test_file:
#     json.dump(data, test_file)


# Load File =========================================
with open('test_data.txt') as test_file:
    data = json.load(test_file)
    # print info file
    for entry in data.items():
        print(entry)
