from app.graph.state import State


def route(state: State) -> str:
    return state.get("route_to") or "end"