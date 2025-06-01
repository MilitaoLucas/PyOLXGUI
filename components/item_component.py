from dataclasses import dataclass, asdict
from typing import Optional, Iterable

from dominate.tags import *
from dominate.tags import comment
from mistune.helpers import HTML_TAGNAME

SPACING = 4

class BaseItemComponent:
    def __init__(self, snippet: str, spacing: int = SPACING, td_comp: Optional[dict] = None, **kwargs):
        self.parameters = dict()
        self.snippet_path = snippet
        self.spacing: int = spacing
        self.exclude_fields = ["spacing"]
        self.td_comp = td_comp if not td_comp is None else {"width":"1%", "align":"left"}


    def add_paramater(self, param: dict) -> None:
        if not type(param) is dict:
            raise TypeError("Parameter must be a dictionary")
        if len(param.keys()) != 1:
            raise ValueError("Parameter must have one key")
        self.parameters.update(param)

    def make_str_snippet(self):
        spacing = self.spacing * " "
        str_s = f"<td{self.generate_attributes(self.td_comp)}>\n{spacing}$+\n" + f"{spacing}html.Snippet(\n"
        str_s += f"{2*spacing}\"{self.snippet_path}\"\n"
        for k,v in self.parameters.items():
            if len(v) == 0: continue
            str_s += f"{2*spacing}\"{k}={v}\",\n"
        str_s += f"{spacing})\n{spacing}$-\n{spacing}</td>"
        return str_s

    @staticmethod
    def generate_attributes(attr_dict: dict):
        """Generate HTML table attributes."""
        attr_str = ""
        for key, value in attr_dict.items():
            if value:  # Only add non-empty attributes
                attr_str += f" {key}=\"{value}\""
        return attr_str

    def dict_factory(self, x):
        return {k: v for (k, v) in x if ((v is not None) and (k not in self.exclude_fields))}
    
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

