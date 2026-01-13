import time
from src.manager import initialize_research_task, execute_next_step
from src.config import PLAN_FILE, NOTEBOOK_FILE

def run_interactive_research():
    print("🔬 --- SPINTRONICS AI RESEARCHER (v2) ---")

    # 1. Check for Resume
    start_fresh = True
    if PLAN_FILE.exists():
        ans = input(f"📂 Found existing plan. Resume? (y/n): ").lower()
        if ans == 'y': 
            start_fresh = False
            print("✅ Resuming...")

    # 2. Initialize
    if start_fresh:
        first_goal = input("\n🎯 Research Goal: ")
        if not first_goal: first_goal = "MTJ stack optimization"
        initialize_research_task(first_goal, resume=False)

    # 3. Main Loop
    while True:
        print("\n⚙️ Working...")
        while True:
            success = execute_next_step()
            if not success: break
            time.sleep(2)

        print("\n✅ Plan Completed.")

        # 4. Interactive Follow-up
        user_input = input("\n🤖 Follow-up question? (Type question or 'exit'): ")
        if user_input.strip().lower() in ['exit', 'quit', 'no']: break

        print(f"📝 Adding to plan...")
        initialize_research_task(user_input, resume=True)

if __name__ == "__main__":
    run_interactive_research()
