from dataclasses import dataclass, asdict, field
import dominate
from dominate.tags import *
from dominate.util import raw, text
from typing import List, Optional, Union, Any
import copy

from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import TerminalFormatter
from .item_component import BaseItemComponent, SPACING, IncludeComment

from bs4 import BeautifulSoup
LEXER = HtmlLexer()
FORMATTER = TerminalFormatter()


@dataclass
class TableConfig:
    """
    A table compiles to something like this:
    <tr ALIGN='left' NAME='SNUM_REFINEMENT_NSFF' width='100%'> <!-- configurable with tr1_parameters, this being the default -->
        <td colspan="#colspan> <!-- configurable with td1_parameters -->
          <table border="0" width="100%" cellpadding="0" cellspacing="0" Xbgcolor="#ffaaaa"> <!-- configurable with table1_parameters -->
            <tr Xbgcolor="#ffffaa"> <!-- configurable with tr2_parameters -->
              <td width='#width%' align='left'> <!-- configurable with td2_parameters -->
                <table width='100%'cellpadding="0" cellspacing="2"> <!-- configurable with table2_parameters -->
                  <tr bgcolor="GetVar(HtmlTableGroupBgColour)"> <!-- configurable with tr3_parameters -->
                      <!-- Any content -->
                  </tr>
              </td>
            </tr>
          </table>
        </td>
    </tr>
    """
    tr1_parameters: Optional[dict] = None
    td1_parameters: Optional[dict] = None
    table1_parameters: Optional[dict] = None
    tr2_parameters: Optional[dict] = None
    td2_parameters: Optional[dict] = None
    table2_parameters: Optional[dict] = None
    tr3_parameters: Optional[dict] = None
    
    def __post_init__(self):
        if self.tr1_parameters is None:
            self.tr1_parameters = {"ALIGN": "left", "NAME": "NAME", "width": "100%"}
        
        if self.td1_parameters is None:
            self.td1_parameters = {"colspan": "#colspan"}
            
        if self.table1_parameters is None:
            self.table1_parameters = {"border": "0", "width": "100%", "cellpadding": "0", "cellspacing": "0", "Xbgcolor": "#ffaaaa"}
        
        if self.tr2_parameters is None:
            self.tr2_parameters = {"Xbgcolor": "#ffffaa"}
        
        if self.td2_parameters is None:
            self.td2_parameters = {"width": "#width%", "align": "left"}
        
        if self.table2_parameters is None:
            self.table2_parameters = {"width": "100%", "cellpadding": "0", "cellspacing": "2"}

        if self.tr3_parameters is None:
            self.tr3_parameters = {"bgcolor": "GetVar(HtmlTableGroupBgColour)"}
    
class Table:
    """
    Dynamic table generator for Olex2 GUI framework.
    Creates HTML tables based on lists of components.
    """
    def __init__(self,
                 rows: List[List[Union[BaseItemComponent, IncludeComment, str]]],
                 header: Optional[List[str]] = None,
                 config: TableConfig = TableConfig(),
                 **kwargs):
        self.rows = rows
        self.config = config
        self.header = header
        self.kwargs = kwargs
        self.structures = []
        self.generate_table_rows()

    def apply_structure(self, comp):
        fel = tr(self.config.tr1_parameters)
        fel.add(td(self.config.td1_parameters,
                   table(self.config.table1_parameters,
                         tr(self.config.tr2_parameters,
                            td(self.config.td2_parameters,
                               table(self.config.table2_parameters, comp))))))

        return fel

    def apply_row(self, row):
        with tr(self.config.tr3_parameters) as row_app:
            for cell in row:
                if isinstance(cell, BaseItemComponent):
                    raw("\n" + str(cell) + "\n")
                elif isinstance(cell, IncludeComment):
                    raw("\n" + str(cell) + "\n")
                else:
                    row_app.add(cell)

        return row_app

    def generate_table_rows(self):
        """Generate all table rows from the component lists."""
        for row in self.rows:
            self.structures.append(self.apply_structure(self.apply_row(row)))

    @staticmethod
    def generate_attributes(attr_dict: dict):
        """Generate HTML table attributes."""
        attr_str = ""
        for key, value in attr_dict.items():
            if value:  # Only add non-empty attributes
                attr_str += f" {key}=\"{value}\""
        return attr_str

    def __str__(self):
        """Generate the complete HTML table."""
        html = "".join(str(structure) for structure in self.structures)
        pretty_html = BeautifulSoup(html, 'html.parser').prettify()
        return pretty_html

    def raw_str(self):
        return "".join(str(structure) for structure in self.structures)

    def __repr__(self):
        return highlight(str(self.__str__()), LEXER, FORMATTER)
