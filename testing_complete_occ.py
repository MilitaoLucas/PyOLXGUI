import os
from importlib import reload
import ast

import olx_gui.components.item_component
import olx_gui.components.table
import temp.blocks
reload(temp.blocks)
reload(olx_gui.components.item_component)
reload(olx_gui.components.table)
from olx_gui.components.item_component import *
from olx_gui.components.table import *
from dotenv import load_dotenv, set_key
import re
lexer = HtmlLexer()
formatter = TerminalFormatter() # This will output ANSI escape codes
from bs4 import BeautifulSoup

def convert_include(inc_comment: str) -> str:
    inc_comment = inc_comment.replace("\\", "/").replace("<!--", "").replace("-->", "")
    inc_comment = inc_comment.replace("#include", "").strip().split()
    name = inc_comment[0]
    inc_rest = [i for i in "".join(inc_comment[1:]).split(";") if i]
    pth = inc_rest[0]
    return f"name=\"{name}\", path=\"{pth}\", other_pars={inc_rest[1:]}"

def combo_convert(combo: str):
    conv = re.findall(r"\$\+((?:.|\n)*?)\$-", combo)[0].strip()
    conv = conv.replace("html.Snippet", "").strip()
    conv = list(ast.literal_eval(conv))
    for i in range(1, len(conv)):
        k, v = conv[i].replace(" ", "").split("=")
        conv[i] = f"{k}=\"{v}\""
    conv[0] = f"\"{conv[0]}\""
    retstr = ", ".join(conv)
    return retstr

structure = []
IC = include_comment
structure.append(IC("tool-h3", "gui/blocks/tool-h3.htm", ["imgage=#image", "colspan=1", "1"]))
cfg = TableConfig(tr1_parameters={"ALIGN":"left", "NAME":'SNUM_REFINEMENT_NSFF',"width":"100%"})

table1 = Table(
    rows=[
        [
            include_comment(name="tool-help-first-column",
                            path="gui/blocks/tool-help-first-column.htm",
                            other_pars=['help_ext=NoSpherA2_Quick_Buttons', '1']),
            b("$spy.NoSpherA2.make_quick_button_gui()"),
        ],
        [
            include_comment(name="tool-help-first-column", path="gui/blocks/tool-help-first-column.htm", other_pars=['help_ext=NoSpherA2_Options_1', '1']),
            text_bold("Basis Set", width="15%", align="left"),
            GeneralComponent("gui/snippets/input-combo",
                             name="NoSpherA2_basis@refine",
                             items="spy.NoSpherA2.getBasisListStr()",
                             value="spy.GetParam('snum.NoSpherA2.basis_name')",
                             onchange="spy.NoSpherA2.change_basisset"
                                      "(html.GetValue('~name~'))",
                             td_comp={"width": "15%"}
                             ).dominate,
            text_bold("Method ", width="12%", align="right"),
            GeneralComponent(
                "gui/snippets/input-combo",
                name="NoSpherA2_method@refine",
                items="spy.NoSpherA2.get_functional_list()",
                value="spy.GetParam('snum.NoSpherA2.method')",
                onchange="spy.SetParam('snum.NoSpherA2.method',html.GetValue('~name~'))",
                td_comp={"width": "14%"}
            ).dominate,
            ComboBoxComponent(
                name="NoSpherA2_method@refine",
                items="spy.NoSpherA2.get_functional_list()",
                phil="snum.NoSpherA2.method",
                td_comp={"width": "14%"}
            ).dominate,
            text_bold("CPUs", width="5%", align="right"),
            GeneralComponent(
                "gui/snippets/input-combo",
                name="NoSpherA2_cpus@refine",
                items="spy.NoSpherA2.getCPUListStr()",
                value="spy.GetParam('snum.NoSpherA2.ncpus')",
                onchange="spy.SetParam('snum.NoSpherA2.ncpus',html.GetValue('~name~'))",
                td_comp={"width": "10%", "align": "center"}
            ).dominate,
            text_bold("Mem(Gb)", width="5%", align="right"),
            GeneralComponent(
                "gui/snippets/input-text",
                name="NoSpherA2_mem",
                value="spy.GetParam('snum.NoSpherA2.mem')",
                onchange="spy.SetParam('snum.NoSpherA2.mem',html.GetValue('~name~'))",
                td_comp={"width": "30%", "align": "center"}
            ).dominate
        ],
    ],
    config=cfg,
    comment_obj=include_comment(
        name="tool-help-first-column", path="gui/blocks/tool-help-first-column.htm", other_pars=['help_ext=NoSpherA2_Quick_Buttons', '1']
    )
)

