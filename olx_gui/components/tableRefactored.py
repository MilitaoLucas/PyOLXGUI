from dataclasses import dataclass, asdict, field
import dominate
from dominate.tags import *
from dominate.util import raw, text, unescape
from typing import List, Optional, Union, Any
import copy
from icecream import ic
from .table import TableConfig, Table
from pygments import highlight
from pygments.lexers import HtmlLexer
from pygments.formatters import TerminalFormatter
from .item_component import BaseItemComponent, SPACING, include_comment, ignore
IC = include_comment
from bs4 import BeautifulSoup
LEXER = HtmlLexer()
FORMATTER = TerminalFormatter()

class Line(tr):
    """
    A line consists of a single table containing help information.
    """
    tagname = "tr"
    def __init__(self, name: str, help_ext: Optional["str"]="#help_ext", **kwargs):
        self.help_ext = help_ext
        super().__init__(**kwargs)
        if "config" in kwargs and isinstance(kwargs["config"], TableConfig):
            self.config = kwargs["config"]
        else:
            self.config = TableConfig()
        self.config.tr1_parameters["NAME"] = name
        for key, value in self.config.tr1_parameters.items():
            self[key] = value
        self.add(include_comment("tool-help-first-column", r"gui\blocks\tool-help-first-column.htm", help_ext=help_ext, other_pars=["1"]))
        self.td1 = td(self.config.td1_parameters)
        self.table1 = table(self.config.table1_parameters)
        self.tr2 = tr(self.config.tr2_parameters)
        self.td2 = td(self.config.td2_parameters)
        self.table2 = table(self.config.table2_parameters)
        self.tr3 = tr(self.config.tr3_parameters)
        self.table2.add(self.tr3)
        self.td2.add(self.table2)
        self.tr2.add(self.td2)
        self.table1.add(self.tr2)
        self.td1.add(self.table1)
        self.add(self.td1)

    @property
    def pretty(self):
        return highlight(str(self), LEXER, FORMATTER)

    def _repr_html_(self):
        return str(self)

class H3Section:
    """This represents a group of Line's that form a section in the GUI. One example is the NoSpherA2 Options section."""
    def __init__(self):
        self.lines: List[Union[Line, comment]] = []
        inc_comment = include_comment("tool-h3", r"gui\blocks\tool-h3.htm", ["1"],
                                               image="#image", colspan="1")
        self.lines.append(inc_comment)

    def add(self, line: Line):
        self.lines.append(line)

    def __str__(self):
        strs = ""
        for line in self.lines:
            strs += "\n" + str(line)
        return strs

    def html_preview(self, highlighting: bool = True):
        """Previews the entire HTML of the section
        """
        if highlighting:
            print(highlight(str(self), LEXER, FORMATTER))
        else:
            print(str(self))

    @property
    def include_comment(self):
        return self.lines[0]

    @include_comment.setter
    def include_comment(self, ic_comment: comment):
        if isinstance(ic_comment, comment):
            self.lines[0] = ic_comment
        else:
            raise TypeError("The comment should be of type comment.")

    def _repr_html_(self):
        return str(self)
