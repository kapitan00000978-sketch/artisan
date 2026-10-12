from craftsman import CraftsmanAgent

def main():
    print("=== Humanpowers Python Agent (Active Demo) ===")
    agent = CraftsmanAgent(
        persona="software_architect",
        min_passing_score=95
    )

    result = agent.execute("Create a secure user authentication module with JWT rotation")
    print("\n[HUMANPOWERS VERIFIED RESULT]:")
    print(f"Holati: {result['status']}")
    print(f"Sifat ko'rsatkichi: {result['score']}/100")
    print(f"Avtomatik tuzatilgan xatolar: {result['flaws_fixed']} ta")

if __name__ == "__main__":
    main()
