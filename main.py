import os
import random
from dotenv import load_dotenv
from google import genai
load_dotenv()
client=genai.Client()

def main():
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
    #remove player and boss history, replace it with battle history
    
    response=client.models.generate_content(
    model="gemini-2.0-flash",
    contents="generate a single scary introductory line for the boss ,keep it less than 25 words",
    config={
        "temperature":0.8
        }
    )
    
 #we can remove responser_player and response_boss, replacing it with a single api call.
      #========================BOSS INTRODUCTION=========================================  
    print("Boss Introduction: ",response.text)
 
    print("battle start..\n")

    print("player attacking the viscious boss\n")
    #=============MAIN LOOP================
    while(boss_hp >0 and player_hp >0):
        player_attack_name=""
        
        print(f"battle running.. boss hp:{boss_hp} | player hp:{player_hp}")
       
        print("Choose Player Attack: 1. Slash Attack 2. Strike Attack 3. Magic Attack 4. Defense Move")
        choice=int(input("Enter your choice: "))
        
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
        #replace this response_player_turn by appending hitory to it            
        
        boss_hp=max(boss_hp,0)
        if(boss_hp==0):
            print("battle ended... player wins!!")
            victory_response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"Generate a herioc victory line for the player who is a princeafter defeating the evil demon boss who was a threat to the kingdom. keep it under 30 words.",
                config={
                    "temperature":0.8,
                    "max_output_tokens":100,
                }
            )
            print("player's final words: ...",victory_response.text)
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
            boss_hp=boss_hp+defense_move #when boss uses special attack, it also
        
        #removed boss_turn_api_call, instead we use a single API call.
        battle_history.append({
            "role":"user",
            "parts":[{"text": f"""the hero used {player_attack_name} attack against the boss. boss is now {boss_hp}. 
                      villian boss used {boss_attack_name} against the hero.
                      current mental state of the boss is : {boss_emotion}.
                      hero hp : {player_hp},
                      narrate this combat turn dramatically adding boss's current emotion to affect the narration.keep it under 25 words for each character."""}]
        })
        
        #to further reduce api calls, call the ai only when something interesting happens.
        if(boss_attack_name=="Death Hell Fire"):
          narration_response=client.models.generate_content(
            model='gemini-2.5-flash',
            contents=battle_history,
            config={
                "temperature":0.9,
                "max_output_tokens": 100,
            }
        )
          print(narration_response.text)
        elif(boss_hp<30):
          narration_response=client.models.generate_content(
            model='gemini-2.5-flash',
            contents=battle_history,
            config={
                "temperature":0.9,
                "max_output_tokens": 100,
            }
        )
        elif(player_hp<30):
              narration_response=client.models.generate_content(
                model='gemini-2.5-flash',
                contents=battle_history,
                config={
                 "temperature":0.9,
                 "max_output_tokens": 100,
                })
              print(narration_response.text)    
        else:                
            print(f" Player used {player_attack_name} and boss used {boss_attack_name} ")

        # immidietly after generating boss response, we will save it into the boss's history.
        battle_history.append({
            "role":"model",
            "parts":[{
                "text": narration_response.text
            }]
        })
        #memory trimming, to efficiently make use of credits nd load
        battle_history=battle_history[-12:]
        #Attack mechanics of boss, changed back to above config.

        boss_hp=max(boss_hp,0)
        player_hp=max(player_hp,0)
        
        
        #boss/player victory narration
        if boss_hp==0:
            print("battle ended... player wins!!")
            print("player's final words: ...",victory_response.text)
        
        elif player_hp==0:     
               loose_response=client.models.generate_content(
               model="gemini-2.5-flash",
               contents=f"generate a single line for the player who is a hero, after being defeated by the boss who was a threat to the kingdom.(the player is a prince). keep it under 30 words and scary.",
               config={
                "temperature":0.8,
                "max_output_tokens":100,
            }
        )   
               print("battle ended... boss wins!!")
               print("Boss's final words:  ...",loose_response.text)
        if boss_hp<30 and boss_flag==False:
            boss_flag=True        
            print("BOSS ENTERED PHASE 2!!")
            

    #print("battle ended... player wins!!")
if __name__=="__main__":
    main()
     
