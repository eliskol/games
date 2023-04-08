import pickle
bruh = {'amongus': 'sus', 'bruh': 'moment'}
with open('data.pickle', 'wb') as f:
    pickle.dump(bruh, f, pickle.HIGHEST_PROTOCOL)

with open('data.pickle', 'rb') as f:
    bruh2 = pickle.load(f)

print(bruh2)