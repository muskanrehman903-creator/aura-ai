from flask import Flask, request, jsonify
from openai import OpenAI

from local_config import OPENAI_API_KEY


# =========================================
# AURA SETUP
# =========================================

app = Flask(__name__)

client = OpenAI(api_key=OPENAI_API_KEY)


# =========================================
# AURA MEMORY
# =========================================

memory = []

eco_points = 0
eco_history = []


# =========================================
# SUSTAINABILITY KNOWLEDGE
# =========================================

sustainability = {
    "water": (
        "Water is precious. 💧\n"
        "You can save water by turning off taps when they are not needed, "
        "fixing leaks, taking shorter showers, and avoiding unnecessary water waste."
    ),

    "energy": (
        "You can save energy by switching off lights and fans when they are "
        "not needed, using energy-efficient appliances, and avoiding unnecessary electricity use. ⚡"
    ),

    "plastic": (
        "You can reduce plastic waste by using reusable bottles and bags, "
        "avoiding unnecessary single-use plastic, and reusing items when possible. ♻️"
    ),

    "trees": (
        "Trees help the environment by absorbing carbon dioxide, supporting "
        "biodiversity, and helping keep ecosystems healthy. 🌳"
    ),

    "climate": (
        "Climate change is affected by greenhouse gas emissions. "
        "Saving energy, reducing waste, protecting trees, and using resources "
        "responsibly can help reduce environmental impact. 🌍"
    )
}


# =========================================
# ECO ACTIONS
# =========================================

eco_actions = {
    "Saving water": {
        "points": 2,
        "keywords": [
            "i saved water",
            "i used less water",
            "i turned off the tap",
            "i turned off water",
            "i stopped wasting water",
            "today i saved water"
        ]
    },

    "Saving energy": {
        "points": 2,
        "keywords": [
            "i saved energy",
            "i saved electricity",
            "i used less electricity",
            "i switched off the lights",
            "i turned off the lights",
            "i switched off the light",
            "today i saved electricity"
        ]
    },

    "Reducing plastic": {
        "points": 2,
        "keywords": [
            "i reused plastic",
            "i reused a plastic bottle",
            "i used a reusable bottle",
            "i reduced plastic",
            "i avoided plastic",
            "i avoided single use plastic",
            "today i reduced plastic"
        ]
    },

    "Planting a tree": {
        "points": 3,
        "keywords": [
            "i planted a tree",
            "i planted tree",
            "i planted a plant",
            "i helped plant a tree",
            "today i planted a tree"
        ]
    }
}


# =========================================
# FIND ECO ACTION
# =========================================

def find_eco_action(message):

    message = message.strip().lower()

    for action in eco_actions:

        for keyword in eco_actions[action]["keywords"]:

            if message == keyword:
                return action

    return None


# =========================================
# FIND SUSTAINABILITY TOPIC
# =========================================

def find_topic(message):

    message = message.lower()

    if "water" in message:
        return "water"

    if (
        "electricity" in message
        or "energy" in message
        or "light" in message
        or "lights" in message
    ):
        return "energy"

    if "plastic" in message:
        return "plastic"

    if (
        "tree" in message
        or "trees" in message
        or "plant" in message
    ):
        return "trees"

    if (
        "climate" in message
        or "global warming" in message
    ):
        return "climate"

    return None


# =========================================
# AURA RESPONSE
# =========================================

