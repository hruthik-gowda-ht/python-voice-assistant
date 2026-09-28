import datetime
import os
import webbrowser

import pyttsx3
import speech_recognition as sr
import wikipedia


# ============================================================
# INITIALIZATION
# ============================================================

print("Initializing your voice assistant...")

# Text-to-speech
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")

if voices:
    engine.setProperty("voice", voices[0].id)

engine.setProperty("rate", 175)
engine.setProperty("volume", 1.0)

# Speech recognizer
recognizer = sr.Recognizer()

# Make speech recognition less sensitive to small background noise
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8


# ============================================================
# SPEAK
# ============================================================

def speak(text):
    print("Assistant:", text)

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("Text-to-speech error:", e)


# ============================================================
# GREETING
# ============================================================

def wish_me():

    hour = datetime.datetime.now().hour

    if 0 <= hour < 12:
        greeting = "Good morning!"

    elif 12 <= hour < 18:
        greeting = "Good afternoon!"

    else:
        greeting = "Good evening!"

    speak(greeting)
    speak("I am your voice assistant. How can I help you?")


# ============================================================
# FIND MICROPHONE
# ============================================================

def get_microphone():

    try:

        microphones = sr.Microphone.list_microphone_names()

        if not microphones:
            print("No microphones found.")
            return None

        print("\nAvailable microphones:")

        for index, name in enumerate(microphones):
            print(f"{index}: {name}")

        # Try the system default microphone first
        microphone = sr.Microphone()

        print("\nUsing Windows default microphone.")

        return microphone

    except Exception as e:

        print("Microphone initialization error:", e)

        return None


# ============================================================
# LISTEN
# ============================================================

def take_command():

    microphone = get_microphone()

    if microphone is None:
        speak("I could not find a microphone.")
        return ""

    try:

        with microphone as source:

            print("\nAdjusting microphone for background noise...")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

            print("Microphone ready.")
            print("Listening... Speak now.")

            # Wait at most 5 seconds for speech to begin
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

        print("Recognizing...")

        query = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        print("You said:", query)

        return query.lower()

    except sr.WaitTimeoutError:

        print("No speech detected.")

        return ""

    except sr.UnknownValueError:

        print("Sorry, I could not understand what you said.")

        speak("Sorry, I could not understand you.")

        return ""

    except sr.RequestError as e:

        print("Speech recognition service error:", e)

        speak("Speech recognition service is unavailable.")

        return ""

    except KeyboardInterrupt:

        print("\nProgram stopped by user.")

        return "exit"

    except Exception as e:

        print("Microphone error:", e)

        return ""


# ============================================================
# OPEN WEBSITE
# ============================================================

def open_website(name, url):

    speak(f"Opening {name}")

    try:

        webbrowser.open(url)

    except Exception as e:

        print("Browser error:", e)

        speak(f"I could not open {name}.")


# ============================================================
# WIKIPEDIA SEARCH
# ============================================================

def search_wikipedia(query):

    search_text = query.replace("wikipedia", "").strip()

    if not search_text:

        speak("What should I search on Wikipedia?")

        return

    speak("Searching Wikipedia.")

    try:

        result = wikipedia.summary(
            search_text,
            sentences=2
        )

        print("\nWikipedia result:")
        print(result)

        speak(result)

    except wikipedia.exceptions.DisambiguationError:

        speak(
            "There are multiple results for that topic. "
            "Please be more specific."
        )

    except wikipedia.exceptions.PageError:

        speak("I could not find that topic on Wikipedia.")

    except Exception as e:

        print("Wikipedia error:", e)

        speak("I could not search Wikipedia right now.")


# ============================================================
# PLAY MUSIC
# ============================================================

def play_music():

    music_folder = os.path.expanduser("~/Music")

    if not os.path.exists(music_folder):

        speak("Your Music folder does not exist.")

        return

    try:

        songs = [
            file
            for file in os.listdir(music_folder)
            if file.lower().endswith(
                (".mp3", ".wav", ".m4a", ".aac")
            )
        ]

        if not songs:

            speak("I could not find any music in your Music folder.")

            return

        song = os.path.join(
            music_folder,
            songs[0]
        )

        speak("Playing music.")

        os.startfile(song)

    except Exception as e:

        print("Music error:", e)

        speak("I could not play your music.")


# ============================================================
# PROCESS COMMAND
# ============================================================

