from textual.widgets import DataTable


def build_query():
    """
    This should build queries using the keys and changes list that results from the diff_tables.
    Should use sqlglot library
    """

def diff_tables(initial_table: DataTable, updated_table: DataTable):
    """
    Make diff between tables, this should result in a dict of changes that have been made from the initial table and the changed ones.
    It should look like:
    {
        "delete": RowKey(), or []
        "insert": RowData(asdsd, slslsls, dddd), or []
        "updated": {
            key: RowKey(),
            updated_cols: {
                col1: 2,
                col2: "new_value"
                }
            }
    }
    """
    initial_rows = initial_table.rows
    updated_rows = updated_table.rows

    pass
