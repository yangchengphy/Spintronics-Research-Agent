import time
from google import genai
from src.config import *
from src.scientist import ask_expert

def initialize_research_task(goal, resume=False):
    if not API_KEY: return
    client = genai.Client(api_key=API_KEY)

    # RESUME MODE: Append to existing plan
    if resume and PLAN_FILE.exists():
        print(f"📂 Updating existing plan...")
        current_plan = PLAN_FILE.read_text(encoding="utf-8")
        update_prompt = f"""
        ORIGINAL PLAN:
        {current_plan}
        NEW REQUEST: "{goal}"
        TASK: Append 1-2 new steps to the plan to address the request.
        Format: [ ] N. FOLLOW-UP: <Action>
        Output ONLY the new steps.
        """
        try:
            response = client.models.generate_content(model=PLANNER_MODEL, contents=update_prompt)
            with open(PLAN_FILE, "a", encoding="utf-8") as f:
                f.write(f"\n{response.text}")
            print("✅ Plan Updated.")
            return
        except: pass

    # NEW MODE: Overwrite
    print(f"📋 Creating NEW Plan for: {goal}")
    prompt = f"""
    Create a 4-step research plan for: '{goal}'.
    Format:
    [ ] 1. EXPLORATION: <Action>
    [ ] 2. EXTRACTION: <Action>
    [ ] 3. SYNTHESIS: <Action>
    [ ] 4. CONCLUSION: <Action>
    Output ONLY the list.
    """
    try:
        response = client.models.generate_content(model=PLANNER_MODEL, contents=prompt)
        PLAN_FILE.write_text(f"# GOAL: {goal}\n\n{response.text}", encoding="utf-8")
        NOTEBOOK_FILE.write_text(f"# LAB NOTEBOOK: {goal}\n*Started: {time.ctime()}*\n\n", encoding="utf-8")
        print("✅ Plan Created.")
    except Exception as e: print(f"❌ Error: {e}")

def execute_next_step():
    if not PLAN_FILE.exists(): return False
    current_plan = PLAN_FILE.read_text(encoding="utf-8")
    current_notes = NOTEBOOK_FILE.read_text(encoding="utf-8")

    if "[ ]" not in current_plan: return False

    client = genai.Client(api_key=API_KEY)

    # --- CRITICAL FIX: PROMPT ENGINEERING ---
    # Forces Natural Language Output instead of Keywords
    manager_prompt = f"""
    CURRENT PLAN:
    {current_plan}
    NOTEBOOK SUMMARY:
    {current_notes[-4000:]}

    TASK: 
    1. Identify the first unchecked item '[ ]'. 
    2. Convert this step into a DETAILED, natural-language research request for the Scientist. 
    3. The request must include all specific constraints (materials, metrics like TMR >200%, process parameters).
    4. DO NOT summarize into keywords. Write it as a full command or question.

    Output ONLY the request string.
    """

    try:
        response = client.models.generate_content(model=PLANNER_MODEL, contents=manager_prompt)
        next_question = response.text.strip().replace('"', '')
        print(f"\n👉 MANAGER Asking: '{next_question}'")

        result = ask_expert(next_question)

        with open(NOTEBOOK_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n\n## Q: {next_question}\n**Findings:**\n{result}\n\n---")

        lines = current_plan.split('\n')
        for i, line in enumerate(lines):
            if "[ ]" in line:
                lines[i] = line.replace("[ ]", "[x]") + " (Completed)"
                break
        PLAN_FILE.write_text('\n'.join(lines), encoding="utf-8")
        return True
    except: return False
