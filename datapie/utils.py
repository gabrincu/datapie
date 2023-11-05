from textual.widgets import DataTable
import csv


def export_to_csv(table: DataTable, path: str):
    """
    Export a Textual DataTable to a CSV file in the path specified
    """
    rows_data = []
    columns = []
    for column_key, column in table.columns.items():
        columns.append(column.label)

    for key in table.rows:
        row_data = table.get_row(key)
        rows_data.append(row_data)

    with open(path, mode="w") as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(columns)
        csv_writer.writerows(rows_data)
