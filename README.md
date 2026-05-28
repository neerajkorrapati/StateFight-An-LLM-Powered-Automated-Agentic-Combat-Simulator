#A Python turn-based text RPG demonstrating lightweight LLM integration. It features a robust combat state 
machine managed via user CLI inputs and randomized NPC logic. Includes real time string interpolation 
to feed combat context into the `gemini-2.5-flash` model, ensuring dynamic turn narratives while handling 
API rate limits efficiently.


This entire project has been completely SELF-CODED and not 'Vibe-Coded' , to better understand the understanding and implementation of llm's, so bear with me if you do find any silly errors.
its a simple application of llm's and uses it to emulate a boss fight , similar to that in a video game.
Goal:
is to use two different Api's, to create a narration, and converse them with each other.
Main Principle:
It uses the two different api's , within the same while loop, 
there-by they converse with each other without our intereferece, similar to that of a video game.
