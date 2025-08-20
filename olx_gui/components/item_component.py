from copy import copy, deepcopy
from dataclasses import dataclass, asdict
from typing import Optional, Iterable, Union
from dominate.tags import *
from dominate.util import raw
from dominate.tags import comment
from mistune.helpers import HTML_TAGNAME
from rich.console import Console
from html2text import html2text
SPACING = 4

class BaseItemComponent:
    def __init__(self, snippet: str, spacing: int = SPACING, td_comp: Optional[dict] = None, disable_td: bool = False,
                 **kwargs):
        self.parameters = dict()
        self.snippet_path = snippet
        self.spacing: int = spacing
        self.disable_td = disable_td
        self.exclude_fields = ["td_comp", "disable_td"]
        self.td_comp = td_comp if not td_comp is None else {"width":"1%", "align":"left"}

    @property
    def dominate(self):
        ident_str = [self.spacing * " " + i for i in self.__str__().split("\n")]
        ident_str = "\n".join(ident_str)
        if not self.disable_td:
            with td(self.td_comp) as htmobj:
                raw("\n" + ident_str + "\n")
        else:
            htmobj = raw("\n" + ident_str + "\n")
        return htmobj

    def add_paramater(self, param: dict) -> None:
        if not type(param) is dict:
            raise TypeError("Parameter must be a dictionary")
        if len(param.keys()) != 1:
            raise ValueError("Parameter must have one key")
        self.parameters.update(param)

    def make_str_snippet(self):
        spacing = self.spacing * " "
        str_s = f"$+\n" + f"{spacing}html.Snippet(\n"
        str_s += f"{2*spacing}\"{self.snippet_path}\",\n"
        for k,v in self.parameters.items():
            if len(v) == 0: continue
            str_s += f"{2*spacing}\"{k}={v}\",\n"
        str_s += f"{spacing})\n$-"
        return str_s

    @staticmethod
    def generate_attributes(attr_dict: dict):
        """Generate HTML table attributes."""
        attr_str = ""
        for key, value in attr_dict.items():
            if value:  # Only add non-empty attributes
                attr_str += f" {key}=\"{value}\""
        return attr_str

    def __str__(self):
        return self.make_str_snippet()

    def __repr__(self):
        return self.make_str_snippet()

class TestComponent(BaseItemComponent):
    def __init__(self, **kwargs):
        super().__init__("gui/snippets/input-combo", **kwargs)
        self.add_paramater({"name":"NoSpherA2_cpus@refine"})
        self.add_paramater({"items":"spy.NoSpherA2.getCPUListStr()"})
        self.add_paramater({"value":"spy.GetParam('snum.NoSpherA2.ncpus')"})
        self.add_paramater({"onchange": "spy.SetParam('snum.NoSpherA2.ncpus', html.GetValue('~name~'))"})

class GeneralComponent(BaseItemComponent):
    def __init__(self, snippet: str, spacing: int = SPACING, **kwargs):
        par_dict = dict()
        for key, value in kwargs.items():
            par_dict.update({key: value})
        if "phil" in par_dict:
            if not "onchange" in par_dict:
                par_dict["onchange"] = f"spy.SetParam('{par_dict["phil"]}',html.GetValue('~name~'))"
            if not "value" in par_dict:
                par_dict["value"] = f"spy.GetParam('{par_dict["phil"]}')"
        super().__init__(snippet, spacing = spacing, **kwargs)
        par_dict_bak = copy(par_dict)
        for i in tuple(par_dict.keys()):
            if i in self.exclude_fields:
                par_dict_bak.pop(i)
        par_dict = par_dict_bak
        self.parameters = par_dict

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

class ComboBoxComponent(GeneralComponent):
    def __init__(self, name: str, items: Union[str, Iterable[str]], **kwargs):
        if "phil" in kwargs:
            phil = kwargs["phil"]
            kwargs["value"] = f"spy.GetParam('{phil}')"
            kwargs["onchange"] = f"spy.SetParam('{phil}',html.GetValue('~name~'))"
            kwargs.pop("phil")
        kwargs["name"] = name
        kwargs["items"] = items
        super().__init__("gui/snippets/input-combo", **kwargs)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

