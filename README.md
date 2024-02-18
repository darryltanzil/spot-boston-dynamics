# Boston Dynamics "Hawkeye" Robot

For Stanford's TreeHacks 2024, we created Boston Dynamics software which uses object & face recognition combined with Open AI's vision and turbo preview AI models to allow seniors and the visually impaired to read signage they wouldn't be able to otherwise.

## What it does
The user states "Hey Spot, can you move a little closer?" and Spot, the dynamic robot comes towards them. Spot acts as the user's eyes, analyzing the environment through a series of snapshots and software which determines whether to move closer and rotate its head in any direction. Once a clear view of the signage/poster is seen, Spot states what the contents of the signage is through the speakers attached on its back.

## How we built it
We used Spot's SDK to figure out basic movement and how to deploy it, creating scripts allowing to send commands to Spot in realtime. With this, we developed Python classes which would process audio, make calls to OpenAI's API to classify what type of command it was, and then make subsequent calls to any of the three: move Spot, have Spot respond with what signage it's looking at, or answer a general GPT requirement. Spot determines what signage it's looking at by screenshotting its current view, converting it into a base64 encoded image, and sending it to the vision model, and recieving a response afterward. To ensure that the signage is as accurate as possible

## Challenges we ran into
(Sriram -- edit if the technical terms in this are inaccurate) We started our project by trying to dynamically run movement commands on Spot via a reverse shell. We were using sockets, which didn't work out for hours and we had no idea why -- didn't help that the internet was out either. We eventually figured out that Nginx was shutting us out on Spot's end, after which we spent some time switching to an implementation which used websockets. We were worried that we'd have to abandon the project throughout, so it was a rough couple hours.
There was also a slight scare when we initially thought DNS wasn't available for code running on Spot's hardware. 

## Accomplishments that we're proud of
Learning how to engineer prompts and rapidly iterate to make it more accurate was a feat that we're proud of!

## What we learned

## What's next for Boston Dynamics "Hawkeye" Robot

## Technologies Used
* Spot® - The Agile Mobile Robot
* Spot SDK for control over hardware
* Websockets for facial recognition
* Ngrok for passing in websocket data
* Python as language of choice
* Docker for easy containerization
* GPT-4's vision & turbo preview models
* JSON for an intermediary data transfer format

