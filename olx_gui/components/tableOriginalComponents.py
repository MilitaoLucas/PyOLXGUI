from dataclasses import dataclass, asdict, field
import dominate
from dominate.tags import *
from dominate.util import raw, text, unescape
from typing import List, Optional, Union, Any
import copy
from .table import TableConfig, Table
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import TerminalFormatter
from .item_component import BaseItemComponent, SPACING, include_comment, ignore
IC = include_comment
from bs4 import BeautifulSoup
LEXER = HtmlLexer()
FORMATTER = TerminalFormatter()

class TableOriginal(Table):
    """
    A table with the original balanced components. A tr element is optional and can be provided to wrap the table (in
    TableConfig). It uses TableConfig from table.py to define the structure of the table.
    """
    def __init__(self, help_ext: Optional["str"]="#help_ext", **kwargs):
        self.help_ext = help_ext
        super().__init__(**kwargs)

    def apply_structure(self, comp):
        if self.comment_obj:
            fel = tr(self.config.tr1_parameters, self.comment_obj)
        else:
            fel = tr(self.config.tr1_parameters)
        fel.add(
            IC("tool-help-first-column", r"gui\blocks\tool-help-first-column.htm",
               other_pars=[f"help_ext={self.help_ext}", "1"],),
            IC("row-table-on", r"gui\blocks\row_table_on.htm",
               other_pars=["1", f"colspan={self.config.td1_parameters["colspan"]}", f"width={self.config.td2_parameters["width"]}"]),
            comp,
            IC("td-table-off", r"gui\balanced\td-table-off.htm", other_pars=["1"])
        )
        print(fel)
        return fel

    def apply_row(self, row):
        group = div()
        with group as row_app:
            for cell in row:
                if isinstance(cell, BaseItemComponent):
                    raw("\n" + str(cell) + "\n")
                else:
                    row_app.add(cell)

        return row_app