with td(width="8%", align="left") as charge_input:
    input_(type="spin",
           name="SET_CHARGE",
           width="50",
           height="17",
           max="1000",
           min="-1000",
           bgcolor="spy.GetParam(gui.html.input_bg_colour)",
           value="$spy.GetParam(snum.NoSpherA2.charge)",
           onchange="spy.SetParam(snum.NoSpherA2.charge,html.GetValue(~name~))"
           )

with td(width="8%", align="right") as charge_multiplicity:
    input_(type="spin",
           width="50",
           height="17",
           name="SET_SNUM_MULTIPLICITY",
           bgcolor="spy.GetParam(gui.html.input_bg_colour)",
           min="1",
           value="$spy.GetParam(snum.NoSpherA2.multiplicity)",
           onchange="spy.SetParam(snum.NoSpherA2.multiplicity,html.GetValue(~name~))"
           )

with td(width="8%", align="left") as cycles_spin:
    input_(
        type="spin",
        width="50",
        height="17",
        bgcolor="spy.GetParam(gui.html.input_bg_colour)",
        name='SET_SNUM_MAX_HAR',
        value='$spy.GetParam(snum.NoSpherA2.Max_HAR_Cycles)',
        onchange='spy.SetParam(snum.NoSpherA2.Max_HAR_Cycles,html.GetValue(~name~))'
    )

table2 = Table(
    rows=[
        [
            text_bold("Charge", width="13%", align="left"),
            charge_input,
            text_bold("Multiplicity", width="16%", align="right"),
            charge_multiplicity,
            GeneralComponent(
                "gui/snippets/input-checkbox-td",
                name="Iterative",
                label="Iterative",
                checked="spy.GetParam('snum.NoSpherA2.full_HAR')",
                oncheck="spy.NoSpherA2.toggle_full_HAR()",
                bgcolor="GetVar(HtmlTableFirstcolColour)",
                onuncheck="spy.NoSpherA2.toggle_full_HAR()",
                td_comp={"width": "2%", "align": "left"}
            ).dominate,
            # The following are toggled on Iterative or full har switch
            ignore(text_bold("Max Cycles", width="18%"),
                   cycles_spin,
                   test="strcmp(spy.GetParam('snum.NoSpherA2.full_HAR'),'True')"),
            ignore(
                GeneralComponent(
                    "gui/snippets/gui-link-button",
                    value="Update .tsc & .wfn",
                    onclick="spy.NoSpherA2.launch() >> html.Update()",
                    bgcolor="GetVar(HtmlTableFirstcolColour)",
                    td1=r"''", td_comp={"width": "29%", "align": "center"}
                ).dominate,
                test="strcmp(spy.GetParam('snum.NoSpherA2.full_HAR'),'False')"
            )
        ],
    ],
    config=cfg,
)

table3 = Table(
    rows=[
        [
            text_bold("Integr. Accuracy", width="13%", align="left"),
            ignore(
                GeneralComponent(
                    "gui/snippets/input-combo",
                    name="NoSpherA2_becke_accuracy@refine",
                    items="'Low;Normal;High;Max'",
                    value="spy.GetParam('snum.NoSpherA2.becke_accuracy')",
                    onchange="spy.SetParam('snum.NoSpherA2.becke_accuracy',html.GetValue('~name~'))",
                    td_comp={"width": "16%", "align": "left"}
                ).dominate,
                test="strcmp(spy.GetParam('snum.NoSpherA2.NoSpherA2_SF'),'True')"
            ),
            GeneralComponent(
                "gui/snippets/input-checkbox-td",
                name="H_Aniso",
                label="H Aniso",
                checked="spy.GetParam('snum.NoSpherA2.h_aniso')",
                oncheck="spy.SetParam('snum.NoSpherA2.h_aniso','True')",
                bgcolor="GetVar(HtmlTableFirstcolColour)",
                onuncheck="spy.SetParam('snum.NoSpherA2.h_aniso','False')",
                td_comp={"width": "1%", "align": "left"}
            ),
            GeneralComponent(
                "gui/snippets/input-checkbox-td",
                name="H_Afix",
                label="No Afix",
                checked="spy.GetParam('snum.NoSpherA2.h_afix')",
                oncheck="spy.SetParam('snum.NoSpherA2.h_afix','True')",
                bgcolor="GetVar(HtmlTableFirstcolColour)",
                onuncheck="spy.SetParam('snum.NoSpherA2.h_afix','False')",
                td_comp={"width": "1%", "align": "left"}
            )
        ],
    ],
    config=cfg,
    comment_obj = include_comment(
        name="tool-help-first-column", path="gui/blocks/tool-help-first-column.htm", other_pars=['help_ext=NoSpherA2_Options_3', '1']
    )
)

