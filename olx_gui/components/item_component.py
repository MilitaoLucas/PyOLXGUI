from copy import copy, deepcopy
from dataclasses import dataclass, asdict
from typing import Optional, Iterable, Union

from dominate.tags import *
from dominate.util import raw
from dominate.tags import comment
from mistune.helpers import HTML_TAGNAME

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
    final_str = f"{path};" + ";".join(other_pars)
    return comment(f" #include {name} {final_str} ", **kwargs)

def text_bold(text: str, width: str="100%", align: str="center"):
    return td({"width": width, "align": align}, b(text))


class ignore(html_tag):
    """
    Represents an <ignore> custom HTML tag.
    """
    tagname = 'ignore'