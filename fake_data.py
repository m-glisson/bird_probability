import random

LOCATIONS = ['MD', 'PA'] # How many different locations you want to break up to
NUMBER_BIRDS = 15    # How many birds do you have recorded? 
SONG_LENGTH_MIN = 15 # Length of the shortest song
SONG_LENGTH_MAX = 30 # Length of the longest song
NUMBER_SYL = 15       # How many Syllable's you have identified

example = {
    "bird": 'bird num 1', 
    "location": "MD", 
    "song" : [
        1, 3, 5, 4, 4, 2, 1
    ]
}


def pick_state(): 
    return random.choice(LOCATIONS)

def sounds_array(number_sounds): 
    return [str(x) for x in list(range(1, number_sounds))]

def make_song(min_len, max_len, sylls):
    arr_len = random.randint(min_len, max_len)
    song_array = []
    for i in range(0, arr_len): 
        song_array.append(random.choice(sylls))

    return song_array



sounds = sounds_array(NUMBER_SYL)



rows = []
for i in range(0,NUMBER_BIRDS):
    bird = {
        'name': f"bird{i}", 
        'location': pick_state(), 
        'song': make_song(SONG_LENGTH_MIN,SONG_LENGTH_MAX,sounds)
    }
    rows.append(bird)

with open('test.csv', 'w') as f:
    f.write("%s,%s,%s\n"%('name', 'location', 'song'))
    for row in rows: 
        f.write("%s,%s,%s\n"%(row['name'],row['location'],','.join(row['song'])))
