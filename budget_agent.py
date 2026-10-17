from llm_client import ask_gemini

def budget_agent(per_person_budget:int, members:int, days:int, research_report: str)->str:
    total_budget = per_person_budget * members

    system_prompt = (
        "You are a strict Financial Auditor for group travel.\n"
        "Your ONLY job is to evaluate pricing options and calculate exact bottom-up costs.\n"
        "RULES:\n"
        "1. Do NOT write a day-by-day itinerary.\n"
        "2. Review the research options provided by the Research Agent.\n"
        "3. Select the best cost-effective options that match user constraints (e.g., Sleeper train, Airbnb villa).\n"
        "4. Calculate bottom-up costs transparently:\n"
        "   - Inter-city travel: round-trip per person × members\n"
        "   - Accommodation: rate per night × nights (divided by members)\n"
        "   - Local transport: daily vehicle rate × days (divided by members)\n"
        "   - Food: exact meal count (days × meals) × average cost\n"
        "5. Output an itemized cost table and state clearly whether the total fits under the budget limit or has savings."
    )

    user_prompt = (
         f"BUDGET CONSTRAINTS:\n"
        f"- Per-Person Budget Limit: ₹{per_person_budget:,}\n"
        f"- Group Size: {members} people\n"
        f"- Total Budget Ceiling: ₹{total_budget:,}\n"
        f"- Duration: {days} days\n\n"
        f"RESEARCH DATA FROM RESEARCH AGENT:\n"
        f"\"\"\"\n{research_report}\n\"\"\"\n\n"
        f"Audit these options and provide a complete bottom-up cost breakdown."
    )

    return ask_gemini(system_prompt, user_prompt)

    