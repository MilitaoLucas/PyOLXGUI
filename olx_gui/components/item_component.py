from copy import copy, deepcopy
from dataclasses import dataclass, asdict
from typing import Optional, Iterable, Union, Dict
from dominate.tags import *
from dominate.util import raw
from dominate.tags import comment
from mistune.helpers import HTML_TAGNAME
from rich.console import Console
from html2text import html2text
from icecream import ic
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
        if k not in kwargs:
            kwargs[k] = pardict[k]
    return kwargs

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




def verify_functions(args: dict) -> None:
    args2 = {k: str(v).strip() for k, v in args.items()}
    for k, v in args2.items():
        if v.startswith("spy") or v.startswith("snum"):
            if v.count("(") != v.count(")"):
                raise ValueError(f"Olex2 functions have to be closed to be valid. {k} contains an invalid amount of "
                                 f"brackets.")


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
        input_width = "100%"
        if "input_width" in kwargs:
            input_width = kwargs["input_width"]
            kwargs.pop("input_width")

        self.td = td(valign="middle", width=input_width)
        self.font = font(size="$GetVar('HtmlFontSizeControls')", valign="middle")
        self.input = inp
        if not txt_label is None:
            self._add_label(txt_label)
        verify_functions(kwargs)
        self.font.add(self.input)
        self.td.add(self.label, self.input)
        self.tr.add(self.td)
        self.table = table(kwargs)
        self.table.add(self.tr)
        self.add(self.table)

    def _add_label(self, txt_label: Union[str, html_tag]):
        if isinstance(txt_label, str):
            self.label = b(txt_label)
        else:
            self.label = txt_label

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
                       fgcolor="GetVar(HtmlFontColour)",
                       bgcolor="GetVar(HtmlTableBgColour)",
                       valign="middle",
                       )
        verify_functions(kwargs)
        tdwidth = None
        if "tdwidth" in kwargs:
            tdwidth = kwargs["tdwidth"]
            kwargs.pop("tdwidth")
        pardict = add_default(pardict, kwargs)
        self.input = input_(pardict)
        super().__init__(self.input, txt_label, label_left)
        if not tdwidth is None:
            self["width"] = tdwidth

class ComboBox(LabeledGeneralComponent):
    """
    Use label_left = True to change the label position.
    """
    def __init__(self, name: str, txt_label: Union[str, html_tag] = "", label_left=False, **kwargs):
        pardict = dict(
            name=name,
            type="combo",
            width="100%",
            height="GetVar(HtmlComboHeight)",
            readonly="true",
            fgcolor="GetVar(HtmlFontColour)",
            bgcolor="GetVar(HtmlInputBgColour)",
            valign="middle"
        )
        verify_functions(kwargs)
        tdwidth = None
        if "tdwidth" in kwargs:
            tdwidth = kwargs["tdwidth"]
            kwargs.pop("tdwidth")
        pardict = add_default(pardict, kwargs)
        self.input = input_(pardict)
        super().__init__(self.input, txt_label, label_left)
        if not tdwidth is None:
            self["width"] = tdwidth

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
        verify_functions(kwargs)
        tdwidth = None
        if "tdwidth" in kwargs:
            tdwidth = kwargs["tdwidth"]
            kwargs.pop("tdwidth")
        pardict = add_default(pardict, kwargs)
        self.input = input_(pardict)
        super().__init__(self.input)

        if not tdwidth is None:
            self["width"] = tdwidth


class InputText(LabeledGeneralComponent):
    def __init__(self, name: str, txt_label: Union[str, html_tag] = "", label_left=False, **kwargs):
        pardict = dict(
            name = name,
            height = "GetVar('HtmlInputHeight')",
            manage = "false",
            password = "false",
            multiline = "false",
            disabled = "false",
            bgcolor = "GetVar('HtmlInputBgColour')",
            fgcolor = "GetVar(HtmlFontColour)",
            value = "#value",
            width = "100%",
            onclick = "#onclick",
            fit = "false",
            flat = "fasle",
            type = "text",
            valign = "center",
        )
        verify_functions(kwargs)
        tdwidth = None
        if "tdwidth" in kwargs:
            tdwidth = kwargs["tdwidth"]
            kwargs.pop("tdwidth")
        pardict = add_default(pardict, kwargs)
        self.input = input_(pardict)
        super().__init__(self.input, txt_label, label_left)
        if not tdwidth is None:
            self["width"] = tdwidth

class InputSpinner(LabeledGeneralComponent):
    def __init__(self, name: str, txt_label: Union[str, html_tag] = "", label_left=False, **kwargs):
        pardict = dict(
            type="spin",
            height="GetVar('HtmlComboHeight')",
            bgcolor="GetVar(HtmlInputBgColour)",
            fgcolor="GetVar(HtmlFontColour)",
            valign="center",
            min="-1000",
            max="1000",
            name=name,
            width="100%",
            setdefault="false",
            disabled="false",
            readonly="false",
            onchangealways="false",
            manage="false",
            custom="arrow_width: -10",
        )
        verify_functions(kwargs)
        tdwidth = None
        if "tdwidth" in kwargs:
            tdwidth = kwargs["tdwidth"]
            kwargs.pop("tdwidth")
        pardict = add_default(pardict, kwargs)
        self.input = input_(pardict)
        super().__init__(self.input, txt_label, label_left)
        if not tdwidth is None:
            self["width"] = tdwidth
