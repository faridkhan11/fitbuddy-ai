import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_plan(age, weight, goal, intensity):

    try:

        prompt = f"""
        Create a simple 7-day fitness workout plan.

        User details:
        Age: {age}
        Weight: {weight}
        Goal: {goal}
        Workout Intensity: {intensity}

        Format:

        Day 1:
        Day 2:
        Day 3:
        Day 4:
        Day 5:
        Day 6:
        Day 7:

        Also give 3 nutrition tips.
        """

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        return f"Error generating plan: {str(e)}"