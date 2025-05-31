from dataclasses import dataclass, asdict, field
import dominate
from dominate.tags import *
from typing import List, Optional, Union, Any
import copy

from tests import tr1_parameters
from .item_component import BaseItemComponent, SPACING

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
    
class Table:
    """
    Dynamic table generator for Olex2 GUI framework.
    Creates HTML tables based on lists of components.
    """
    def __init__(self,
                 rows: List[List[Union[BaseItemComponent, str]]],
                 header: Optional[List[str]] = None,
                 spacing: int = SPACING,
                 tr_attributes: dict = None,
                 table_attributes: dict = None,
                 **kwargs):
        self.rows = rows
        self.header = header

        self.spacing = spacing
        self.kwargs = kwargs

    def generate_table_header(self):
        """Generate the HTML table header if provided."""
        if not self.header:
            return ""

        header_str = f"{self.spacing*" "}<tr{self.generate_attributes(self.tr_attributes)}>\n"
        for h in self.header:
            header_str += f"{self.spacing*" "}  <th>{h}</th>\n"
        header_str += f"{self.spacing*" "}</tr>\n"
        return header_str

    def generate_table_rows(self):
        """Generate all table rows from the component lists."""
        rows_str = ""
        for row in self.rows:
            rows_str += f"{self.spacing*" "}<tr>\n"
            for cell in row:
                spacing = 2*self.spacing*" "
                if isinstance(cell, BaseItemComponent):
                    rows_str += f"<td>\n"
                    # Copy the component to avoid modifying the original
                    # Adjust spacing to match the table indentation
                    cell.spacing = 3*self.spacing
                    rows_str += str(cell)
                    rows_str += f"\n{2*self.spacing*" "}</td>\n"
                else:
                    rows_str += "\n".join([spacing + c for c in cell.split("\n")])
            rows_str += f"{self.spacing*" "}</tr>\n"
        return rows_str

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
        attr_str = self.generate_attributes(self.table_attributes)
        table_str = f"<table{attr_str}>\n"

        # Add header if provided
        header_str = self.generate_table_header()
        if header_str:
            table_str += header_str

        # Add rows
        table_str += self.generate_table_rows()

        # Close table
        table_str += f"</table>"

        return table_str

    def __repr__(self):
        return self.__str__()


@dataclass
class SimpleTable:
    """
    A simple dataclass-based table implementation that follows the BaseItemComponent pattern.
    This is useful for creating basic tables with minimal configuration.
    """
    rows: List[List[Union[BaseItemComponent, str]]]
    header: List[str] = field(default_factory=list)
    table_class: str = ""
    table_id: str = ""
    table_style: str = ""
    border: str = ""
    cellpadding: str = ""
    cellspacing: str = ""
    width: str = ""
    spacing: int = SPACING
    table_attributes: dict = field(default_factory=dict)
    tr_attributes: dict = field(default_factory=dict)

    def __post_init__(self):
        self.table = Table(
            rows=self.rows,
            header=self.header,
            table_class=self.table_class,
            table_id=self.table_id,
            table_style=self.table_style,
            border=self.border,
            cellpadding=self.cellpadding,
            cellspacing=self.cellspacing,
            width=self.width,
            spacing=self.spacing,
            tr_attributes = self.tr_attributes,
            table_attributes =  self.table_attributes,
        )

    def __str__(self):
        return str(self.table)

    def __repr__(self):
        return self.__str__()


# Example specialized table implementations
@dataclass
class DataTable(SimpleTable):
    """
    A data table with styling suitable for displaying data.
    """
    def __post_init__(self):
        if not self.table_class:
            self.table_class = "data-table"
        if not self.border:
            self.border = "1"
        if not self.cellpadding:
            self.cellpadding = "3"
        super().__post_init__()


@dataclass
class FormTable(SimpleTable):
    """
    A table designed for form layouts with components.
    """
    def __post_init__(self):
        if not self.table_class:
            self.table_class = "form-table"
        if not self.cellpadding:
            self.cellpadding = "2"
        super().__post_init__()
