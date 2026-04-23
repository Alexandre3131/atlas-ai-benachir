import typer

from atlas.llm import chat
from atlas.memory import save, search

app = typer.Typer()

SYSTEM_PROMPT = (
    "Tu es Atlas, assistant IA interne d'ATLAS Consulting. "
    "Tu réponds en français de façon concise et précise."
)


def build_system_prompt(query: str) -> str:
    memories = search(query)
    if not memories:
        return SYSTEM_PROMPT

    memories_text = "\n".join(f"- {m}" for m in memories)
    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Éléments de contexte issus des conversations précédentes :\n"
        f"{memories_text}"
    )


@app.command()
def main(
    model: str = typer.Option("qwen3:8b", help="Modèle Ollama à utiliser"),
    timeout: float = typer.Option(60.0, help="Timeout en secondes"),
    stream: bool = typer.Option(True, help="Activer le streaming"),
):
    print(f"Atlas AI - modèle : {model}")
    print("Tapez 'exit' pour quitter.\n")

    history = []

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

        system_prompt = build_system_prompt(user_input)
        messages = [{"role": "system", "content": system_prompt}] + history
        messages.append({"role": "user", "content": user_input})

        print("Atlas : ", end="", flush=True)

        if stream:
            response_text = ""
            for token in chat(model, messages, timeout=timeout, stream=True):
                print(token, end="", flush=True)
                response_text += token
            print("\n")
        else:
            response_text = chat(model, messages, timeout=timeout, stream=False)
            print(f"{response_text}\n")

        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": response_text})

        save(user_input, response_text)
