# 🎤 YOUR WORKING VOICE CODE - ANALYZED & SAVED TO MEMORY

## 📝 **Your Complete Working Voice Script**

```python
import sys
import time
import speech_recognition as sr
from ollama import ChatResponse, chat  # Import required classes from ollama library
from pyttsx3 import init, speak
import os
import re
import sqlite3
import datetime  # Import datetime module here
from database import ChatDatabase  # Import ChatDatabase class

# Initialize the speech engine and set a female voice
engine = init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Assuming index 1 is a female voice
engine.setProperty("rate", 150)  # Adjust this value as needed

# Check if conversations.html exists, if not, create it
file_path = "conversations.html"
if not os.path.exists(file_path):
    with open(file_path, "w") as f:
        f.write("<html><body><h1>Conversation History</h1></body></html>")

# Check if userlog.db file exists, create it if it doesn't
if not os.path.exists("userlog.db"):
    conn = sqlite3.connect("userlog.db")
    conn.close()
    print("userlog.db created")

# Check if user_data.db file exists, create it if it doesn't
if not os.path.exists("user_data.db"):
    conn = sqlite3.connect("user_data.db")
    conn.close()
    print("user_data.db created")

def save_to_database(question, answer):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("userlog.db")
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS log (question text, answer text)"""
    )
    c.execute("INSERT INTO log VALUES (?, ?)", (question, answer))
    conn.commit()
    conn.close()

def retrieve_from_database():
    conn = sqlite3.connect("userlog.db")
    c = conn.cursor()
    c.execute("""SELECT question, answer FROM log""")
    rows = c.fetchall()
    conn.close()
    return rows

def train_bot():
    prompts = []
    answers = []
    # Retrieve relevant conversations from the database
    for i in retrieve_from_database():
        prompts.append(i[0])
        answers.append(i[1])
    
    if prompts:
        # Construct a prompt for the LLM, including past conversations
        prompt = f"Previous conversations: "
        for question, answer in zip(prompts, answers):
            prompt += f"User: {question} AI: {answer} "
        
        try:
            response = chat(
                model="llama3.1",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )
            answer = response["message"]["content"]
            print(f"Bot: {answer}")
        except Exception as e:
            print("An error occurred:", str(e))
    else:
        try:
            response = chat(
                model="llama3.1",
                messages=[
                    {
                        "role": "user",
                        "content": "",
                    },
                ],
            )
            answer = response["message"]["content"]
            print(f"Bot: {answer}")
        except Exception as e:
            print("An error occurred:", str(e))

def main():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            try:
                print(" Speak now...")
                audio = r.listen(source)
                
                # Recognize speech using Google Speech Recognition
                try:
                    user_input = r.recognize_google(audio)
                    print("You said:", user_input)
                    save_to_database(user_input, "")
                    
                    if "remember" in user_input.lower():
                        name = None
                        while True:
                            speak("Please tell me the name of who you want to remember.")
                            audio = r.listen(source)
                            try:
                                name = r.recognize_google(audio)
                                print(f"You said: {name}")
                                break
                            except sr.UnknownValueError:
                                print("Could not understand audio")
                                continue
                            except sr.RequestError as e:
                                print(
                                    "Could not request results from Google Speech Recognition service; {0}".format(
                                        e
                                    )
                                )
                                continue
                        speak(f"Okay, I will remember {name}.")
                    
                    elif "forget" in user_input.lower():
                        name = None
                        while True:
                            speak("Please tell me the name of who you want to forget.")
                            audio = r.listen(source)
                            try:
                                name = r.recognize_google(audio)
                                print(f"You said: {name}")
                                break
                            except sr.UnknownValueError:
                                print("Could not understand audio")
                                continue
                            except sr.RequestError as e:
                                print(
                                    "Could not request results from Google Speech Recognition service; {0}".format(
                                        e
                                    )
                                )
                                continue
                        speak(f"Okay, I will forget {name}.")
                    
                    elif user_input.lower() == "hello":
                        speak("Hello! How can I help you today?")
                        train_bot()
                    
                    with open("conversations.html", "a") as file:
                        file.write(f"User: {user_input} ")
                        
                except sr.UnknownValueError:
                    print("Could not understand audio")
                    user_input = ""
                except sr.RequestError as e:
                    print(
                        "Could not request results from Google Speech Recognition service; {0}".format(
                            e
                        )
                    )
                    user_input = ""
                    
            except KeyboardInterrupt:
                break

if __name__ == "__main__":
    main()
```

