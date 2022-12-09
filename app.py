from flask import Flask, redirect, render_template, request, url_for
from graphviz import Digraph, nohtml
import os


app = Flask(__name__, static_url_path="/static")


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BST:
    def __init__(self) -> None:
        self.root = None

    def insert(self, val):
        if self.root is None:
            self.root = Node(val)
        else:
            self._insert(self.root, val)

    def _insert(self, root, val):

        # Insert left
        if val < root.data:
            if root.left:
                self._insert(root.left, val)
            else:
                root.left = Node(val)

        # Insert right
        elif val > root.data:
            if root.right:
                self._insert(root.right, val)
            else:
                root.right = Node(val)

        # Check If equal
        else:
            print("Value already exists")
            return

    def search(self, root, key):
        if root is None:
            return False

        if key == root.data:
            return True

        elif key < root.data:
            return self.search(root.left, key)

        elif key > root.data:
            return self.search(root.right, key)

        else:
            return False

    def bfs(self):
        if self.root is None:
            return []
        q = [self.root]
        ls = []
        while len(q) > 0:
            currElem = q.pop(0)
            ls.append(currElem)
            # print(id(currElem))

            if currElem.right:
                q.append(currElem.right)

            if currElem.left:
                q.append(currElem.left)
        return ls

    def invert(self, root):
        if root is None:
            return None

        # Do dfs
        root.left, root.right = root.right, root.left
        self.invert(root.left)
        self.invert(root.right)

    def delete_node(self, root, key):
        if root is not None:
            if key > root.data:
                root.right = self.delete_node(root.right, key)
            elif key < root.data:
                root.left = self.delete_node(root.left, key)
            else:
                if not root.left and not root.right:
                    return None
                elif not root.left and root.right:
                    return root.right
                elif root.left and not root.right:
                    return root.left
                else:
                    # get the inorder successor
                    node = root.right
                    while node.left is not None:
                        node = node.left
                    root.data = node.data
                    root.right = self.delete_node(root.right, node.data)
            return root

    def deleteNode(self, root, key):
        return self.delete_node(root, key)

    def graphviz(self, nodes, *args, **kwargs):  # pragma: no cover
        if "node_attr" not in kwargs:
            kwargs["node_attr"] = {
                "shape": "record",
                "style": "filled, rounded",
                "color": "lightgray",
                "fillcolor": "lightgray",
                "fontcolor": "black",
            }
        digraph = Digraph(*args, **kwargs)

        for node in nodes:
            node_id = str(id(node))

            digraph.node(node_id, nohtml(f"<l>|<v> {node.data}|<r>"))

            if node.left is not None:
                digraph.edge(f"{node_id}:l", f"{id(node.left)}:v")

            if node.right is not None:
                digraph.edge(f"{node_id}:r", f"{id(node.right)}:v")

        return digraph


obj = BST()


def rerender():
    os.system("rm -rf ./static/Digraph")
    os.system("rm -rf ./static/Digraph.png")
    k = obj.bfs()
    k1 = obj.graphviz(k)
    k1.render(format="png", filename="./static/Digraph")


@app.route("/", methods=["GET", "POST"])
def index():
    found = 0
    if request.args.get("found"):
        found = request.args.get("found")
        if bool(int(found)):
            return render_template("index.html", found=found)

    if request.method == "POST":
        cval = int(request.form["create"])
        # print(cval)
        obj.insert(cval)
        return redirect("/")

    else:
        if obj.root is not None:
            rerender()
        else:
            rerender()

        return render_template("index.html")


@app.route("/reset", methods=["POST"])
def reset():
    obj.root = None
    rerender()
    return redirect("/")


@app.route("/invert", methods=["POST"])
def invert():
    obj.invert(obj.root)
    rerender()
    return redirect("/")


@app.route("/find", methods=["POST"])
def find():
    cval = int(request.form["find"])
    res = obj.search(obj.root, cval)
    found = int(res)
    return redirect(url_for("index", found=found))


@app.route("/delete", methods=["POST"])
def delete():

    if request.method == "POST":
        cval = int(request.form["delete"])
        obj.deleteNode(obj.root, cval)
        return redirect("/")

    else:
        if obj.root is not None:
            rerender()
        else:
            rerender()

        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
