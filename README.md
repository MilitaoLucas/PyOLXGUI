# PyOLXGUI
I found it pretty hard to keep track of blocks and close every tag using the current system on Olex2. So I decided to 
build this. 

## Basic functioning
PyOLXGUI works by creating some abstractions arround building the layout as to reduce boilerplate code and ensuring the
HTML is complete.

### item_components
Item components usually inherit from the class `LabeledGeneralComponent` and are used as general inputs. There is already
a lot of components and I accept requests from any you may want within reason.

#### Cycle Component
One notable component is the Cycle one. It works by ignoring one component over the other while mantaining the size of 
the biggest component. The Ignore component uses it with a component with nothing inside so if something is ignored it
doesn't changes the positioning.

### Rows
The first one is the Row clas. This row acts as an absstraction for the `row_table_on` blocks present on the olex2-gui blocks.
It also shows the rendered HTML content inside of it on Jupyter notebooks.

### H3Sections
H3Sections serve as a section on the GUI. The HTML it generates can be stored in a file. It also includes preview 
functionality that shows the rendered HTML content on Jupyter notebooks. 

### RowConfig
Row config is a Dataclass that is used to configure the way the general row will behave. It needs to be passed as an
argument to each row. 


## Features
- One of the biggest features of this project is automatically sizing. The size will be divided between every item_component.
But if a compoent has a `tdwidth` defined, its size will be respected by subtracting it from the calculation. That way,
developing the GUI is easier. 
- This framework is developed on the principle of contenarizing components with labels or related structures. As such, it is
easy to but a label on a component. It also autoindents the code making it much easier to read.
- The framework also replaces the default blocks on the Olex2-GUI as much as viable, so it can make it easier to debug and configure
the Classes present herein. 
- HTML preview is here! You can render HTML on Jupyter for now to have an idea of how the GUI will look on 
Olex2.