from llm_client import ask_gemini

def research_agent(start_location : str,destination : str,days : int, members : int, side_note: str = "")-> str:
    system_prompt =  (
        "You are a dedicated Travel Research Scout.\n"
        "Your ONLY job is to research realistic travel options, accommodations, and activities.\n"
        "RULES:\n"
        "1. Do NOT build a day-by-day itinerary.\n"
        "2. Do NOT calculate the total trip budget.\n"
        "3. Output MUST be a structured, bulleted list with clear price estimates:\n"
        "   - Inter-city Transport: Specific train/bus options, travel class, estimated fare per person.\n"
        "   - Accommodation: 2-3 options suitable for the group size (e.g. shared villa/Airbnb) with price per night.\n"
        "   - Food: Average meal cost per person (respecting dietary preferences).\n"
        "   - Local Transport: Suitable options (e.g., Tempo Traveller daily rental rate).\n"
        "   - Key Attractions: Must be grouped by region (e.g., North vs South) with entry costs if any.\n"
        "4. Strictly honor any user preferences (e.g., specific train class, food type)."
    )

    note_section =  f"\nSpecific Preferences: {side_note}" if side_note else ""

    user_prompt =  (
        f"Research options for a trip:\n"
        f"- Origin: {start_location}\n"
        f"- Destination: {destination}\n"
        f"- Group Size: {members} people\n"
        f"- Duration: {days} days"
        f"{note_section}\n\n"
        f"Provide your structured research list with benchmark pricing."
    )

    return ask_gemini(system_prompt, user_prompt)

if __name__ == "__main__":
    import sys
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding='utf-8')

    resarch_output = research_agent(
        "Mumbai",
        "Goa",
        4,
        10,
        "Strictly Sleeper (SL) train class only, purely vegetarian meals, stay in a shared Airbnb villa, avoid cross-region travel on the same day."
    )
    print(resarch_output)