def process_query(query):

    query = query.lower().strip()

    if not query:
        return


    # --------------------------------------------------------
    # YOUTUBE
    # --------------------------------------------------------

    if "open youtube" in query or "youtube" == query:

        open_website(
            "YouTube",
            "https://www.youtube.com"
        )


    # --------------------------------------------------------
    # GOOGLE
    # --------------------------------------------------------

    elif "open google" in query:

        open_website(
            "Google",
            "https://www.google.com"
        )


    # --------------------------------------------------------
    # GITHUB
    # --------------------------------------------------------

    elif "open github" in query:

        open_website(
            "GitHub",
            "https://github.com"
        )


    # --------------------------------------------------------
    # LINKEDIN
    # --------------------------------------------------------

    elif "open linkedin" in query:

        open_website(
            "LinkedIn",
            "https://www.linkedin.com"
        )


    # --------------------------------------------------------
    # INSTAGRAM
    # --------------------------------------------------------

    elif "open instagram" in query:

        open_website(
            "Instagram",
            "https://www.instagram.com"
        )


    # --------------------------------------------------------
    # FACEBOOK
    # --------------------------------------------------------

    elif "open facebook" in query:

        open_website(
            "Facebook",
            "https://www.facebook.com"
        )


    # --------------------------------------------------------
    # REDDIT
    # --------------------------------------------------------

    elif "open reddit" in query:

        open_website(
            "Reddit",
            "https://www.reddit.com"
        )


    # --------------------------------------------------------
    # STACK OVERFLOW
    # --------------------------------------------------------

    elif (
        "open stack overflow" in query
        or "open stackoverflow" in query
    ):

        open_website(
            "Stack Overflow",
            "https://stackoverflow.com"
        )


    # --------------------------------------------------------
    # GMAIL
    # --------------------------------------------------------

    elif "open gmail" in query:

        open_website(
            "Gmail",
            "https://mail.google.com"
        )


    # --------------------------------------------------------
    # WIKIPEDIA
    # --------------------------------------------------------

    elif "wikipedia" in query:

        search_wikipedia(query)


    # --------------------------------------------------------
    # TIME
    # --------------------------------------------------------

    elif (
        "what time is it" in query
        or "what is the time" in query
        or query == "time"
        or "tell me the time" in query
    ):

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        speak(
            f"The current time is {current_time}"
        )


    # --------------------------------------------------------
    # DATE
    # --------------------------------------------------------

    elif (
        "what is today's date" in query
        or "what is the date" in query
        or query == "date"
        or "tell me the date" in query
    ):

        current_date = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        speak(
            f"Today's date is {current_date}"
        )


    # --------------------------------------------------------
    # PLAY MUSIC
    # --------------------------------------------------------

    elif (
        "play music" in query
        or "play song" in query
    ):

        play_music()


    # --------------------------------------------------------
    # OPEN VS CODE
    # --------------------------------------------------------

    elif (
        "open visual studio code" in query
        or "open vs code" in query
        or "open code" in query
    ):

        speak("Opening Visual Studio Code.")

        try:

            os.system("code")

        except Exception as e:

            print("VS Code error:", e)

            speak(
                "I could not open Visual Studio Code."
            )


    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    elif (
        "hello" in query
        or "hi" in query
        or "hey" in query
    ):

        speak("Hello! How can I help you?")


    # --------------------------------------------------------
    # WHO ARE YOU
    # --------------------------------------------------------

    elif (
        "who are you" in query
        or "what are you" in query
    ):

        speak(
            "I am your Python voice assistant. "
            "I can open websites, search Wikipedia, "
            "tell you the time and date, and play music."
        )


    # --------------------------------------------------------
    # EXIT
    # --------------------------------------------------------

    elif (
        query == "exit"
        or query == "quit"
        or query == "stop"
        or query == "goodbye"
        or "shut down" in query
    ):

        return "exit"


    # --------------------------------------------------------
    # UNKNOWN
    # --------------------------------------------------------

    else:

        speak(
            "I don't know that command yet."
        )

    return "continue"


# ============================================================
# MAIN
# ============================================================

def main():

    print("\n========================================")
    print("       PYTHON VOICE ASSISTANT")
    print("========================================")

    wish_me()
    speak("Hello master!,how can I help you today?")

    while True:

        query = take_command()

        if query == "exit":

            speak("Goodbye!")
            break

        if not query:

            continue

        result = process_query(query)

        if result == "exit":

            speak("Goodbye!")
            break


# ============================================================
# START PROGRAM
# ============================================================

if __name__ == "__main__":
    main()