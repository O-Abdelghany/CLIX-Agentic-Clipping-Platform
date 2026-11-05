from app.graph.graph import graph


def main():
    print("Starting LangGraph application...")

    # Initial state to kick off the graph
    initial_state = {
        "messages": []
    }
    graph.get_graph().print_ascii()
    result = graph.invoke(initial_state)
    print("Graph execution complete.")
    print("Result:", result)


if __name__ == "__main__":
    main()
