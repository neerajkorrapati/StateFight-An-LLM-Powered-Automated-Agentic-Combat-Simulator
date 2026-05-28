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
        print(f"battle running.. boss hp:{boss_hp} | player hp:{player_hp}")
       
        print("Choose Player Attack: 1. Slash Attack 2. Strike Attack 3. Magic Attack 4. Defense Move")
        choice=int(input("Enter your choice: "))
        if choice==1:
            print("You used a Slash Attack!\n")
            boss_hp=boss_hp-slash_attack
        elif choice==2:
            print("You used a Strike Attack!\n")
            boss_hp=boss_hp-strike_attack
        elif choice==3:
            print("You used a Magic Attack!\n")
            boss_hp=boss_hp-magic_attack
        elif choice==4:
            print("heh, you used defense\n")
            player_hp=player_hp+defense_move
        else:
            print("Invalid choice")
        print("Boss attacking the player\n")
        choice=random.randint(1,4)
        if choice==1:
            print("Boss used a Slash Attack!\n")
            player_hp=player_hp-slash_attack
        elif choice==2:
            print("Boss used a Strike Attack!\n")
            player_hp=player_hp-strike_attack
        elif choice==3:
            print("Boss used a Magic Attack!\n")
            player_hp=player_hp-magic_attack
        elif choice==4:
            print("Boss used defense\n")
            boss_hp=boss_hp+defense_move
        
        boss_hp=max(boss_hp,0)
        player_hp=max(player_hp,0)
        if boss_hp==0:
            print("battle ended... player wins!!")
            print("player's final words: ...",response_player.text)
        elif player_hp==0:
        
            print("battle ended... boss wins!!")
            print("Boss's final words:  ...",response_boss.text)

    #print("battle ended... player wins!!")
if __name__=="__main__":
    main()