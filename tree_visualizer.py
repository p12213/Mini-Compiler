from graphviz import Digraph
from reportlab.platypus import SimpleDocTemplate, Image as RLImage
from reportlab.lib.pagesizes import A4
from ast_nodes import *

def draw_ast(ast):
    if isinstance(ast, list):
        ast = ProgramNode(ast)

    dot = Digraph("AST", format="png")
    # Modern clean background and orthogonal lines
    dot.attr(rankdir="TB", bgcolor="#FAFAFA", splines="ortho")
    dot.attr(nodesep="0.6", ranksep="0.8")
    
    # Edge styling
    dot.attr("edge", fontname="Segoe UI", fontsize="10", color="#7F8C8D", penwidth="1.5")
    
    # Default node styling: vibrant colors, white text, no border
    dot.attr("node", fontname="Segoe UI", fontsize="12", fontcolor="white", shape="box", style="rounded,filled", penwidth="0")

    counter = [0]

    def new_id():
        counter[0] += 1
        return f"n{counter[0]}"

    def make_node(label, fill="#34495E", shape="box", fontcolor="white"):
        node_id = new_id()
        dot.node(node_id, label, fillcolor=fill, shape=shape, fontcolor=fontcolor)
        return node_id

    def connect(parent, child, edge_label=None):
        if edge_label:
            dot.edge(parent, child, label=edge_label, fontcolor="#34495E")
        else:
            dot.edge(parent, child)

    def add_nodes(node, parent=None, edge_label=None):
        if isinstance(node, ProgramNode):
            node_id = make_node("PROGRAM", fill="#2C3E50")
            if parent: connect(parent, node_id, edge_label)
            for stmt in node.statements:
                add_nodes(stmt, node_id)
            return node_id

        elif isinstance(node, AssignNode):
            node_id = make_node(f"ASSIGN\n{node.name}", fill="#D35400")
            if parent: connect(parent, node_id, edge_label)
            add_nodes(node.expr, node_id, "value")
            return node_id

        elif isinstance(node, PrintNode):
            node_id = make_node("PRINT", fill="#27AE60")
            if parent: connect(parent, node_id, edge_label)
            add_nodes(node.expr, node_id, "expr")
            return node_id

        elif isinstance(node, NumberNode):
            node_id = make_node(f"NUMBER\n{node.value}", fill="#C0392B")
            if parent: connect(parent, node_id, edge_label)
            return node_id

        elif isinstance(node, VarNode):
            node_id = make_node(f"VAR\n{node.name}", fill="#8E44AD")
            if parent: connect(parent, node_id, edge_label)
            return node_id

        elif isinstance(node, BinOpNode):
            symbols = {"PLUS": "+", "MINUS": "-", "MUL": "*", "DIV": "/", "LT": "<", "GT": ">", "EQEQ": "=="}
            op_symbol = symbols.get(node.op, node.op)
            node_id = make_node(f"BINOP\n{op_symbol}", fill="#2980B9", shape="circle" if len(op_symbol) <= 2 else "box")
            if parent: connect(parent, node_id, edge_label)
            add_nodes(node.left, node_id, "left")
            add_nodes(node.right, node_id, "right")
            return node_id

        elif isinstance(node, IfNode):
            node_id = make_node("IF", fill="#E67E22", shape="hexagon")
            if parent: connect(parent, node_id, edge_label)

            cond_id = make_node("CONDITION", fill="#F39C12", shape="diamond", fontcolor="black")
            connect(node_id, cond_id)
            add_nodes(node.condition, cond_id)

            body_id = make_node("THEN", fill="#16A085", shape="folder")
            connect(node_id, body_id)
            for stmt in node.body: add_nodes(stmt, body_id)

            if node.else_body:
                else_id = make_node("ELSE", fill="#E74C3C", shape="folder")
                connect(node_id, else_id)
                for stmt in node.else_body: add_nodes(stmt, else_id)

            return node_id

        elif isinstance(node, WhileNode):
            node_id = make_node("WHILE", fill="#F39C12", shape="hexagon", fontcolor="black")
            if parent: connect(parent, node_id, edge_label)

            cond_id = make_node("CONDITION", fill="#F1C40F", shape="diamond", fontcolor="black")
            connect(node_id, cond_id)
            add_nodes(node.condition, cond_id)

            body_id = make_node("BODY", fill="#1ABC9C", shape="folder")
            connect(node_id, body_id)
            for stmt in node.body: add_nodes(stmt, body_id)

            return node_id

        elif isinstance(node, ForNode):
            node_id = make_node("FOR LOOP", fill="#34495E", shape="hexagon")
            if parent: connect(parent, node_id, edge_label)

            var_id = make_node(f"VAR\n{node.var_name}", fill="#9B59B6", shape="ellipse")
            connect(node_id, var_id)

            start_id = make_node("START", fill="#F39C12", shape="ellipse", fontcolor="black")
            connect(node_id, start_id)
            add_nodes(node.start, start_id)

            end_id = make_node("END", fill="#E67E22", shape="ellipse")
            connect(node_id, end_id)
            add_nodes(node.end, end_id)

            body_id = make_node("BODY", fill="#1ABC9C", shape="folder")
            connect(node_id, body_id)
            for stmt in node.body: add_nodes(stmt, body_id)

            return node_id

        elif isinstance(node, FuncNode):
            node_id = make_node(f"FUNCTION\n{node.name}", fill="#2ECC71", shape="component")
            if parent: connect(parent, node_id, edge_label)

            body_id = make_node("BODY", fill="#27AE60", shape="folder")
            connect(node_id, body_id)
            for stmt in node.body: add_nodes(stmt, body_id)

            return node_id

        elif isinstance(node, CallNode):
            node_id = make_node(f"CALL\n{node.name}", fill="#E74C3C", shape="cds")
            if parent: connect(parent, node_id, edge_label)
            return node_id

        else:
            node_id = make_node(node.__class__.__name__, fill="#95A5A6")
            if parent: connect(parent, node_id, edge_label)
            return node_id

    add_nodes(ast)

    img_path = dot.render("ast_tree", cleanup=True)

    pdf_path = "ast_tree.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    doc.build([RLImage(img_path, width=400, height=600)])

    return img_path, pdf_path