def aura_response(message):

    global eco_points

    message = message.strip().lower()


    # -----------------------------------------
    # GREETINGS
    # -----------------------------------------

    if message in ["hello", "hi", "hey", "salam", "assalamualaikum"]:

        return "Hello! 👋 How can I help you today?"


    # -----------------------------------------
    # GOODBYE
    # -----------------------------------------

    if message in ["bye", "goodbye", "allah hafiz"]:

        return "Allah Hafiz! 🌱 Keep caring for our planet. 🌍"


    # -----------------------------------------
    # ECO ACTION
    # -----------------------------------------

    action = find_eco_action(message)

    if action:

        points = eco_actions[action]["points"]


        # Prevent duplicate action
        if action in eco_history:

            return (
                f"You already recorded {action} in this session. 🌱\n"
                f"No extra points were added.\n"
                f"Your eco score is still {eco_points}. 📊"
            )


        eco_points += points

        eco_history.append(action)


        return (
            f"Great job! 🌱 You completed: {action}.\n\n"
            f"You earned {points} eco points.\n"
            f"Your total eco score is now {eco_points}. 📊"
        )


    # -----------------------------------------
    # ECO SCORE
    # -----------------------------------------

    if (
        message == "eco score"
        or message == "my eco score"
        or message == "score"
        or message == "points"
    ):

        if eco_history:

            actions_text = "\n".join(
                f"🌱 {action}" for action in eco_history
            )

            return (
                f"Your eco score is {eco_points} 🌱\n\n"
                f"Your eco actions:\n"
                f"{actions_text}"
            )

        else:

            return (
                "Your eco score is 0 🌱\n\n"
                "You haven't recorded any eco actions yet."
            )


    # -----------------------------------------
    # SUSTAINABILITY KNOWLEDGE
    # -----------------------------------------

    topic = find_topic(message)

    if topic:

        return sustainability[topic]


    # -----------------------------------------
    # AURA IDENTITY
    # -----------------------------------------

    if (
        "who are you" in message
        or "what are you" in message
        or "your name" in message
    ):

        return (
            "I'm AURA AI 🤖🌱\n"
            "A sustainability-focused AI assistant designed to "
            "help people learn about the environment and make "
            "eco-friendly choices."
        )


    # -----------------------------------------
    # AI FALLBACK
    # -----------------------------------------

    try:

        response = client.responses.create(
            model="gpt-5.6",
            input=(
                "You are AURA AI, a friendly sustainability assistant. "
                "Give short, useful and simple answers. "
                "Focus on environment, sustainability, water, energy, "
                "climate, trees and everyday eco-friendly actions.\n\n"
                f"User: {message}"
            )
        )

        return response.output_text


    except Exception:

        return (
            "I'm still learning. 🌱🤖\n"
            "Try asking me about water, energy, plastic, trees, "
            "climate, or your eco score."
        )


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    return """
<!DOCTYPE html>

<html>

<head>

<title>AURA AI</title>

<style>

body {
    font-family: Arial, sans-serif;
    background: #eef7ee;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 600px;
    margin: auto;
}

h1 {
    text-align: center;
}

.subtitle {
    text-align: center;
}

#chat {
    background: white;
    padding: 15px;
    border-radius: 12px;
    min-height: 350px;
    margin-top: 20px;
    white-space: pre-wrap;
}

input {
    width: 70%;
    padding: 12px;
    margin-top: 15px;
    border-radius: 8px;
    border: 1px solid #aaa;
}

button {
    padding: 12px 18px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

.user {
    margin-top: 15px;
    font-weight: bold;
}

.aura {
    margin-top: 8px;
    white-space: pre-wrap;
}

</style>

</head>


<body>

<div class="container">

<h1>🌱 AURA AI</h1>

<p class="subtitle">
AURA is running! 🤖
</p>

<div id="chat"></div>

<input
    id="message"
    placeholder="Talk to AURA..."
>

<button onclick="sendMessage()">
Send
</button>

</div>


<script>

async function sendMessage() {

    const input = document.getElementById("message");

    const message = input.value.trim();

    if (!message) {
        return;
    }


    const chat = document.getElementById("chat");


    chat.innerHTML +=
        '<div class="user">You: ' +
        message +
        '</div>';


    input.value = "";


    chat.innerHTML +=
        '<div class="aura" id="thinking">AURA is thinking... 🤖</div>';


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });


        const data = await response.json();


        document.getElementById("thinking").remove();


        chat.innerHTML +=
            '<div class="aura"><b>AURA:</b> ' +
            data.message.replace(/\\n/g, "<br>") +
            '</div>';


    }

    catch (error) {

        document.getElementById("thinking").innerHTML =
            "AURA: I couldn't connect to the server. 🤖";

    }

}


document.getElementById("message").addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);

</script>

</body>

</html>
"""


# =========================================
# CHAT API
# =========================================

@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    message = data.get("message", "").strip()


    if not message:

        return jsonify({
            "message": "Please type something. 🌱",
            "eco_points": eco_points
        })


    memory.append(message)


    answer = aura_response(message)


    return jsonify({
        "message": answer,
        "audio": None,
        "eco_points": eco_points
    })


# =========================================
# START AURA
# =========================================

if __name__ == "__main__":

    print("===============================")
    print("          AURA AI")
    print("===============================")

    print("")
    print("Open this in your browser:")
    print("http://127.0.0.1:8080")

    print("")
    print("AURA is running...")

    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False
    )