def to_dict(obj, exclude_fields = None):
    if exclude_fields is None:
        exclude_fields = []
    result = dict()
    for key, value in obj.__dict__.items():
        if key in exclude_fields:
            continue
        result[key] = value

    return result

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

# TODO: Make every component as good as this one
class InputCheckbox(td):
    """
    Use label_left = True to change the label position.
    """
    tagname = "td"
    def __init__(self, name: str, txt_label: Union[str, html_tag] = "", label_left=False, **kwargs):
        if not kwargs:
            kwargs = {"cellpadding": "2",  "cellspacing": "0"}
        super().__init__()
        self.tr = tr(valign="middle")
        self.td_input = td(valign="middle")
        self.font = font(size="$GetVar('HtmlFontSizeControls')", valign="middle")
        self.input = input_(type="checkbox", height=20, width=0, fgcolor="GetVar(HtmlFontColour)",
                            bgcolor="GetVar(HtmlTableBgColour)", name=name, valign="middle"
                            )
        self.td_label = td(align="left", valign="middle")
        if isinstance(txt_label, str):
            self.label = b(txt_label)
        else:
            self.label = txt_label
        self.font.add(self.input)
        self.td_input.add(self.input)
        self.td_label.add(self.label)
        if label_left:
            self.tr.add(self.td_label)
            self.tr.add(self.td_input)
        else:
            self.tr.add(self.td_input)
            self.tr.add(self.td_label)
        self.table = table(kwargs)
        self.table.add(self.tr)
        self.add(self.table)

    def _repr_html_(self):
        return str(self)

class LabeledGeneralComponent(td):
    """
    Use label_left = True to change the label position.
    """
    tagname = "td"
    def __init__(self, inp: html_tag, txt_label: Union[str, html_tag] = "",  label_left=False, **kwargs):
        if not kwargs:
            kwargs = {"cellpadding": "2",  "cellspacing": "0"}
        super().__init__()
        self.tr = tr(valign="middle")
        self.td_input = td(valign="middle")
        self.font = font(size="$GetVar('HtmlFontSizeControls')", valign="middle")
        self.input = inp
        self.td_label = td(align="left", valign="middle")
        if isinstance(txt_label, str):
            self.label = b(txt_label)
        else:
            self.label = txt_label
        self.font.add(self.input)
        self.td_input.add(self.input)
        self.td_label.add(self.label)
        if label_left:
            self.tr.add(self.td_label)
            self.tr.add(self.td_input)
        else:
            self.tr.add(self.td_input)
            self.tr.add(self.td_label)
        self.table = table(kwargs)
        self.table.add(self.tr)
        self.add(self.table)

    def _repr_html_(self):
        return str(self)

class InputCheckbox2(LabeledGeneralComponent):
    """
    Use label_left = True to change the label position.
    """
    def __init__(self, name: str, txt_label: Union[str, html_tag] = "", label_left=False, **kwargs):
        if not kwargs:
            kwargs = {"cellpadding": "2",  "cellspacing": "0"}

        self.input = input_(type="checkbox", height=20, width=0, fgcolor="GetVar(HtmlFontColour)",
                bgcolor="GetVar(HtmlTableBgColour)", name=name, valign="middle"
                )
        super().__init__(self.input, txt_label, label_left, **kwargs)

    def _repr_html_(self):
        return str(self)

class ComboBox(LabeledGeneralComponent):
    """
    Use label_left = True to change the label position.
    """
    def __init__(self, name: str, txt_label: Union[str, html_tag] = "", label_left=False, **kwargs):
        if not kwargs:
            kwargs = {"cellpadding": "2",  "cellspacing": "0"}

        self.input = input_(type="combo", height="GetVar(HtmlComboHeight)", readonly="true", fgcolor="GetVar(HtmlFontColour)",
                bgcolor="GetVar(HtmlInputBgColour)", name=name, valign="middle"
                )
        super().__init__(self.input, txt_label, label_left, **kwargs)

    def _repr_html_(self):
        return str(self)
