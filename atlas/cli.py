import typer

from atlas.config import config
from atlas.guardrails import check_input
from atlas.llm import chat
from atlas.memory import save, search

app = typer.Typer()

SYSTEM_PROMPT = config.persona.system_prompt


def build_system_prompt(query: str) -> tuple[str, int]:
    memories = search(query)
    if not memories:
        return SYSTEM_PROMPT, 0

    memories_text = "\n".join(f"- {m}" for m in memories)
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Éléments de contexte issus des conversations précédentes :\n"
        f"{memories_text}"
    )
    return prompt, len(memories)


@app.command()
def main(
    model: str = typer.Option(config.model.name, help="Modèle Ollama à utiliser"),
    timeout: float = typer.Option(500, help="Timeout en secondes"),
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

        guard = check_input(user_input)
        if not guard.allowed:
            print(f"Atlas : {guard.reason}\n")
            continue

        user_input = guard.text

        system_prompt, memory_hits = build_system_prompt(user_input)
        messages = [{"role": "system", "content": system_prompt}] + history
        messages.append({"role": "user", "content": user_input})

        print("Atlas : ", end="", flush=True)

        if stream:
            response_text = ""
            for token in chat(
                model, messages, timeout=timeout, stream=True, memory_hits=memory_hits
            ):
                print(token, end="", flush=True)
                response_text += token
            print("\n")
        else:
            response_text = chat(
                model,
                messages,
                timeout=timeout,
                stream=False,
                memory_hits=memory_hits,
                guardrail_triggered=guard.triggered_rule or None,
            )
            print(f"{response_text}\n")

        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": response_text})

        save(user_input, response_text)
