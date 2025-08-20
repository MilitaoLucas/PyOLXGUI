from copy import copy, deepcopy
from dataclasses import dataclass, asdict
from typing import Optional, Iterable, Union, Dict
from dominate.tags import *
from dominate.util import raw
from dominate.tags import comment
from mistune.helpers import HTML_TAGNAME
from rich.console import Console
from html2text import html2text
SPACING = 4

def to_dict(obj, exclude_fields = None):
    if exclude_fields is None:
        exclude_fields = []
    result = dict()
    for key, value in obj.__dict__.items():
        if key in exclude_fields:
            continue
        result[key] = value

    return result

def add_default(pardict, kwargs):
    for k in pardict:
        if k in kwargs:
            pardict[k] = kwargs[k]
    return pardict

def include_comment(name: str, path: str, other_pars: Optional[Iterable[str]] = None, **kwargs):
    pars = []
    for key, value in kwargs.items():
        pars.append(f"{key}={value}")

    if not other_pars is None:
        for i in other_pars:
            if not '=' in i:
                pars.append(i)
            else:
                pars.insert(0, i)
    final_str = f"{path};" + ";".join(pars)
    return comment(f" #include {name} {final_str} ", **kwargs)

def text_bold(text: str, width: str="100%", align: str="center"):
    return td({"width": width, "align": align}, b(text))


class ignore(html_tag):
    """
    Represents an <ignore> custom HTML tag.
    """
    tagname = 'ignore'

def input_button(name: str, value: str, onclick: str, height: str = "20", type: str = "button", **kwargs):
    return input_(type=type, name=name, value=value, height=height, onclick=onclick, bgcolor="#8C8C8F",
              fgcolor="#ffffff", fit="false", flat="GetVar(linkButton.flat)", disabled="false",
              custom="GetVar(custom_button)",  **kwargs)

def text_input(name: str, value: str = "", label: str = "",
               height: str = "GetVar('HtmlInputHeight')", manage: str = "false",
               password: str = "false", multiline: str = "false", disabled: str = "false",
               bgcolor: str = "GetVar('HtmlInputBgColour')",
               fgcolor: str = "GetVar(HtmlFontColour)", onchange: str = "",
               onleave: str = "", onreturn: str = "", **kwargs):
    """
    Creates a text input element using dominate tags.
    """
    # with font(size="$GetVar('HtmlFontSizeControls')") as font_element:
    font_element = input_(
            type="text",
            height=height,
            bgcolor=bgcolor,
            fgcolor=fgcolor,
            valign="center",
            name=name,
            label=label,
            value=value,
            onchange=onchange,
            onleave=onleave,
            onreturn=onreturn,
            manage=manage,
            password=password,
            multiline=multiline,
            disabled=disabled,
            **kwargs
        )
    return font_element

class LabeledGeneralComponent(td):
    """
    Use label_left = True to change the label position.
    """
    tagname = "td"
    def __init__(self, inp: html_tag, txt_label: Optional[Union[str, html_tag]] = None, label_left=False, **kwargs):
        if not kwargs:
            kwargs = {"cellpadding": "2",  "cellspacing": "0"}
        super().__init__()
        self.label_left = label_left
        self.tr = tr(valign="middle")
        self.td_input = td(valign="middle")
        self.font = font(size="$GetVar('HtmlFontSizeControls')", valign="middle")
        self.input = inp
        if not txt_label is None:
            self._add_label(txt_label)

        self.font.add(self.input)
        self.td_input.add(self.input)

        self.table = table(kwargs)
        self.table.add(self.tr)
        self.add(self.table)

    def _add_label(self, txt_label: Union[str, html_tag]):
        self.td_label = td(align="left", valign="middle")
        if isinstance(txt_label, str):
            self.label = b(txt_label)
        else:
            self.label = txt_label
        self.td_label.add(self.label)
        if self.label_left:
            self.tr.add(self.td_label)
            self.tr.add(self.td_input)
        else:
            self.tr.add(self.td_input)
            self.tr.add(self.td_label)

    def _repr_html_(self):
        return str(self)

class InputCheckbox(LabeledGeneralComponent):
    """
    Use label_left = True to change the label position.
    """
    def __init__(self, name: str, txt_label: Union[str, html_tag] = "", label_left=False, **kwargs):
        pardict = dict(name=name,
                       type="checkbox",
                       height=20,
                       width=0,
                       fgcolor="GetVar(HtmlFontColour)",
                       bgcolor="GetVar(HtmlTableBgColour)",
                       valign="middle"
                       )
        pardict = add_default(pardict, kwargs)
        self.input = input_(pardict)
        super().__init__(self.input, txt_label, label_left)

class ComboBox(LabeledGeneralComponent):
    """
    Use label_left = True to change the label position.
    """
    def __init__(self, name: str, txt_label: Union[str, html_tag] = "", label_left=False, **kwargs):
        pardict = dict(
            name=name,
            type="combo",
            height="GetVar(HtmlComboHeight)",
            readonly="true",
            fgcolor="GetVar(HtmlFontColour)",
            bgcolor="GetVar(HtmlInputBgColour)",
            valign="middle"
        )
        pardict = add_default(pardict, kwargs)
        self.input = input_(pardict)
        super().__init__(self.input, txt_label, label_left)

class Button(LabeledGeneralComponent):
    def __init__(self, name: str, **kwargs):
        pardict = dict(
            name=name,
            type="button",
            value="#value",
            width="100%",
            onclick="#onclick",
            bgcolor="#bgcolor",
            fgcolor="#fgcolor",
            fit="false",
            flat="fasle",
            disabled="false",
        )
        pardict = add_default(pardict, kwargs)
        self.input = input_(pardict)
        super().__init__(self.input)




