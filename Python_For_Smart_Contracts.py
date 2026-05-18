from dotenv import load_dotenv
import os
from google import genai
import json
import time
from pathlib import Path
import tkinter as tk
from tkinter import filedialog

# =========================================================
# 1️⃣ API KEY + CLIENT
# =========================================================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# =========================================================
# 2️⃣ PROMPT TEMPLATE
# =========================================================
PROMPT_TEMPLATE = """
Final Prompt:
You are a professional smart contract vulnerability detector. Analyze the following Solidity Smart contract while applying these rules strictly. Your scope is limited to examining only the executable code—functions, modifiers, and logic—while ignoring all comments, metadata, or non-functional text.

You must check for seven specific vulnerabilities:
1. Reentrancy
2. Access Control
3. Arithmetic issues
4. Unchecked Return Values
5. Denial of Service
6. Front-Running
7. Time Manipulation

Rules:
- Do not speculate.
- Only report evidence-based issues.
- Respect Solidity version protections.
- Ignore unreachable/dead code.

Output:
One line per vulnerability in this format:
<Vulnerability Name>: short justification. Verdict: 0 or 1

[INPUT]
{code}
"""

# =========================================================
# 3️⃣ ANALYSIS FUNCTION (UPDATED FOR NEW SDK)
# =========================================================
def analyze_contract(code, max_retries=3):
    prompt = PROMPT_TEMPLATE.format(code=code)

    result = ""

    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            result = response.text.strip()
            lines = [l.strip() for l in result.splitlines() if l.strip()]

            if len(lines) >= 7:
                return "\n".join(lines[:7])

            print(f"Retry {attempt+1}: Incomplete output ({len(lines)} lines)")
            time.sleep(2)

        except Exception as e:
            print(f"Error on attempt {attempt+1}: {e}")
            time.sleep(3)

    return result if result else "Analysis failed."

# =========================================================
# 4️⃣ FILE SELECTOR (VS CODE / WINDOWS)
# =========================================================
def select_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select Solidity Smart Contract",
        filetypes=[("Solidity files", "*.sol"), ("All files", "*.*")]
    )

    return file_path


# =========================================================
# 5️⃣ MAIN
# =========================================================
if __name__ == "__main__":

    print("📂 Select a Solidity smart contract file...")

    contract_path = select_file()

    if not contract_path:
        print("❌ No file selected. Exiting.")
        exit()

    # Read contract
    with open(contract_path, "r", encoding="utf-8") as f:
        code = f.read()

    print("\n🔍 Analyzing contract...\n")

    # Run analysis
    result = analyze_contract(code)

    # =====================================================
    # ✅ UPDATED OUTPUT FILE NAME LOGIC
    # =====================================================
    input_path = Path(contract_path)
    output_file = input_path.parent / f"{input_path.stem}_gemini_result.json"

    # Save output locally
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            {input_path.name: result},
            f,
            indent=2,
            ensure_ascii=False
        )

    print("✅ Analysis completed.")
    print("📄 Saved to:", output_file)

    print("\n========== RESULT ==========\n")
    print(result)