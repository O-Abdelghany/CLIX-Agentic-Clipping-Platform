from app.graph.graph import graph


def main():
    print("\nWelcome to CLIX — Your AI-powered video clipping assistant.")
    print("Type 'exit' or 'quit' to stop.\n")

    history = []

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("CLIX: Goodbye! See you next time.")
            break

        history.append({"role": "user", "content": user_input})

        result = graph.invoke({"messages": history})

        last_message = result["messages"][-1]
        response = last_message.content if hasattr(last_message, "content") else str(last_message)

        print(f"\nCLIX: {response}\n")

        history = result["messages"]


if __name__ == "__main__":
    main()
