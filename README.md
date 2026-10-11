# Score-Getter

A python script for getting current scores of college football games. Will eventually tie into home assistant.
Currently, it fetches the games for that day, and then tracks those games over minute intervals. 

#### Eventual Features

Eventually, it will make this data available to home assistant, move to 15 second intervals, and go to the espn scoreboard method for updating scores. 
It will also display visual for where the ball is, who has it, and a gameclock (basically the espn boxscore but in terminal)

Relies heavily on the [Public ESPN Api](https://github.com/pseudo-r/Public-ESPN-API).

### LLM Disclosure

A local LLM (Qwen 3.5 9B) was used for help finding libraries, commenting, and generating API requests

