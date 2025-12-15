import requests
import sys
import json
import subprocess
from pathlib import Path
from typing import List, Tuple, Dict

# --- Configuration ---
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3:8b" # Ensure this model is pulled in Ollama
OUTPUT_QMD_FILE = "ai_ast_grep_review.qmd"

# --- Language & Pattern Mapping for ast-grep ---
# We use ast-grep's built-in patterns for function/method/class definitions.
# --- Language & Pattern Mapping for ast-grep ---
LANGUAGE_MAP = {
    # UPDATED PYTHON PATTERN: Search for functions/methods (more granular than classes)
    '.py': {'lang': 'python', 'pattern': 'def $NAME($PARAMS): $$$'},
    '.js': {'lang': 'javascript', 'pattern': 'function $NAME($PARAMS) { $$$ }'},
    '.ts': {'lang': 'typescript', 'pattern': 'function $NAME($PARAMS) { $$$ }'},
    '.go': {'lang': 'go', 'pattern': 'func $NAME($PARAMS) $RETURN { $$$ }'},
    '.rs': {'lang': 'rust', 'pattern': 'fn $NAME($PARAMS) $RETURN { $$$ }'},
    '.java': {'lang': 'java', 'pattern': 'class $NAME { $$$ }'}, # Java mostly classes
    '.c': {'lang': 'c', 'pattern': 'int $NAME($PARAMS) { $$$ }'},
}

def detect_language(file_path: Path) -> str:
    """Detects language based on file extension and returns ast-grep details."""
    ext = file_path.suffix.lower()
    return LANGUAGE_MAP.get(ext, None)

# --- Stage 1: Code Parsing using ast-grep ---

def parse_code_into_blocks_ast_grep(file_path: Path, lang_config: Dict) -> List[Tuple[str, str]]:
    """
    Uses the 'sg scan --json' command to find logical blocks (functions/classes)
    and extracts their source code using the corrected argument order.
    """
    code_content = file_path.read_text(encoding='utf-8')
    language = lang_config['lang']
    pattern = lang_config['pattern']
    
    print(f"   -> Using ast-grep ({language}) with pattern: '{pattern}'")

    try:
        command = [
            'sg', 
            'run', 
            '--json', 
            '--pattern', pattern,
            '-l', language,
            str(file_path),
        ]
        
        print(f"   -> Comando SG: {' '.join(command)}")
        
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        
        # Parse the JSON output
        matches = json.loads(result.stdout)
        
    except subprocess.CalledProcessError as e:
        print(f"   !!! Error running ast-grep: {e.stderr.strip()}")
        print("   !!! CHECK 1: Ensure 'sg' is in your PATH.")
        print("   !!! CHECK 2: Try simplifying the pattern in LANGUAGE_MAP if this continues.")
        # Fallback to simple file-level block if ast-grep fails
        return [("Code File Logic", code_content)]
    except json.JSONDecodeError:
        print("   !!! Error decoding ast-grep JSON output. Check ast-grep installation.")
        return [("Code File Logic", code_content)]

    blocks = []
    found_lines = set()
    
    for match in matches:
        # sg run JSON output: match['range']['start']['line'] is 0-indexed
        start_line = match['range']['start']['line']
        end_line = match['range']['end']['line'] + 1 # Include the end line
        
        # Extract source code for the match
        block_code = '\n'.join(code_content.splitlines()[start_line:end_line]).strip()
        
        # Try to determine a title from the matched code
        first_line = block_code.splitlines()[0]
        block_title = f"{language.capitalize()} Block: {first_line[:50]}..."
        
        if block_code and start_line not in found_lines:
            blocks.append((block_title, block_code))
            # Mark all lines of this block as found to prevent overlap
            for line_num in range(start_line, end_line):
                found_lines.add(line_num)
                
    if not blocks and code_content.strip():
        # If no blocks were found, treat the whole file as one block
        return [("Entire File Logic", code_content.strip())]
        
    return blocks

