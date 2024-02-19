# Hawkeye - Multimodal Interaction Robot

[![Watch the video](https://github.com/darryltanzil/spot-boston-dynamics/assets/5387769/54f19158-6752-4d41-ad5a-896e53d35a31)](https://www.youtube.com/watch?v=PDaMZ3OyuGc)

Hawkeye is a real time multimodal conversation and interaction agent for the Boston Dynamics’ mobile robot Spot. Leveraging OpenAI’s experimental GPT-4 Turbo and Vision AI models, Hawkeye aims to empower everyone, from seniors to healthcare professionals in forming new and unique interactions with the world around them. 

## What it does
The core of Hawkeye is powered by its conversation-action engine. Using audio and visual inputs from the real world, all decisions and movements made by Hawkeye are generated and inferenced on the fly in near real time. For instance, when faced with a command like "Hey Spot, can you move a little closer?” Hawkeye digests the task on hand to build step-by-step instructions for the robot to follow. This means that Hawkeye is able to dynamically adapt, change, and learn with new environments. It knows when and how to improve its vantage point, orchestrate complex maneuvers, and advance closer to its target. Hawkeye flawlessly navigates through any environment, all while avoiding a reliance on pre-coded movement patterns.

## How we built it

Hawkeye is powered by OpenAI's experimental GPT-4 Turbo and Vision AI models, alongside Spot’s movement SDK. On initialization, Hawkeye uses speech-to-text to wait for an interaction from the user, where it then determines the type and intention of the request. Then, relevant information is fed into OpenAI’s GPT4-Turbo and Vision to generate a chain of command for the robot to follow, with the ability to map out its actions and navigate to the goal. Incrementally, Hawkeye reevaluates and replans its movements to eventually reach its intended goal. 

## Challenges we ran into
Our main challenge with developing on the Spot is finding ways to rapidly build and prototype new features without having to rebuild the entire project on every change. As such, we developed a custom command server to push to push, patch, and deploy new code over websockets without needing a reboot. This rapidly increased our rate of innovation with the Spot robot, giving us the flexibility and maneuverability to make our project a reality.
Another main challenge was determining what kind of command a phrase is when it’s first received from the mic. Since there are “movement”, “image processing”, and “general commands”, all with their own functionality, it was difficult coming up with a simple way to classify each command to be one of the three. We resolved this by creating an input delegate which makes an API call to OpenAI, and makes a judgment on what classification it thinks the command is.

## Accomplishments that we're proud of
Learning how to engineer prompts and rapidly iterate to make it more accurate was a feat that we're proud of! The learning curve for Spot's SDK was quite steep and we're happy to have come out of it with minimal team friction. We also got it to dance in the last hour by just telling it to dance, which was very satisfying. Not breaking the $75k robot was relieving as well!

## What we learned
By using Spot's and its SDK, we worked with a lot of hardware which we otherwise would never have access to. We learnt a lot about the physical sensors and I/O onboard. Moreover, it was the first time working with facial and object recognition libraries for a lot of us. Finally, we became much more proficient with GPT APIs.

## What's next for Hawkeye
Looking ahead, we envision further refining Hawkeye by incorporating dynamic object tracking along with facial recognition tech to improve the breadth of human-assistance tasks. This would allow it to dynamically change its motion to avoid moving obstacles (e.g., people in a moving crowd). Spot has huge potential as a guide dog once combined with AI, being able to talk to and guide its owner — with Hawkeye’s interaction software, we believe this level of robotics collaboration will shape the future.

## Technologies Used
* Spot® - The Agile Mobile Robot
* Spot SDK for control over hardware
* Websockets for our dynamic code launcher
* Python as language of choice
* Docker for easy containerization
* GPT-4's vision & turbo preview models


## Gallery
<img width="545" alt="image" src="https://github.com/darryltanzil/spot-boston-dynamics/assets/5387769/cdf53bf4-1ad2-40d3-9717-0880b02d24f3">

Boston Dynamics Robot with Speakers & Webcam attached

![image](https://github.com/darryltanzil/spot-boston-dynamics/assets/5387769/a18ae56c-429d-48d2-a604-e42640652cad)
Initial Sketches for Software
