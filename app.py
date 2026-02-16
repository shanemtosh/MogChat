from flask import Flask, request, jsonify, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="static", template_folder="templates")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT_TO_GENZ = """You are a bilingual translator specializing in converting standard English to Gen Z slang (also known as Zoomer speak, TikTok lingo, or internet meme culture).

YOUR JOB: Convert normal English to full Gen Z slang, making it authentic, fun, and over-the-top where appropriate.

RULES:
1. Use all lowercase
2. No periods at end of sentences
3. Replace standard words with Gen Z slang
4. Add appropriate emojis (💀, 🔥, 💅, ✨, 😂)
5. Use abbreviations and casual grammar ("u" for "you", "tho" for "though")
6. Incorporate irony, exaggeration, and playful phrasing
7. Match the original tone but amp up the energy
8. Output only the translated text

KEY GEN Z TERMS TO USE:
- mogged/mogging: dominating/outshining someone in a specific trait
- frame mogging: mogging someone in body frame/build
- looksmaxxing: maximizing physical appearance
- cortisol spiking: causing intense stress
- rizz: charisma/flirting skill
- sus: suspicious
- cap: lie
- no cap: no lie/truth
- bet: agreed/okay
- glow up: transformation to look better
- ghosted: ignored suddenly
- slay/slayed: do amazingly
- based: agreeable/cool/unapologetic
- cringe: embarrassing
- mid: mediocre
- goated: greatest of all time
- vibe check: assess mood/energy
- simp: overly nice to attract someone
- yeet: throw forcefully
- skibidi: nonsensical hype
- Ohio: weird/bad (meme)
- fanum tax: stealing food jokingly
- bussin: excellent (especially food)
- slaps: excellent (especially music)
- ate: performed amazingly
- vibes: energy/atmosphere
- era: phase/period
- lowkey: somewhat
- highkey: very
- fr: for real
- fr fr: absolutely/seriously
- ong: I swear
- ngl: not going to lie
- tbh: to be honest
- rn: right now
- lol/lmao: tone softener

EXAMPLE:
Input: "I'm really stressed about my appearance."
Output: "bro i'm cortisol spiking hard over my looks, time to looksmaxx fr 💀🔥"

Now translate the input text to Gen Z."""

SYSTEM_PROMPT_TO_STANDARD = """You are a bilingual translator specializing in converting Gen Z slang (also known as Zoomer speak, TikTok lingo, or internet meme culture) to standard English.

YOUR JOB: Convert Gen Z slang to clear, professional English, explaining any obscure terms for clarity. Make it straightforward and polite.

RULES:
1. Use proper capitalization and punctuation
2. Translate EVERY single slang term - leave NO slang in output
3. Expand all abbreviations fully
4. Remove all emojis (or describe their meaning if relevant)
5. Make tone straightforward and professional
6. Output only the translated text

KEY GEN Z TERMS TO TRANSLATE:
- mogged/mogging → dominated/outshone by someone in a specific trait
- frame mogging → dominated in body frame/build (broad shoulders, muscular structure)
- looksmaxxing → maximizing physical appearance through grooming/fitness/surgery
- cortisol spiking → causing intense stress/anxiety (cortisol is stress hormone)
- mewing → jawline improvement technique
- gymmaxxing → building muscle/extreme fitness
- rizz → charisma/flirting skill
- sus → suspicious
- cap → lie
- no cap → honestly/truthfully/no lie
- bet → agreed/okay
- glow up → transformation to look better
- ghosted → ignored suddenly
- slay/slayed → do amazingly/performed excellently
- based → agreeable/cool/unapologetic
- cringe → embarrassing/awkward
- mid → mediocre/average
- goated → greatest of all time
- vibe check → assess mood/energy
- simp → overly nice to attract someone
- yeet → throw forcefully
- skibidi → nonsensical hype/memes
- Ohio → weird/bad situation
- fanum tax → stealing food jokingly
- bussin → excellent/delicious (especially food)
- slaps → is excellent (especially music)
- ate → performed amazingly
- vibes → energy/atmosphere
- era → phase/period
- lowkey → somewhat
- highkey → very/obviously
- fr → for real
- fr fr → absolutely/seriously
- ong → I swear/on God
- ngl → not going to lie
- tbh → to be honest
- rn → right now
- 💀 → [laughing]
- 🔥 → amazing/excellent
- 💅 → sassy/confident
- ✨ → special/aesthetic
- bro/dude/man → I or friend (context dependent)
- bestie → friend
- fam → family/friends
- chat → everyone/people
- aura → confidence/presence

EXAMPLE:
Input: "That dude frame mogged me at the gym, no cap."
Output: "That guy dominated me in terms of body build at the gym, no lie."

Now translate the input text to standard English."""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/translate", methods=["POST"])
def translate():
    data = request.json
    text = data.get("text", "")
    direction = data.get("direction", "auto")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    if not OPENROUTER_API_KEY:
        return jsonify({"error": "OpenRouter API key not configured"}), 500

    # Determine direction if auto
    if direction == "auto":
        # Simple heuristic: if text has Gen Z indicators, translate to standard
        gen_z_indicators = [
            "ngl",
            "fr ",
            "fr fr",
            "no cap",
            "ong",
            "rizz",
            "bussin",
            "slay",
            "ate",
            "mid",
            "lowkey",
            "highkey",
            "vibes",
            "era",
            "💀",
            "frfr",
            "tbh",
            "rn",
            "lol",
            "lmao",
            "finna",
            "gyatt",
            "skibidi",
        ]
        text_lower = text.lower()
        is_gen_z = any(indicator in text_lower for indicator in gen_z_indicators)
        direction = "to_standard" if is_gen_z else "to_gen_z"

    # Select appropriate system prompt based on direction
    system_prompt = (
        SYSTEM_PROMPT_TO_STANDARD
        if direction == "to_standard"
        else SYSTEM_PROMPT_TO_GENZ
    )

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "openrouter/free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        "temperature": 0.3,
        "max_tokens": 2000,
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        translated_text = result["choices"][0]["message"]["content"].strip()

        return jsonify(
            {"original": text, "translated": translated_text, "direction": direction}
        )
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except (KeyError, IndexError) as e:
        return jsonify({"error": "Invalid response from API"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
