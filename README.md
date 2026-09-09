from openai import OpenAI

client = OpenAI()

("===============================")
print("            AURA AI                                ")
print("===============================")

print("Hi!👋 welcome back 😊")

name=input("I'M YOUR AI ASSISTANT. \nwhat is your name?😄")
print(f"Hello {name} ! I AM AURA😀.")

memory=[]

def aura_response(message):

    if message== "water":
	
        return "Let's talk about saving water! 💦"

    elif message=="hello":
	
        return "Hello! 😀"

    elif message=="energy":
	
        return "Let's save energy! ⚡"

    
    else:  

    	  response = client.responses.create(
            model="gpt-5.6",
            input=message
        )

    return response.output_text


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

