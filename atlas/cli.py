import typer

from atlas.llm import chat

app = typer.Typer()

SYSTEM_PROMPT = (
    "Tu es Atlas, assistant IA interne d'ATLAS Consulting. "
    "Tu réponds en français de façon concise et précise."
)


@app.command()
def main(
    model: str = typer.Option("qwen3:8b", help="Modèle Ollama à utiliser"),
    timeout: float = typer.Option(60.0, help="Timeout en secondes"),
    stream: bool = typer.Option(True, help="Activer le streaming"),
):
    print(f"Atlas AI - modèle : {model}")
    print("Tapez 'exit' pour quitter.\n")

    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input("Vous : ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir !")
            break

        if user_input.lower() == "exit":
            print("Au revoir !")
            break

        if not user_input:
            continue

        history.append({"role": "user", "content": user_input})

        print("Atlas : ", end="", flush=True)

        if stream:
            response_text = ""
            for token in chat(model, history, timeout=timeout, stream=True):
                print(token, end="", flush=True)
                response_text += token
            print("\n")
        else:
            response_text = chat(model, history, timeout=timeout, stream=False)
            print(f"{response_text}\n")

        history.append({"role": "assistant", "content": response_text})
