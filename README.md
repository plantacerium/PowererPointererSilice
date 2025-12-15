# Powerer Pointerer Silice Instructor

### *Your Codebase, Narrated by AI.*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![Ollama](https://img.shields.io/badge/Powered%20By-Ollama-white?style=for-the-badge&logo=ollama&labelColor=black)](https://ollama.ai/)
[![Quarto](https://img.shields.io/badge/Rendered%20With-Quarto-blueviolet?style=for-the-badge&logo=quarto)](https://quarto.org/)
[![ast-grep](https://img.shields.io/badge/Parsed%20With-ast--grep-green?style=for-the-badge)](https://ast-grep.github.io/)

---

**Instructor** is not just a code reviewer; it's a storytelling engine for software. It takes any source file, dissects it using advanced Abstract Syntax Trees (AST), feeds it to a local AI Senior Engineer, and produces a stunning, interactive presentation that walks you through the logic, intent, and brilliance of your code.

Whether you're onboarding new devs, reviewing complex legacy code, or just documenting your masterpiece, **Instructor** turns static text into a dynamic masterclass.

## 🚀 Why Powerer Pointerer Silice Instructor?

*   **🧠 Senior Engineer/Teacher Persona**: The AI doesn't just explain *what* the code does; it explains *why* it matters, using high-level analogies and professional insights.
*   **🔒 100% Local & Private**: Powered by **Ollama**, your code never leaves your machine. No API keys, no data leaks.
*   **⚡ Precision Parsing**: Uses **ast-grep** to structurally understand your code (functions, classes, methods) rather than dumb regex splitting.
*   **✨ Beautiful Output**: Generates a **Quarto (Reveal.js)** presentation with side-by-side code and explanation views, auto-advancing slides, and syntax highlighting.

## 🛠️ How It Works

1.  **Scan**: `ast-grep` parses your source file to identify logical blocks (functions, classes) based on the language grammar.
2.  **Analyze**: Each block is sent to a local LLM (via Ollama) with a "Senior Engineer" system prompt to generate a pedagogical explanation.
3.  **Render**: The results are woven into a `Quarto` markdown file (`.qmd`).
4.  **Present**: Quarto compiles this into a standalone HTML5 presentation.

## ⚡ Support

<div align="center">

**Made with ❤️ and ☕ by the Plantacerium**

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/plantacerium)

⭐ **Star us on GitHub** if the script is useful to You! ⭐

</div>

## 📦 Requirements

*   **Python 3.9+**
*   **[Ollama](https://ollama.ai/)** (Running locally with a model like `qwen2.5-coder` or `llama3`)
*   **[ast-grep](https://ast-grep.github.io/)** (`sg` command line tool)
*   **[Jupyter]([https://quarto.org/](https://jupyter.org/))** (Jupyter Notebooks)
*   **[Quarto](https://quarto.org/)** (CLI for rendering presentations)

## 🏁 Quick Start

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/plantacerium/PowererPointererSilice.git
    cd PowererPointererSilice
    ```

2.  **Install Python Dependencies**
    ```bash
    pip install requests
    ```

3.  **Ensure External Tools are Ready**
    *   Start Ollama: `ollama serve` (and make sure you've pulled your model, e.g., `ollama pull qwen3:8b`)
    *   Check `sg` and `quarto` are in your PATH.

4.  **Run Instructor**
    ```bash
    # Analyze a Python file
    python instructor.py path/to/your/code.py
    ```

5.  **View the Magic**
    Instructor generates a `.qmd` file. Render it using Quarto:
    ```bash
    quarto render ai_ast_grep_review.qmd --to revealjs
    ```
    Open the generated HTML file in your browser and enjoy the show! 🍿

## 🌍 Supported Languages

Instructor uses `ast-grep`'s powerful pattern matching. Out of the box, it supports:

*   🐍 **Python** (`.py`)
*   📜 **JavaScript** (`.js`)
*   📘 **TypeScript** (`.ts`)
*   🐹 **Go** (`.go`)
*   🦀 **Rust** (`.rs`)
*   ☕ **Java** (`.java`)
*   🇨 **C** (`.c`)

*Adding more languages is as easy as adding a single line to the `LANGUAGE_MAP` in `instructor.py`!*

## 🎨 Customization

Open `instructor.py` to tweak:
*   `OLLAMA_MODEL`: Change the AI brain (e.g., `mistral`, `codellama`, `deepseek-coder`).
*   `presentation settings`: Adjust slide timing, themes, or transition speeds in the `generate_qmd` function.

## 🤝 Contributing

We want to make code literacy universal. If you have ideas for better prompts, cooler Quarto themes, or more language support:
1.  Fork it.
2.  Branch it.
3.  Pull Request it.

## ⚡ Support

<div align="center">

**Made with ❤️ and ☕ by the Plantacerium**

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/plantacerium)

⭐ **Star us on GitHub** if the script is useful to You! ⭐

</div>

## 📄 License

MIT. Let's build something awesome.