@dataclass
class InputComboComponent(BaseItemComponent):
    name: str
    items: str
    value: str
    onchange: str = ""
    label: str = ""
    readonly: str = ""
    onchangealways: str = ""
    onleave: str = ""
    onreturn: str = ""
    onenter:str = ""
    width: str = ""
    height: str = ""
    manage: str = ""
    setdefault: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    disabled: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        super().__init__("gui/snippets/input-combo", spacing = spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class GuiLinkComponent(BaseItemComponent):
    value: str
    name: str = ""
    scope: str = ""
    width: str = ""
    height: str = ""
    fgcolor: str = ""
    disabled: str = ""
    fit: str = ""
    flat: str = ""
    onclick: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        if self.name == "": self.name = self.value
        super().__init__("gui/snippets/input-combo", spacing = spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class GuiLinkPlainComponent(BaseItemComponent):
    value: str
    hint: str = ""
    width: str = ""
    height: str = ""
    name: str = ""
    onclick: str = ""
    fit: str = ""
    focus: str = ""
    flat: str = ""
    disabled: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    custom: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        if self.name == "":
            self.name = self.value
        super().__init__("gui/snippets/gui-link-plain", spacing=spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()
    
@dataclass
class GuiLinkButtonComponent(BaseItemComponent):
    value: str
    hint: str = ""
    width: str = ""
    height: str = ""
    name: str = ""
    onclick: str = ""
    fit: str = ""
    focus: str = ""
    flat: str = ""
    disabled: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        if self.name == "":
            self.name = self.value
        super().__init__("gui/snippets/gui-link-button", spacing=spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class InputButtonComponent(BaseItemComponent):
    value: str
    name: str = ""
    width: str = ""
    height: str = ""
    onclick: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    fit: str = ""
    flat: str = ""
    hint: str = ""
    disabled: str = ""
    custom: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        if self.name == "": 
            self.name = self.value
        super().__init__("gui/snippets/input-button", spacing=spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class InputButtonTdComponent(BaseItemComponent):
    value: str
    name: str = ""
    width: str = ""
    height: str = ""
    onclick: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    fit: str = ""
    flat: str = ""
    hint: str = ""
    disabled: str = ""
    custom: str = ""
    td1: str = ""
    td2: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        super().__init__("gui/snippets/input-button-td", spacing=spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()
    

@dataclass
class InputCheckboxComponent(BaseItemComponent):
    name: str
    label: str = ""
    checked: str = ""
    oncheck: str = ""
    onuncheck: str = ""
    target: str = ""
    data: str = ""
    width: str = ""
    height: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    value: str = ""
    onclick: str = ""
    right: str = ""
    manage: str = ""
    disabled: str = ""
    custom: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        super().__init__("gui/snippets/input-checkbox", spacing=spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class InputCheckboxPlainComponent(BaseItemComponent):
    name: str
    label: str = ""
    checked: str = ""
    oncheck: str = ""
    onuncheck: str = ""
    width: str = ""
    height: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    value: str = ""
    onclick: str = ""
    right: str = ""
    manage: str = ""
    disabled: str = ""
    custom: str = ""
    target: str = ""
    data: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        super().__init__("gui/snippets/input-checkbox-plain", spacing=spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class InputCheckboxTdComponent(BaseItemComponent):
    name: str
    label: str = ""
    checked: str = ""
    oncheck: str = ""
    onuncheck: str = ""
    width: str = ""
    height: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    value: str = ""
    onclick: str = ""
    right: str = ""
    manage: str = ""
    disabled: str = ""
    custom: str = ""
    td1: str = ""
    td2: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        super().__init__("gui/snippets/input-checkbox-td", spacing=spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()
    

@dataclass
class InputComboTdComponent(BaseItemComponent):
    name: str
    items: str
    value: str
    onchange: str = ""
    label: str = ""
    readonly: str = ""
    onchangealways: str = ""
    onleave: str = ""
    onreturn: str = ""
    onenter:str = ""
    width: str = ""
    height: str = ""
    manage: str = ""
    setdefault: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    disabled: str = ""
    custom: str = ""   
    td1: str = ""
    td2: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        super().__init__("gui/snippets/input-combo-td", spacing=spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class InputLabelComponent(BaseItemComponent):
    value: str
    name: str = ""
    width: str = ""
    label: str = ""
    height: str = ""
    fgcolor: str = ""
    bgcolor: str = ""
    valign: str = ""
    halign: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        super().__init__("gui/snippets/input-label", spacing = spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class InputSliderComponent(BaseItemComponent):
    value: str
    name: str = ""
    width: str = ""
    height: str = ""
    manage: str = ""
    password: str = ""
    multiline: str = ""
    disabled: str = ""
    td1: str = ""
    td2: str = ""
    param: str = ""
    scale: str = ""
    min: str = ""
    max: str = ""
    cmd: str = ""
    swidth: str = ""
    invert: str = ""
    bgcolor: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        super().__init__("gui/snippets/input-slider", spacing = spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class InputSpinTdComponent(BaseItemComponent):
    value: str
    name: str = ""
    label: str = ""
    min: str = ""
    max: str = ""
    width: str = ""
    readonly: str = ""
    manage: str = ""
    onchangealways: str = ""
    setdefault: str = ""
    disabled: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    custom: str = ""
    td1: str = ""
    td2: str = ""
    onchange: str = ""
    onleave: str = ""
    onreturn: str = ""
    onenter: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        super().__init__("gui/snippets/input-spin-td", spacing = spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class InputTextComponent(BaseItemComponent):
    value: str
    name: str = ""
    label: str = ""
    width: str = ""
    height: str = ""
    manage: str = ""
    password: str = ""
    multiline: str = ""
    disabled: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    onchange: str = ""
    onleave: str = ""
    onreturn: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        super().__init__("gui/snippets/input-text", spacing = spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class InputTextTdComponent(BaseItemComponent):
    value: str
    name: str = ""
    width: str = ""
    height: str = ""
    manage: str = ""
    password: str = ""
    multiline: str = ""
    disabled: str = ""
    bgcolor: str = ""
    fgcolor: str = ""
    onchange: str = ""
    onleave: str = ""
    td_comp: Optional[dict] = None
    spacing: int = SPACING

    def __post_init__(self):
        spc = self.spacing
        del self.spacing
        spacing = spc
        super().__init__("gui/snippets/input-text-td", spacing = spacing)
        self.parameters = asdict(self, dict_factory=self.dict_factory)

    def __repr__(self): return super().__repr__()
    def __str__(self): return super().__str__()

@dataclass
class IncludeComment:
    name: str
    path: str
    other_pars: Optional[Iterable[str]] = None
    
    def __str__(self):
        final_str = self.path + ";".join(self.other_pars)
        return f"<!-- #include {self.name} {final_str} -->"


def text_bold(text: str, width: str="100%", align: str="center"):
    with td({"width": width, "align": align}) as btext:
        b(text)
    return btext

class ignore(html_tag):
    """
    Represents an <ignore> custom HTML tag.
    """
    tagname = 'ignore'