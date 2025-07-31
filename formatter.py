from prettytable import PrettyTable

def format_table(results, headers):
    table = PrettyTable()
    table.field_names = headers
    for row in results:
        table.add_row(row)
    print(table)
    return table.get_string()
from prettytable import PrettyTable