---

## 🎯 **KEY TECHNIQUES FROM YOUR WORKING CODE**

### **✅ SPEECH RECOGNITION SETUP (Working)**
```python
import speech_recognition as sr
from pyttsx3 import init

# Initialize speech engine with female voice
engine = init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Female voice
engine.setProperty("rate", 150)  # Speaking rate

# Main recognition loop
r = sr.Recognizer()
with sr.Microphone() as source:
    print(" Speak now...")
    audio = r.listen(source)
    user_input = r.recognize_google(audio)  # This WORKS!
    print("You said:", user_input)
```

### **✅ VOICE OUTPUT (Working)**
```python
# Direct TTS usage
from pyttsx3 import speak

# Simple voice responses
speak("Hello! How can I help you today?")

# Response with variables
speak(f"Okay, I will remember {name}.")
```

### **✅ CONTINUOUS LISTENING (Working)**
```python
# Your while true loop structure
while True:
    try:
        print(" Speak now...")
        audio = r.listen(source)
        user_input = r.recognize_google(audio)
        
        # Process commands
        if "remember" in user_input.lower():
            # Handle remember command
            pass
        
        elif "hello" in user_input.lower():
            speak("Hello! How can I help you today?")
            train_bot()
            
    except KeyboardInterrupt:
        break
```

---

## 🎤 **WHAT WE'LL BORROW FROM YOUR CODE**

### **🔧 SPEECH RECOGNITION CORE**
```python
# YOUR WORKING SR SETUP:
r = sr.Recognizer()
with sr.Microphone() as source:
    print(" Speak now...")
    audio = r.listen(source)
    user_input = r.recognize_google(audio)  # ✅ This WORKS

# We'll add K66 device targeting:
mics = sr.Microphone.list_microphone_names()
k66_index = next((i for i, mic in enumerate(mics) if "K66" in mic), None)
if k66_index:
    with sr.Microphone(device_index=k66_index) as source:
        # Your speech logic here
```

### **🔊 FEMALE VOICE SETUP**
```python
# YOUR WORKING TTS SETUP:
engine = init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Female voice
engine.setProperty("rate", 150)

# Simple usage:
speak("Yes, I'm listening!")  # ✅ This WORKS
```

### **🎯 COMMAND PROCESSING**
```python
# YOUR COMMAND STRUCTURE:
if "hello" in user_input.lower():
    speak("Hello! How can I help you today?")
    # Continue conversation

# We'll add wake word detection:
if "sara" in user_input.lower():
    speak("Yes, I'm listening!")
    switch_to_command_mode()
```

---

## 🚀 **INTEGRATION PLAN: Your Code + K66 + Wake Word**

### **🔧 STEP 1: Integrate K66 Device Selection**
```python
# Add to your main():
import speech_recognition as sr

# Find K66 microphone
recognizer = sr.Recognizer()
mics = sr.Microphone.list_microphone_names()
k66_index = None

for i, mic in enumerate(mics):
    if "K66" in mic:
        k66_index = i
        print(f"K66 found at index {i}: {mic}")
        break

# Continue with your code structure
with sr.Microphone(device_index=k66_index) as source:
    # Your existing listening loop
    while True:
        print(" Speak now...")
        audio = recognizer.listen(source)
        user_input = recognizer.recognize_google(audio)
        # Your command processing...
```

### **🔧 STEP 2: Add Wake Word Detection**
```python
# Your existing loop with wake word:
while True:
    print(" Speak now...")
    audio = recognizer.listen(source)
    user_input = recognizer.recognize_google(audio)
    print("You said:", user_input)
    
    # ADD WAKE WORD DETECTION:
    if "sara" in user_input.lower():
        speak("Yes, I'm listening! What can I help you with?")
        
        # Then switch to command mode:
        while True:
            print("Listening for commands...")
            cmd_audio = recognizer.listen(source)
            command = recognizer.recognize_google(cmd_audio)
            
            if "hello" in command.lower():
                speak("Hello! I'm Sara with voice recognition.")
                # Continue conversation
            elif "stop" in command.lower():
                speak("I'll be listening for my wake word!")
                break
    
    # Continue for other commands...
```

