# Boston Dynamics Senior Companion

For Stanford's TreeHacks 2024, we created Boston Dynamics software which uses object & face recognition combined with Open AI's artificial intelligence to allow seniors and the visually impaired to read signage they wouldn't be able to otherwise.

## What it does
The user states "Hey Spot, can you move a little closer?" and Spot, the dynamic robot comes towards him. Spot acts as the user's eyes, analyzing the environment through a series of snapshots and software which determines whether to move closer and rotate its head in any direction. Once a clear view of the signage/poster is seen, Spot states what the contents of the signage is through the speakers attached on its back.

## How we built it

## Challenges we ran into
There were some intermittent internet connections and a slight scare when we initially thought DNS wasn't available for code running on Spot's hardware. 
## Accomplishments that we're proud of

## What we learned

## What's next for Boston Dynamics Senior Companion

## Technologies Used
* Spot SDK for control over hardware
* Websockets for facial recognition
* Ngrok for passing in websocket data
* Python as language of choice
* Docker for easy containerization
* GPT-4's vision & turbo preview models
* JSON for an intermediary data transfer format

