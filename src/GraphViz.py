import graphviz

def render(user_id: str, doc_id: str, docs: list[tuple[str, int]], graph: dict[str, list[str]]):
    g = graphviz.Digraph('also_likes', filename='also_likes.gv')

    g.node(user_id[-4:], user_id[-4:], style='filled', fillcolor="green")
    g.node(doc_id[-4:], doc_id[-4:], style='filled', fillcolor="green")

    for doc, users in graph.items():
        for user in users:
            g.edge(user[-4:], doc[-4:])


    g.view()