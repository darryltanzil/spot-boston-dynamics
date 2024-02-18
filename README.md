# Boston Dynamics "Hawkeye" Robot

For Stanford's TreeHacks 2024, we created software for Boston Dynamics' Spot. It leverages object & face recognition combined with Open AI's GPT4 for Vision and turbo preview AI models to allow seniors and the visually impaired to read signage they wouldn't be able to otherwise. 

## What it does
The user states "Hey Spot, can you move a little closer?" and Spot, the dynamic robot, comes towards them. Spot acts as the user's eyes, analyzing the environment through a series of snapshots and software which determines whether to move closer and/or rotate its head in any direction. When the user asks what some given signage says, Spot states what the content of the signage is through the speakers attached on its back. If the signage is too blurry or far away, Spot will move closer until it isn't. It can also combine complicated, ambiguous series of movements seamlessly without using any hardcoded movements. 

## How we built it
We used Spot's SDK to figure out basic movement and how to deploy it, creating scripts allowing us to send commands to Spot in realtime. With this, we developed Python classes which would process audio, make calls to OpenAI's API to classify what type of command it was, and then make subsequent calls. This would result in the most appropriate response between moving Spot, having Spot respond with what signage it's looking at, or answering a general GPT requirement -- all on the fly. Spot determines what signage it's looking at by screenshotting its current view, converting it into a base64 encoded image, sending it to the vision model, and recieving a response afterward. This response would contain the contents of the image if the model was capable of reading it, or it would contain the directions that Spot would need to move in to be able to read it clearly. 
As the project progressed and we had more time on our hands, we implemented complex chains of movements by allowing GPT to dynamically interpret whatever series of complex instructions were said to Spot. 

## Challenges we ran into
We started our project by trying to dynamically run movement commands on Spot via a reverse shell. We were using sockets, which didn't work out for hours and we had no idea why -- didn't help that the internet was out either. We eventually figured out that Nginx was shutting us out on Spot's end, after which we spent some time switching to an implementation which used websockets. We were worried that we'd have to abandon the project throughout, so it was a rough couple hours.
There was also a slight scare when we initially thought DNS wasn't available for code running on Spot's hardware. Finally, we had a couple last-minute hiccups. GPT was reading some images wrongly, the microphone on Spot wasn't working as intended, and prompt chaining wasn't working perfectly due to an issue on Spot's end. 

## Accomplishments that we're proud of
Learning how to engineer prompts and rapidly iterate to make it more accurate was a feat that we're proud of! The learning curve for Spot's SDK was quite steep and we're happy to have come out of it with minimal team friction. We also got it to dance in the last hour by just telling it to dance, which was very satisfying. Not breaking the $75k robot was relieving as well!

## What we learned
By using Spot's and its SDK, we worked with a lot of hardware which we otherwise would never have access to. We learnt a lot about the physical sensors and I/O onboard. Moreover, it was the first time working with facial and object recognition libraries for a lot of us. Finally, we became much more proficient with GPT APIs.

## What's next for Boston Dynamics "Hawkeye" Robot
We believe that we could've used Spot to its full potential if we had more time. We could've implemented facial recognition, memory and object tracking properly. This would've allowed it to dynamically change its motion to avoid moving obstacles (eg. people in a moving crowd). When combined with AI with all of these features, we think that Spot has huge potential as a guide dog. 

## Technologies Used
* Spot® - The Agile Mobile Robot
* Spot SDK for control over hardware
* Websockets for facial recognition
* Ngrok for passing in websocket data
* Python as language of choice
* Docker for easy containerization
* GPT-4's vision & turbo preview models
* JSON for an intermediary data transfer format
* Implementation as a guard dog


## Gallery
<img width="545" alt="image" src="https://github.com/darryltanzil/spot-boston-dynamics/assets/5387769/cdf53bf4-1ad2-40d3-9717-0880b02d24f3">

Boston Dynamics Robot with Speakers & Webcam attached

![image](https://github.com/darryltanzil/spot-boston-dynamics/assets/5387769/a18ae56c-429d-48d2-a604-e42640652cad)
Initial Sketches for Software


