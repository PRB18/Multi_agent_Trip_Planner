from naive_multi_agent import research_agent
from budget_agent import budget_agent

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

    budget_output = budget_agent(
        15000,
        10,
        4,
        resarch_output
    )
    print(budget_output)