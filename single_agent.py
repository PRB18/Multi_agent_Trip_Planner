from llm_client import ask_gemini

def build_prompt(
    start_location: str, 
    destination: str, 
    per_person_budget: int, 
    days: int, 
    members: int, 
    side_note: str = ""
):
    # Calculate group total budget programmatically
    total_budget = per_person_budget * members

    system_prompt = (
        "You are an expert travel planner, logistics auditor, and strict budget accountant.\n"
        "Your task is to plan realistic, rigorously calculated itineraries. Adhere strictly to these mandatory rules:\n\n"

        "1. STRICT DAY COUNT & TIMELINE:\n"
        f"   - The entire trip MUST span EXACTLY {days} days (labeled Day 1 through Day {days}).\n"
        f"   - The {days} days INCLUDE all travel/transit days.\n"
        f"   - Day 1 begins when leaving {start_location}. Day {days} ends when returning to {start_location}.\n"
        f"   - Absolutely DO NOT generate 'Day 0' or 'Day {days + 1}'. If transit is overnight, it counts within Day 1 / Day 2.\n\n"

        "2. ZERO PREFERENCE OVERRIDES (NO ARBITRARY UPGRADES):\n"
        "   - Never alter or upgrade the user's explicit preferences for 'comfort', 'convenience', or 'budget balancing'.\n"
        "   - If 'sleeper train' or 'Sleeper (SL)' is requested, you MUST use Indian Railways Sleeper Class fares (~₹450-₹550 for Mumbai-Goa). Do NOT change it to AC 3-Tier or AC chair car.\n\n"

        "3. BOTTOM-UP MATHEMATICAL RIGOR (NO FORCED TOTALS):\n"
        "   - Every line item in the budget table must be calculated bottom-up using explicit unit rates.\n"
        "   - Food calculation must be transparent: state total meals count (e.g. days × 3 meals) × average cost per meal per person = exact food total.\n"
        "   - The numbers mentioned in the day-by-day itinerary text MUST match the numbers in the summary table.\n"
        "   - Do NOT force-inflate line items just to hit the budget cap. If the realistic total is less than the budget, report the difference as 'Unallocated Savings / Buffer'.\n\n"

        "4. GEOGRAPHIC & TRANSIT REALISM:\n"
        "   - Keep activities clustered geographically per day (e.g., keep North Goa and South Goa on separate days).\n"
        "   - Account for real-world travel durations (e.g., North Goa to South Goa / Old Goa to Palolem takes 1.5–2 hours each way). Never schedule unrealistic same-evening cross-district turnarounds.\n\n"

        "5. REALISTIC BENCHMARKS & SEASONALITY:\n"
        "   - Use realistic Indian ground rates: IRCTC Sleeper class fares (~₹500/person), 12-seater Tempo Traveller (~₹4,500-₹5,500/day + driver allowance), Airbnb for 10 people (~₹8,000-₹12,000/night total divided by 10).\n"
        "   - Acknowledge seasonality for seasonal markets or beach shacks (e.g., seasonal flea markets only operate November to April)."
    )

    note_section = f"\n- Additional User Constraints & Preferences: {side_note}" if side_note else ""

    user_prompt = (
        f"Please create a detailed, realistic {days}-day trip plan with the following specifications:\n"
        f"- Origin: {start_location}\n"
        f"- Destination: {destination}\n"
        f"- Group Size: {members} people\n"
        f"- Duration: Exactly {days} days (The {days} days include travel days. Day 1 starts when we leave {start_location}, and Day {days} ends back at {start_location})\n"
        f"- Budget Limit per Person: ₹{per_person_budget:,}\n"
        f"- Total Group Budget Limit: ₹{total_budget:,}"
        f"{note_section}\n\n"
        f"Required Output Format:\n"
        f"1. Day-by-Day Itinerary (Strictly Day 1 to Day {days}) with realistic timestamps, realistic travel durations, and geographically clustered spots.\n"
        f"2. Itemized Bottom-Up Budget Table with columns: [Category, Calculation / Formula, Cost Per Person (₹), Total Group Cost (₹)].\n"
        f"3. Verification Audit confirming exact day count ({days} days), adherence to user constraints, and exact mathematical sum."
    )

    return system_prompt, user_prompt


if __name__ == "__main__":
    import sys
    # Ensure Windows console supports Unicode characters like ₹
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')

    sp, up = build_prompt(
        start_location="Mumbai",
        destination="Goa",
        per_person_budget=15000,
        days=4,
        members=10,
        side_note="Strictly Sleeper (SL) train class only, purely vegetarian meals, stay in a shared Airbnb villa, avoid cross-region travel on the same day."
    )

    print("Generating itinerary with Gemini...\n")
    result = ask_gemini(sp, up)
    
    # Save to a markdown file for easy viewing
    with open("itinerary.md", "w", encoding="utf-8") as f:
        f.write(result)
        
    print(result)
    print("\nSaved full itinerary to itinerary.md")
