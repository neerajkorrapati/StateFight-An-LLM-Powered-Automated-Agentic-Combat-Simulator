import os
import random
from dotenv import load_dotenv
from google import genai
load_dotenv()
client=genai.Client()

def main():

    boss_hp=100
    player_hp=85
    slash_attack=10
    strike_attack=13
    magic_attack=15
    defense_move=5 #if defense employed, player hp will increse by 5
    Death_hell_fire=18 #special attack of the boss, which activates when boss hp is less than 30.
    boss_history=[
        {
        "role":"user",
        "parts":[{"text": """You are an ancient dark fantasy boss.
        You are fighting a prince hero.
        Speak aggressively and dramatically.
        Mock the player often.
        Keep responses under 20 words."""}]
        }
    ]
    player_history=[
        {
        "role":"user",
        "parts":[{"text": """You are a brave prince hero, who is trying to saave his kingdom by defeating the dark fantasy boss.
        Speak heroically and dramatically.
        Keep responses under 20 words."""}]
        }
    ]
    
    response=client.models.generate_content(
    model="gemini-2.0-flash",
    contents="generate a single scary introductory line for the boss ,keep it less than 25 words",
    config={
        "temperature":0.8
        }
    )

    response_boss=client.models.generate_content(
                model="gemini-2.0-flash",
                contents="generate  a  fearsome line for the boss after defeating the player who is the hero.add evil laugh and something sadistic in the next line",
                config={
                    "temperature":0.8
                }
            )
    response_player=client.models.generate_content(
                model="gemini-2.5-flash",
                contents="generate a  single heroic line for the player who is a hero, after defeating the boss who was a threat to the kingdom,(the player is a prince).",
                config={
                    "temperature":0.8
                }
            )
    
    
    
    print("Boss Introduction: ",response.text)

    


    print("battle start..\n")
    print("player attacking the viscious boss\n")
    while(boss_hp >0 and player_hp >0):
        player_attack_name=""
        
        print(f"battle running.. boss hp:{boss_hp} | player hp:{player_hp}")
       
        print("Choose Player Attack: 1. Slash Attack 2. Strike Attack 3. Magic Attack 4. Defense Move")
        choice=int(input("Enter your choice: "))
        
        if choice==1:
            player_attack_name="Slash Attack"
        elif choice==2:
            player_attack_name="Strike Attack"
        elif choice==3:
            player_attack_name="Magic Attack"
        elif choice==4:
            player_attack_name="Defense Move"
        else:
            print("Invalid choice, missed the attack!!")
        #replcae this response_player_turn by appending hitory to it
        player_history.append({
            "role":"user",
            "parts":[{"text": f"""the hero used {player_attack_name} attack against the boss. boss is now {boss_hp}. 
                      respond with a heroic fantasy narration."""}]
        })
        response_player_turn=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=player_history,
        config={
            "temperature":0.7,
            "max_output_tokens": 100,
        }  
        )
        print(response_player_turn.text) 

        player_history.append({
            "role":"model",
            "parts":[{
                "text":response_player_turn.text
            }]
        })
        if choice==1:
            boss_hp=boss_hp-slash_attack
        elif choice==2:
            boss_hp=boss_hp-strike_attack
        elif choice==3:
            boss_hp=boss_hp-magic_attack
        elif choice==4:
            player_hp=player_hp+defense_move
            
        
        boss_hp=max(boss_hp,0)
        if(boss_hp==0):
            print("battle ended... player wins!!")
            print("player's final words: ...",response_player.text)
            break
        
      
       #BOSS ATTACKS BACK
        boss_emotion=""
        if(boss_hp<30):
            boss_emotion="enraged"
        elif(boss_hp>=30 and boss_hp<70):
            boss_emotion="annoyed"
        elif(boss_hp>=70):
            boss_emotion="arrogant"
        
        boss_attack_name=""
        print("Boss attacking the player\n")
        if(boss_hp>30):
            bchoice=random.randint(1,4)
        elif(boss_hp<=30):
            bchoice=random.randint(1,5) #this adds an additional layer of depth to the boss fight, unlocks a new stage of the boss        

        if bchoice==1:
            boss_attack_name="Slash Attack"
        elif bchoice==2:
            boss_attack_name="Strike Attack"
        elif bchoice==3:
            boss_attack_name="Magic Attack"
        elif bchoice==4:
            boss_attack_name="Defense Move"
        elif bchoice==5:
            boss_attack_name="Death Hell Fire"
        
        #removed boss_turn_api_call
        boss_history.append({
            "role":"user",
            "parts":[{"text": f"""the hero used {player_attack_name} attack against the boss. boss is now {boss_hp}. 
                      Attack player with {boss_attack_name}. Mock the prince while attaacking.
                      current mental state of the boss is : {boss_emotion}, respond according to the mental state."""}]
        })
        response_boss_turn=client.models.generate_content(
            model='gemini-2.5-flash',
            contents=boss_history,
            config={
                "temperature":0.9,
                "max_output_tokens": 100,
            }
        )
        print(response_boss_turn.text)

        # immidietly after generating boss response, we will save it into the boss's history.
        boss_history.append({
            "role":"model",
            "parts":[{
                "text": response_boss_turn.text
            }]

        })
        #Attack mechanics of boss
        if bchoice==1:
            player_hp=player_hp-slash_attack
        elif bchoice==2:
            player_hp=player_hp-strike_attack
        elif bchoice==3:
            player_hp=player_hp-magic_attack
        elif bchoice==4:
            boss_hp=boss_hp+defense_move
        elif bchoice==5:
            player_hp= player_hp-Death_hell_fire
            boss_hp=boss_hp+defense_move #when boss uses special attack, it also heals itself a bit, making it more challenging for the player.

        boss_hp=max(boss_hp,0)
        player_hp=max(player_hp,0)
        
        #boss/player victory narration
        if boss_hp==0:
            print("battle ended... player wins!!")
            print("player's final words: ...",response_player.text)
        
        elif player_hp==0:        
            print("battle ended... boss wins!!")
            print("Boss's final words:  ...",response_boss.text)
        if boss_hp<30:
            print("===BOSS IS ENRAGED!!===")

    #print("battle ended... player wins!!")
if __name__=="__main__":
    main()
     
