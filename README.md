from local_config import OPENAI_API_KEY
from openai import OpenAI

client = OpenAI(api_key=OPENAI_API_KEY)


print("===============================")
print("            AURA AI                                ")
print("===============================")

print("Hi!👋 welcome back 😊")

name=input("I'M YOUR AI ASSISTANT. \nwhat is your name?😄")
print(f"Hello {name} ! I AM AURA😀.")

memory=[]


# 🌱 DAY 7: Sustainability knowledge
sustainability = {
    "water": "Save water by fixing leaks and turning off taps when not needed. 💧",
    "energy": "Save energy by switching off unused lights and appliances. ⚡",
    "plastic": "Reduce plastic waste by reusing items and avoiding unnecessary plastic. ♻️",
    "trees": "Trees provide habitats and help absorb carbon dioxide. 🌳",
    "climate": "Climate change means long-term changes in Earth's climate patterns. 🌍"
}

def aura_response(message):

    # DAY 7
    if message in sustainability:
        return sustainability[message]

    elif message == "hello":
        return "Hello! 😀"

    # DAY 5 + DAY 6 + DAY 8
    else:
        try:
            response = client.responses.create(
                model="gpt-5.6",
                input=message
            )

            return response.output_text

        except Exception as e:
            return "Sorry, I'm having trouble right now. Please try again. 😔"
        
while True:

    message = input("You: ")

    memory.append(message)

    if message == "bye":
        print("👋 Bye! Nice talking with you!")
        break

    response = aura_response(message)

    print("AURA:", response)

 
print("AURA memory:")
print(memory)

