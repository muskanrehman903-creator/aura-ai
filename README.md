print("===============================")
print("            AURA AI                                ")
print("===============================")

print("Hi!👋 welcome back 😊")

name=input("I'M YOUR AI ASSISTANT. \nwhat is your name?😄")
print(f"Hello {name} ! I AM AURA😀.")

message=[]

def aura_response(message):

    if message== "water":
	
        print("Let's talk about to save water!💦")

    elif message=="hello":
	
        print("Hello!😀")

    elif message=="energy":
	
        print("Let's save energy⚡")

    else:  

    	print("I'm still learning...😐") 

while True:

    message = input("You: ")

    memory.append(message)

    if message == "bye":
        print("👋 Bye! Nice talking with you!")
        break

    response = aura_response(message)

    print("AURA:", response)

 
print("AURA memory:")
print(menory)

