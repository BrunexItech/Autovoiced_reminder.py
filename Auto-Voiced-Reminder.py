# To run the following code kindly install the following in your virtual environment
#gtts
#pygame
#schedule
#python_dateutil
from gtts import gTTS #translates text to speech
import pygame #plays the audio
import schedule # tracking the actual time
import time
import threading
from dateutil import parser #for time conversion

user_name = input("Enter your name: \n")

#Asks the user the time the reminder should signal for daily inputs then converts the time to 24HR clock system
while True:
    time_reminder = input("Enter the time you would wish to be reminded to set up your daily goals:\n"
                          "Use 24hr clock system eg:HH/MM or 12hr system with AM/PM \n")
    try:
        correct_time_reminder = parser.parse(time_reminder).strftime("%H:%M")
        break
    except (TypeError, ValueError):
        print("Invalid Time input! Please enter the correct time format!")

daily_objectives = []
stop_current_audio = None

#Function that can stop the audio when it starts playing
def stopping_audio():
    global stop_current_audio
    while True:
        user_choice = input("Press 's' and then 'Enter' to stop the audio: \n")
        if user_choice == 's':
            stop_current_audio = time.strftime("%H:%M")
            print("The audio reminder stopped!")

#Function converts the daily objectives from text to sound
def daily_task():
    global daily_objectives, stop_current_audio
    try:
        objective = f"Hello {user_name}, do you have any daily plans or objectives for the day?"
        tts = gTTS(objective, lang="en")
        tts.save("text_sound.mp3")

        pygame.mixer.init()
        pygame.mixer.music.load("text_sound.mp3")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy(): # allows the music to finish playing
            pygame.time.Clock().tick(5)

        while True: #allows user to re_enter the code after selecting the wrong choice
            user_response = input("Do you have any goals or plans for the day? (yes/no) \n").lower()
            if user_response == "yes":
                while True:
                    day_objective = input("Enter your daily objectives or type 'done' to finish the process \n").lower()
                    if day_objective == "done":
                        break

                    while True:
                        objective_time = input(
                            "Enter the time for this objective; \n Use 24hr clock system eg HH/MM or 12hr clock system in AM/PM: \n")
                        try:
                            parsed_time = parser.parse(objective_time).strftime("%H:%M")
                            daily_objectives.append({"Objective": day_objective.capitalize(), "Time": parsed_time})
                            break
                        except (ValueError, TypeError):
                            print("Invalid input! Please enter the correct time format!")
                break

            elif user_response == "no":
                print("Thank you for your feedback!")
                exit(0)

            else:
                print("Invalid input! Please enter a yes or no.")


        print("\nYour daily objectives are as follows:")
        print("-" * 30)

        for i, obj in enumerate(daily_objectives, start=1):
            print(f"{i}. Objective: {obj['Objective']} , Time: {obj['Time']}")

        #allows the current audio to continue playing while waiting for the user's prompt
        threading.Thread(target=stopping_audio, daemon=True).start()

        while True: # loops checks if the current time matches with user's time for the task
            current_time = time.strftime("%H:%M")
            for i, obj in enumerate(daily_objectives, start=1):
                try:
                    parsed_time = parser.parse(obj["Time"]).strftime("%H:%M")
                    if obj["Time"] == current_time and obj["Time"] != stop_current_audio:
                        # Reading the printed objectives
                        tts = gTTS(obj["Objective"], lang="en")
                        tts.save(f"Objective {i}.mp3")
                        pygame.mixer.music.load(f"Objective {i}.mp3")
                        pygame.mixer.music.play()

                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)

                except (ValueError, TypeError):
                    print("Invalid Time input! Please enter the correct format!")

    except Exception as e:
        print(f"An error occurred: {e}!")

schedule.every().day.at(correct_time_reminder).do(daily_task)

while True:
    schedule.run_pending()
    time.sleep(1)