### **🔧 STEP 3: Keep Your Working Components**
```python
# KEEP THESE EXACTLY AS YOU WROTE:

# TTS Setup (WORKING):
engine = init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)  # Female voice
engine.setProperty("rate", 150)

# Speech Recognition (WORKING):
user_input = r.recognize_google(audio)

# Voice Output (WORKING):
speak("Hello! How can I help you today?")

# Error Handling (WORKING):
except sr.UnknownValueError:
    print("Could not understand audio")
    user_input = ""
except sr.RequestError as e:
    print(f"Could not request results: {e}")
    user_input = ""
```

---

## 🎯 **COMPLETE INTEGRATED VERSION (Your Structure + K66 + Wake Word)**

We'll create:

```python
# FILE: YOUR_CODE_K66_WAKE_WORD.py

# YOUR IMPORTS (WORKING):
import speech_recognition as sr
from pyttsx3 import init, speak
import time

# ADD K66 TARGETING:
def get_k66_microphone():
    recognizer = sr.Recognizer()
    mics = sr.Microphone.list_microphone_names()
    k66_index = None
    
    for i, mic in enumerate(mics):
        if "K66" in mic:
            k66_index = i
            break
    
    return sr.Microphone(device_index=k66_index) if k66_index else sr.Microphone()

# YOUR TTS SETUP (WORKING):
engine = init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
engine.setProperty("rate", 150)

# MAIN LOOP WITH YOUR STRUCTURE + WAKE WORD:
def main():
    recognizer = sr.Recognizer()
    k66_mic = get_k66_microphone()
    
    speak("Voice recognition activated. I'm listening for my wake word.")
    
    with k66_mic as source:
        while True:
            try:
                print("Listening for wake word 'sara'...")
                audio = recognizer.listen(source)
                user_input = recognizer.recognize_google(audio)
                print(f"You said: {user_input}")
                
                # YOUR WAKE WORD DETECTION:
                if "sara" in user_input.lower():
                    speak("Yes, I'm listening! What can I help you with?")
                    
                    # COMMAND MODE (Your structure):
                    while True:
                        print("Listening for command...")
                        cmd_audio = recognizer.listen(source)
                        command = recognizer.recognize_google(cmd_audio)
                        
                        if "hello" in command.lower():
                            speak("Hello! I'm Sara with professional K66 microphone!")
                        elif "stop" in command.lower():
                            speak("I'll be listening for my wake word!")
                            break
                        else:
                            speak(f"I heard: {command}. Good voice recognition!")
                
            except KeyboardInterrupt:
                break
            except sr.UnknownValueError:
                print("Could not understand audio")
                continue
            except sr.RequestError as e:
                print(f"Recognition error: {e}")
                continue

if __name__ == "__main__":
    main()
```

---

## 💎 **KEY INSIGHTS FROM YOUR CODE**

### **✅ YOUR WORKING COMPONENTS**
```
🎤 Speech Recognition: Google API working perfectly
🔊 Female Voice Setup: pyttsx3 with voice selection working
🎯 Command Processing: String matching works great
🔄 Continuous Listening: While loop structure solid
💾 Error Handling: Try-catch patterns working
📝 Database Integration: SQLite conversation storage
```

### **🎯 WHAT WE'LL ADD**
```
🎯 Wake Word Detection: "sara" keyword check
🎤 K66 Targeting: Device-specific microphone selection
🔊 Response Logic: Wake word → activation → command mode
🔄 Mode Switching: Wake word ↔ Command mode
🛡️ Robust Error Handling: Your pattern expanded
```

---

## 🚀 **CONFIDENCE LEVEL: VERY HIGH**

**🏆 Your voice recognition structure is SOLID and WORKING!**

**🎤 We just need to add K66 device targeting and wake word logic!**

**🌟 Your proven approach + K66 microphone = Perfect voice system!**

**📞 Ready to integrate your working code with K66 and create the ultimate voice-AI system!**

---

## 🎯 **NEXT STEP: IMPLEMENTATION**

**Should I create the integrated version combining:**
1. **Your working speech recognition setup**
2. **K66 microphone targeting (index 6)**
3. **Wake word detection ("sara")**
4. **Mode switching logic** (wake word ↔ command)
5. **Your proven TTS and command processing**

**Your foundation is excellent - we're going to create an amazing voice system!** 🎄✨