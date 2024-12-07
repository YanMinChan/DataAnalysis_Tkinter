import graphviz
import pandas as pd

class GraphvizError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def render(user_id: str, doc_id: str, graph: pd.DataFrame):
    g = graphviz.Digraph("also_likes", filename="also_likes.gv")

    g.node(user_id[-4:], user_id[-4:], style="filled", fillcolor="green")
    g.node(doc_id[-4:], doc_id[-4:], style="filled", fillcolor="green")

    for u_id, d_id in zip(graph["visitor_uuid"], graph["env_doc_id"]):
        g.edge(u_id[-4:], d_id[-4:])

    try:
        g.view()
    except graphviz.CalledProcessError as error:
        raise GraphvizError(f"GraphvizError: {error}")