def get_ollama_explanation(code_block: str, block_title: str) -> str:
    """
    Sends a request to the local Ollama API to get an explanation for the code block.
    (Same as before, ensuring consistency in the senior-level explanation prompt)
    """
    print(f"   -> Querying model for: {block_title}...")

    prompt = f"""
You are a Senior Software Engineer specializing in teaching.
Analyze the following code block, which is part of a larger file, titled: "{block_title}".

1.  **Summarize** the block's *intent* and *functionality*.
2.  **Explain** the underlying technical concepts as if teaching an unknowledgeable person (simple terms, high-level analogies).
3.  **Maintain** a professional, senior-level language and tone throughout the explanation.
4.  **Do not** include the code itself in your explanation.

CODE BLOCK:
---
{code_block}
---
"""
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3
        }
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload, timeout=1200)
        response.raise_for_status() 
        explanation = response.json().get('response', 'Error: Model response not found.')
        return explanation.strip()

    except requests.exceptions.RequestException as e:
        print(f"   !!! Error communicating with Ollama API: {e}")
        return f"AUTOMATIC ANALYSIS FAILED: Ollama connection error. Please check if Ollama is running and '{OLLAMA_MODEL}' is installed."

# --- Stage 2: QMD/TXT Generation ---

def generate_qmd(input_path: Path, blocks_with_explanations: List[Tuple[str, str, str]]):
    """
    Generates the final QMD file.
    """
    lang = input_path.suffix.lstrip('.').lower() or 'text'
    qmd_file = Path(OUTPUT_QMD_FILE)

    qmd_output = f"""---
title: "Senior Software Engineer Code Review - {input_path.name}"
subtitle: "Analyzed by {OLLAMA_MODEL} using ast-grep"
format:
  revealjs:
    scrollable: true
    # Enhanced Autopilot: 10 seconds for reading and thinking
    auto-slide: 10000 
    auto-advance: true
    transition-speed: slow
    # New Feature: Show progress bar
    progress: true
---

# Code Review Walkthrough

"""
    # Code Statistics and Summary Slide
    qmd_output += f"""
## Summary & Metrics

* **File:** `{input_path.name}`
* **Language:** `{lang.upper()}`
* **Total Blocks Analyzed:** **{len(blocks_with_explanations)}**
* **LLM Used:** `{OLLAMA_MODEL}`

This presentation will auto-advance every 10 seconds. Focus on the code on the left and the Senior Engineer's explanation on the right.

"""

    for i, (title, code, explanation) in enumerate(blocks_with_explanations):
        # Adding line numbers for quick reference (Markdown formatting)
        code_lines = len(code.splitlines())
        
        block_content = f"""
## Block {i+1}: {title} 
*(~{code_lines} lines of code)*

### 💻 Code ({lang.upper()})
```{{{lang}}}
{code.strip()}
```

### 🧠 Senior Explanation
{explanation.strip()}

"""
        qmd_output += block_content
    qmd_file.write_text(qmd_output, encoding='utf-8')
    
    print(f"\n✅ Generated Quarto Presentation file: {qmd_file.name}")
    print("\n>>> NEXT STEP: Run Quarto to see the result:")
    print(f"    quarto render {qmd_file.name} --to revealjs")

def main(): 
    if len(sys.argv) < 2: 
        print("Usage: python ast_grep_analyzer.py <path_to_code_file>") 
        print("Supported extensions:", list(LANGUAGE_MAP.keys())) 
        sys.exit(1)

    input_path = Path(sys.argv[1])

    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found.")
        sys.exit(1)

    lang_config = detect_language(input_path)
    if not lang_config:
        print(f"Error: Unsupported file extension '{input_path.suffix}'.")
        print("Supported extensions:", list(LANGUAGE_MAP.keys()))
        sys.exit(1)

    print(f"--- Starting AST-Grep Analysis of {input_path.name} ---")

    # 1. Parse the code using ast-grep
    code_blocks = parse_code_into_blocks_ast_grep(input_path, lang_config)
    print(f"Found {len(code_blocks)} logical code blocks using ast-grep.")

    # 2. Get explanations from Ollama
    blocks_with_explanations = []
    for title, code in code_blocks:
        print(f"\nProcessing Block: {title}")
        explanation = get_ollama_explanation(code, title)
        blocks_with_explanations.append((title, code, explanation))

    # 3. Generate the output files
    generate_qmd(input_path, blocks_with_explanations)

if __name__ == "__main__": 
    main()
