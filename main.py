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
    
    response=client.models.generate_content(
    model="gemini-2.5-flash",
    contents="generate a single scary introductory line for the boss ,keep it less than 25 words",
    config={
        "temperature":0.8
        }
    )

    response_boss=client.models.generate_content(
                model="gemini-2.5-flash",
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
        attack_name=""
        
        print(f"battle running.. boss hp:{boss_hp} | player hp:{player_hp}")
       
        print("Choose Player Attack: 1. Slash Attack 2. Strike Attack 3. Magic Attack 4. Defense Move")
        choice=int(input("Enter your choice: "))
        
        if choice==1:
            attack_name="Slash Attack"
        elif choice==2:
            attack_name="Strike Attack"
        elif choice==3:
            attack_name="Magic Attack"
        elif choice==4:
            attack_name="Defense Move"
        else:
            print("Invalid choice, missed the attack!!")
        
        response_player_turn=client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"Generate a  fantasy narration for a hero using {attack_name}, to attack the boss to save his city, keep it less than 20 words",
        config={
            "temperature":0.7,
            "max_output_tokens": 100,
        }  
        )
        print(response_player_turn.text) 
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

        print("Boss attacking the player\n")
        choice=random.randint(1,4)

        if choice==1:
            attack_name="Slash Attack"
        elif choice==2:
            attack_name="Strike Attack"
        elif choice==3:
            attack_name="Magic Attack"
        elif choice==4:
            attack_name="Defense Move"
        
        response_boss_turn=client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Generate a dark fantasy narration for a boss using {attack_name}, to attack the hero, keep it less than 20 words",
        config={
            "temperature":0.8,
            "max_output_tokens": 100,
        }
        )
        print(response_boss_turn.text)
        #Attack mechanics of boss
        if choice==1:
            player_hp=player_hp-slash_attack
        elif choice==2:
            player_hp=player_hp-strike_attack
        elif choice==3:
            player_hp=player_hp-magic_attack
        elif choice==4:
            boss_hp=boss_hp+defense_move

        boss_hp=max(boss_hp,0)
        player_hp=max(player_hp,0)
        
        #boss/player victory narration
        if boss_hp==0:
            print("battle ended... player wins!!")
            print("player's final words: ...",response_player.text)
        
        elif player_hp==0:        
            print("battle ended... boss wins!!")
            print("Boss's final words:  ...",response_boss.text)

    #print("battle ended... player wins!!")
if __name__=="__main__":
    main()