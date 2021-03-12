from typing import List
from beautifultable import BeautifulTable


def make_table(header: List[str], content: List[List[str]]):
    table = BeautifulTable()
    table.columns.header = header
    for row in content:
        table.rows.append(row)
    table.set_style(BeautifulTable.STYLE_BOX_ROUNDED)
    return str(table)
