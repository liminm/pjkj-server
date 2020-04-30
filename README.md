AI project game server
======================

This is the backend for the 2020 AI tournament at the TU Berlin AOT.

To run, simply call `python3 src/main.py`.

# Storage Setup

## How to setup Docker the first time
`sudo docker pull mongo  // just download the image
sudo docker run --name mongoDB -p 27017:27017 -d mongo // run the image`

After that MongoDB will run and not shutdown if its not explicitly told so, even after a restart it will automatically start again

To get an overview over all running container type
`sudo docker ps `


## How to use the dictionary

### How to connect to the storage module
`from storage.DatabaseDictionary import DatabaseDictionary
storage = DatabaseDictionary()`

### How to save something
`key = 'insert your key here'
game = {
    'player1': 'Lorenz',
    'player2': 'Matthias',
    'history': [
        {'FEN': '8/123/8a...', 'time_player': 1, ...},
        {'FEN': '8/123/8a...', 'time_player': 1, ...},
        ...
    ]
}
storage[key] = game`

### How to read something
`game = storage['key']`

### How to iterate over all entries
`for key in storage:
    game = storage[key]`

## Important Information
- The module only accepts String keys, if not a type error will be raised!
- The values must be convertable to json if its not there will occur errors which are not handled yet!