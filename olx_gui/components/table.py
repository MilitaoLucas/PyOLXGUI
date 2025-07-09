from dataclasses import dataclass, asdict, field
import dominate
from dominate.tags import *
from dominate.util import raw, text, unescape
from typing import List, Optional, Union, Any
import copy

from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import TerminalFormatter
from .item_component import BaseItemComponent, SPACING, include_comment, ignore

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
            <!-- those bellow are part of the TableGroup Class
              <td width='#width%' align='left'> <!-- configurable with td2_parameters --> 
                <table width='100%'cellpadding="0" cellspacing="2"> <!-- configurable with table2_parameters -->
                  <tr bgcolor="GetVar(HtmlTableGroupBgColour)"> <!-- configurable with tr3_parameters -->
                      <!-- Any content -->
                  </tr>
              </td>
            <!-- those above are part of the TableGroup Class
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
            self.td2_parameters = {"width": "100", "align": "left"}
        
        if self.table2_parameters is None:
            self.table2_parameters = {"width": "100%", "cellpadding": "0", "cellspacing": "2"}

        if self.tr3_parameters is None:
            self.tr3_parameters = {"bgcolor": "$GetVar(HtmlTableGroupBgColour)"}
    
class Table:
    """
    Dynamic table generator for Olex2 GUI framework.
    Creates HTML tables based on lists of components.
    """
    ignore_condition: str

    def __init__(self,
                 rows: List[List[Union[BaseItemComponent, html_tag, str]]],
                 header: Optional[List[str]] = None,
                 config: TableConfig = TableConfig(),
                 ignore_condition: Optional[str] = None,
                 comment_obj: Optional[html_tag] = None,
                 **kwargs):
        self.rows = rows
        self.config = config
        self.header = header
        self.kwargs = kwargs
        self.structures = []
        self.comment_obj = comment_obj
        self.ignore_tag = False

        if not ignore_condition is None:
            self.ignore_tag = True
            self.ignore_condition = ignore_condition
        self.generate_table_rows()

    def apply_structure(self, comp):
        if self.comment_obj:
            fel = tr(self.config.tr1_parameters, self.comment_obj)
        else: 
            fel = tr(self.config.tr1_parameters)
        fel.add(td(self.config.td1_parameters,
                   table(self.config.table1_parameters,
                         tr(self.config.tr2_parameters,
                            comp))))

        return fel
    
    def apply_group(self, comp):
        return td(self.config.td2_parameters,
                  table(self.config.table2_parameters, 
                        tr(self.config.tr3_parameters, comp)))

    def apply_row(self, row):
        group = td(self.config.td2_parameters).add(
                table(self.config.table2_parameters)).add( 
                        tr(self.config.tr3_parameters))
        with group as row_app:
            for cell in row:
                if isinstance(cell, BaseItemComponent):
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
        html = self.raw_str()            
        pretty_html = BeautifulSoup(str(html), 'html.parser').prettify().replace("&gt;", ">").replace("&lt;", "<")
        return pretty_html

    def raw_str(self):
        if not self.ignore_tag:
            html = copy.deepcopy(self.structures[0])
            for structure in self.structures[1:]:
                html.add(structure)
        else:
            html = ignore(test=f"{self.ignore_condition}")
            for structure in self.structures.copy():
                html.add(structure)
        return str(html)

    def __repr__(self):
        return highlight(str(self.__str__()), LEXER, FORMATTER)

class TableGroup():
    """
    This is supposed to imitate the behavior of group_begin.htm block. I want to do self contained blocks to avoid 
    errors.
    """
    pass