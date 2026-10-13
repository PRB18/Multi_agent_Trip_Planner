from llm_client import ask_gemini

def plan_trip(
    start_location: str, 
    destination: str, 
    per_person_budget: int, 
    days: int, 
    members: int, 
    side_note: str = ""   # Optional parameter with default empty string
):
    # Automatically calculate total group budget in Python
    total_budget = per_person_budget * members

    system_prompt = (
        "You are an expert travel consultant specializing in realistic, budget-conscious group itineraries.\n"
        "When planning a trip, you must:\n"
        "1. Recommend practical transport options from the starting location to the destination (train, flight, bus, or drive) with estimated costs.\n"
        "2. Leverage group sizes for shared cost savings (shared rooms/villas, group cab rentals, split meals).\n"
        "3. Provide a clear day-by-day itinerary with practical activities.\n"
        "4. Include a detailed budget breakdown covering: Inter-city Travel, Accommodation, Local Transport, Food, Activities, and Emergency Buffer.\n"
        "5. Strictly respect the specified budget limits.\n"
        "6. Strictly honor any special requests, preferred travel modes, or constraints provided in the user's notes."
    )

    # Format the side note if one was provided
    note_line = f"\n- Additional Preferences / Notes: {side_note}" if side_note else ""

    user_prompt = (
        f"Please plan a {days}-day group trip with the following details:\n"
        f"- Starting Point: {start_location}\n"
        f"- Destination: {destination}\n"
        f"- Group Size: {members} people\n"
        f"- Budget per Person: ₹{per_person_budget:,}\n"
        f"- Total Group Budget: ₹{total_budget:,}"
        f"{note_line}\n\n"
        f"Provide a day-by-day plan and a cost breakdown showing both per-person and total group expenses."
    )

    return system_prompt, user_prompt   


if __name__ == "__main__":
    # Example: Notice the comma after members=10
    sp, up = plan_trip(
        start_location="Mumbai",
        destination="Goa",
        per_person_budget=15000,
        days=4,
        members=10,
        side_note="Prefer traveling by sleeper train, purely vegetarian food, and stay in a air bnb."
    )

    result = ask_gemini(sp, up)
    print(result)
