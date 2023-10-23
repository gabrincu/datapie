from textual.widgets import Tree, Static
from textual.app import ComposeResult
from rich.console import RenderableType
from textual.message import Message
from textual import log, on, events


#TODO: use reactive attribute for Tree query
class DbTree(Static):
    def __init__(
        self,
        db_connection,
        renderable: RenderableType = "",
        *,
        expand: bool = False,
        shrink: bool = False,
        markup: bool = True,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        super().__init__(
            renderable=renderable,
            expand=expand,
            shrink=shrink,
            markup=markup,
            name=name,
            id=id,
            classes=classes,
            disabled=disabled,
        )
        self.connection = db_connection
        cursor = self.connection.cursor()
        self.table_names = cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        ).fetchall()

    class ExploreTable(Message):
        def __init__(self, node, query):
            super().__init__()
            self.node = node
            self.query = query

    def compose(self) -> ComposeResult:
        log(self.table_names)
        tree: Tree[dict] = Tree("Public")
        tables = tree.root.add("Tables", expand=True)
        for table in self.table_names:
            tables.add_leaf(table[0])
        yield tree

    @on(Tree.NodeSelected)
    def node_selected(self, event: Tree.NodeSelected):
        if not event.node.is_root:
            query = f"Select * from {event.node.label} limit 20;"
            self.post_message(self.ExploreTable(event.node, query))
    
    @on(events.Focus)
    def on_focus(self, event: events.Focus):
        print("merge tree")
        self.add_class("focused")

