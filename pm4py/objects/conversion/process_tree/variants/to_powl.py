from pm4py.objects.process_tree.obj import ProcessTree, Operator as PTOperator
from pm4py.objects.powl.obj import POWL, StrictPartialOrder, OperatorPOWL, Transition, SilentTransition
from typing import Optional, Dict, Any


def apply_recursive(tree: ProcessTree, rec_depth=0) -> POWL:
    """
    Internal method
    """
    nodes = []

    for c in tree.children:
        nodes.append(apply_recursive(c, rec_depth+1))

    if tree.operator is None:
        if tree.label is not None:
            powl = Transition(label=tree.label)
        else:
            powl = SilentTransition()
    elif tree.operator == PTOperator.OR:
        raise Exception("conversion of process trees containing OR nodes is not supported!")
    elif tree.operator == PTOperator.XOR:
        powl = OperatorPOWL(PTOperator.XOR, nodes)
    elif tree.operator == PTOperator.LOOP:
        powl = OperatorPOWL(PTOperator.LOOP, nodes)
    else:
        powl = StrictPartialOrder(nodes=nodes)

    if tree.operator == PTOperator.SEQUENCE:
        for i in range(len(nodes)-1):
            powl.order.add_edge(nodes[i], nodes[i+1])

    return powl


def apply(tree: ProcessTree, parameters: Optional[Dict[Any, Any]] = None) -> POWL:
    """
    Converts a process tree model to a POWL model

    Parameters
    ---------------
    tree
        Process tree

    Returns
    ---------------
    powl_model
        POWL model
    """
    if parameters is None:
        parameters = {}

    return apply_recursive(tree)
