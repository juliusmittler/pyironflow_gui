import ipywidgets as widgets
from python.treeview import TreeView
from python.reactflow import PyironFlowWidget
from python.create_macro import custom
from IPython.display import display
from pyiron_workflow import Workflow


class PyironFlow:
    def __init__(self, wf_list=None):
        # generate empty default workflow if workflow list is empty
        if wf_list is None:
            wf_list = []
        if len(wf_list) == 0:
            wf_list = [Workflow('workflow')]

        self.workflows = wf_list

        self.out_log = widgets.Output(layout={'border': '1px solid black', 'width': '800px'})
        self.out_widget = widgets.Output(layout={'border': '1px solid black', 'min_width': '500px'})
        self.wf_widgets = [PyironFlowWidget(wf, log=self.out_log, out_widget=self.out_widget)
                           for wf in self.workflows]
        self.view_flows = self.view_flows()
        self.tree_view = TreeView(flow_widget=self.wf_widgets[0], log=self.out_log)
        self.macro_name = widgets.Text(
            value='',
            placeholder='',
            description='Macro Name:',
            disabled=False   
        )
        self.macro_button = widgets.Button(
            description='Create Macro',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
        )
        
        self.macro =  widgets.Box([self.macro_name, self.macro_button])
        
        self.accordion = widgets.Accordion(children=[self.tree_view.gui, self.out_widget, self.out_log, self.macro],
                                           titles=['Node Library', 'Output', 'Logging Info', 'Custom Macro'],
                                           layout={'border': '1px solid black', 'min_width': '500px'})
        for widget in self.wf_widgets:
            widget.accordion_widget = self.accordion

        self.gui = widgets.HBox([
            self.accordion,
            self.view_flows,
            # self.out_widget
        ],
            layout={'border': '1px solid black'})

    
    def on_button_clicked(self, b):
            custom(self.workflows[0], self.macro_name)
                
    self.macro_button.on_click(on_button_clicked)
    
    def get_workflow(self, tab_index=0):
        wf_widget = self.wf_widgets[tab_index]
        return wf_widget.get_workflow()

    def view_flows(self):
        tab = widgets.Tab()
        tab.children = [self.display_workflow(index) for index, _ in enumerate(self.workflows)]
        tab.titles = [wf.label for wf in self.workflows]
        return tab

    def display_workflow(self, index: int, out_flow=None):
        w = self.wf_widgets[index]

        if out_flow is None:
            out_flow = widgets.Output(layout={'border': '1px solid black', 'width': '800px'})

        with out_flow:
            display(w.gui)

        return out_flow
