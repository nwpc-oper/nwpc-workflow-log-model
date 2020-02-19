from nwpc_workflow_log_model.analytics.node_situation import NodeSituation
from nwpc_workflow_log_model.analytics.node_situation_dfa import (
    NodeSituationDFA, NodeStatus, SituationType
)


def test_node_situation_dfa():
    dfa = NodeSituationDFA(name="test")
    dfa.trigger(NodeStatus.queued.value)
    assert dfa.node_situation.state == SituationType.CurrentQueue

    dfa.trigger(NodeStatus.submitted.value)
    assert dfa.node_situation.state == SituationType.Submit

    dfa.trigger(NodeStatus.active.value)
    assert dfa.node_situation.state == SituationType.Active

    dfa.trigger(NodeStatus.complete.value)
    assert dfa.node_situation.state == SituationType.Complete
