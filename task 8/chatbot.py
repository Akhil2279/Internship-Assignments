# chatbot.py

import wikipedia

print("Hello! I am SmartChatBot. Ask me anything! (type 'bye' to exit)")

while True:
    user_input = input("You: ").lower()

    # greetings
    if user_input in ["hi", "hello", "hey"]:
        print("ChatBot: Hello! How can I help you today?")

    # asking name
    elif "your name" in user_input:
        print("ChatBot: I am SmartChatBot, powered by Python and Wikipedia!")

    # feelings
    elif "how are you" in user_input:
        print("ChatBot: I'm doing great, thanks for asking! How are you?")

    # time
    elif "time" in user_input:
        from datetime import datetime
        print("ChatBot: The current time is", datetime.now().strftime("%H:%M:%S"))

    # exit condition
    elif "bye" in user_input:
        print("ChatBot: Goodbye! Have a nice day ")
        break

    else:
        try:
            # Try to fetch summary from Wikipedia
            answer = wikipedia.summary(user_input, sentences=2)
            print("ChatBot:", answer)
        except wikipedia.exceptions.DisambiguationError as e:
            print("ChatBot: Hmm, that’s too broad. Did you mean one of these?", e.options[:5])
        except wikipedia.exceptions.PageError:
            print("ChatBot: Sorry, I couldn’t find anything about that.")
        except Exception as e:
            print("ChatBot: Oops, something went wrong. Please try again.")