cfg.tr1_parameters["NAME"] = "SNUM_REFINEMENT_RIFIT"
table4 = Table(
    rows=[
        [
            GeneralComponent(
                "gui/snippets/input-checkbox-td",
                name="Ri_Fit",
                label="RI-Fit",
                checked="spy.GetParam('snum.NoSpherA2.NoSpherA2_RI_FIT')",
                oncheck="spy.SetParam('snum.NoSpherA2.NoSpherA2_RI_FIT','True')>>html.Update()",
                bgcolor="GetVar(HtmlTableFirstcolColour)",
                onuncheck="spy.SetParam('snum.NoSpherA2.NoSpherA2_RI_FIT','False')>>html.Update()",
                disable_td=True
            ).dominate,
            ignore(
                text_bold("Auxiliary Basis", width="30%"),
                GeneralComponent(
                    "gui/snippets/input-combo",
                    name="NoSpherA2_ORCA_RIFIT@refine",
                    items="'combo_basis_fit;def2_universal_jkfit;def2_svp_jkfit;hgbsp3_7;def2_qzvppd_rifit;tzvp_jkfit;cc-pvqz-jkfit'",
                    value="spy.GetParam('snum.NoSpherA2.auxiliary_basis')",
                    onchange="spy.SetParam('snum.NoSpherA2.auxiliary_basis',html.GetValue('~name~'))",
                    td_comp={"width": "40%"}
                ).dominate,
                td(b(), width="40%", align="left"),
                test="not strcmp(spy.GetParam('snum.NoSpherA2.NoSpherA2_RI_FIT'), False)"
            )
        ],
    ],
    config=cfg,
    comment_obj = include_comment(
        name="tool-help-first-column", path="gui/blocks/tool-help-first-column.htm", other_pars=['help_ext=NoSpherA2_Options_RIFit', '1']
    ),
    ignore_condition="not(strcmp(spy.GetParam('user.NoSpherA2.show_ri_fit'),'False'))"
)

free_html1 = include_comment(
    name="ELMO_specific", path="../util/pyUtil/NoSpherA2/ELMO_specific.htm", other_pars=['help_ext=NoSpherA2Extras', '1']
)

cfg.tr1_parameters["NAME"] = "SNUM_REFINEMENT_NSFF"
table5 = Table(
    rows=[
        [
            text_bold("Grouped Parts", width="25%", align="left"),
            GeneralComponent(
                "gui/snippets/input-text",
                name="NoSpherA2_Disorder_Groups@refine",
                value="spy.GetParam('snum.NoSpherA2.Disorder_Groups')",
                onchange="spy.SetParam('snum.NoSpherA2.Disorder_Groups',html.GetValue('~name~'))",
                td_comp={"width": "70%"}
            ).dominate
        ],
    ],
    config=cfg,
    ignore_condition="spy.NoSpherA2.is_disordered()"
)

table6 = Table(
    rows=[
        [
            td("No Settings available.", width="25%", align="center")
        ],
    ],
    config=cfg,
    ignore_condition="not(spy.GetParam('snum.NoSpherA2.Calculate'))"
)

calculate_list = [table1, table2, table3, table4, free_html1, table5]
first_comment = include_comment(name="tool-h3", path="gui/blocks/tool-h3.htm",
                                  other_pars=['image=#image', 'colspan=1', '1'])
html_final = ignore(*(raw(str(i)) for i in calculate_list), test="spy.GetParam('snum.NoSpherA2.Calculate')")
html_final = str(first_comment) + "\n\n" + str(html_final) + "\n" + str(table6)
pretty_html = BeautifulSoup(str(html_final), 'html.parser').prettify()
highlighted_html = highlight(str(pretty_html), lexer, formatter)
load_dotenv()

with open(os.getenv("DEPLOY_PATH"), "w") as f:
    f.write(str(pretty_html))
print(highlighted_html)