from pyiron_workflow import as_function_node, as_macro_node
from typing import Optional

@as_macro_node()
def macro_new(wf, part1_a: Optional[float|int] = None):
    from pyiron_nodes.custom_node import part_1
    from pyiron_nodes.custom_node import part_2
    from pyiron_nodes.custom_node import part_3
    wf.part1 = part_1(a = part1_a)
    wf.part2 = part_2(a = wf.part1)
    wf.part3 = part_3(a = wf.part2)
    return wf.part3