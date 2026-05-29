import os
import random
from dotenv import load_dotenv
from google import genai
load_dotenv()
client=genai.Client()

def main():
    boss_flag_2=False
    boss_flag=False
    boss_hp=100
    player_hp=85
    slash_attack=10
    strike_attack=13
    magic_attack=15
    defense_move=5 #if defense employed, player hp will increse by 5
    Death_hell_fire=18 #special attack of the boss, which activates when boss hp is less than 30.
    battle_history=[
        {
        "role":"user",
        "parts":[{"text": """You are a cinematic dark fantasy battle narrator.

         Narrate:
        - the heroic prince,whois fighting to save his kingdom from the clutches of darkness.
        - the ancient evil boss who is an evil arrogant being with immense power.

         Keep narration dramatic and under 30 words.."""}]
        }
    ]
    
    response=client.models.generate_content(
    model="gemini-2.5-flash",
    contents="generate a single scary introductory line for the boss ,keep it less than 25 words",
    config={
        "temperature":0.8
        }
    )

    print("Boss Introduction: ",response.text)
    print("battle start..\\n")
    print("player attacking the viscious boss\\n")

    while(boss_hp >0 and player_hp >0):
        player_attack_name=""

        print(f"battle running.. boss hp:{boss_hp} | player hp:{player_hp}")
        print("Choose Player Attack: 1. Slash Attack 2. Strike Attack 3. Magic Attack 4. Defense Move")
        try:
            choice=int(input("Enter your choice: "))
        except ValueError:
            print("please enter a valid integer between 1 to 4")
            continue

        if choice==1:
            player_attack_name="Slash Attack"
            boss_hp=boss_hp-slash_attack
        elif choice==2:
            player_attack_name="Strike Attack"
            boss_hp=boss_hp-strike_attack
        elif choice==3:
            player_attack_name="Magic Attack"
            boss_hp=boss_hp-magic_attack
        elif choice==4:
            player_attack_name="Defense Move"
            player_hp=player_hp+defense_move
        else:
            print("Invalid choice, missed the attack!!")
            continue

        boss_hp=max(boss_hp,0)

        if(boss_hp==0):
            print("battle ended... player wins!!")
            victory_response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents="Generate a heroic victory line for the player who is a prince after defeating the evil demon boss.",
                config={
                    "temperature":0.8,
                }
            )
            print("player's final words: ...",victory_response.text)
            break

        boss_emotion=""
        if(boss_hp<30):
            boss_emotion="enraged"
        elif(boss_hp>=30 and boss_hp<70):
            boss_emotion="annoyed"
        elif(boss_hp>=70):
            boss_emotion="arrogant"

        boss_attack_name=""
        print("Boss attacking the player\\n")

        if(boss_hp>30):
            bchoice=random.randint(1,4)
        else:
            bchoice=random.randint(1,5)

        if bchoice==1:
            boss_attack_name="Slash Attack"
            player_hp=player_hp-slash_attack
        elif bchoice==2:
            boss_attack_name="Strike Attack"
            player_hp=player_hp-strike_attack
        elif bchoice==3:
            boss_attack_name="Magic Attack"
            player_hp=player_hp-magic_attack
        elif bchoice==4:
            boss_attack_name="Defense Move"
            boss_hp=boss_hp+defense_move
        elif bchoice==5:
            boss_attack_name="Death Hell Fire"
            player_hp= player_hp-Death_hell_fire
            boss_hp=boss_hp+defense_move

        battle_history.append({
            "role":"user",
            "parts":[{"text": f"""the hero used {player_attack_name} attack against the boss. boss is now {boss_hp} hp.
                      villian boss used {boss_attack_name} against the hero.
                      current mental state of the boss is : {boss_emotion}.if boss hp is below 31, make him more enraged and annoyed.
                      hero hp : {player_hp},
                      narrate this combat turn dramatically."""}]
        })

        narration_response = None
        if boss_hp<30 and boss_flag==False:
            boss_flag=True
            print("BOSS ENTERED PHASE 2!!")
            print(f"""=== THE ABYSS LORD ENTERS PHASE 2 ===

Dark flames erupt from the boss...
His armor cracks...
His eyes glow crimson...\n""")

        if(boss_attack_name=="Death Hell Fire"):
            narration_response=client.models.generate_content(
                model='gemini-2.5-flash',
                contents=battle_history,
                config={"temperature":0.9,}
            )
            print(narration_response.text)

        elif boss_hp<30 and boss_flag_2==False:
            narration_response=client.models.generate_content(
                model='gemini-2.5-flash',
                contents=battle_history,
                config={"temperature":0.9,}
            )
            print(narration_response.text)
            boss_flag_2=True;

        elif(player_hp<30):
            narration_response=client.models.generate_content(
                model='gemini-2.5-flash',
                contents=battle_history,
                config={"temperature":0.9,}
            )
            print(narration_response.text)

        else:
            print(f"\n Player used {player_attack_name} and boss used {boss_attack_name} \n")

        if narration_response is not None:
            battle_history.append({
                "role":"model",
                "parts":[{"text": narration_response.text}]
            })

        battle_history=battle_history[-12:]

        boss_hp=max(boss_hp,0)
        player_hp=max(player_hp,0)

        if player_hp==0:
            loose_response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents="generate a single line for the defeated prince hero. keep it under 30 words.",
                config={
                    "temperature":0.8,
                }
            )
            print("\nbattle ended... boss wins!!")
            print("Boss's final words:  ...",loose_response.text)
            break

        

if __name__=="__main__":
    main()

