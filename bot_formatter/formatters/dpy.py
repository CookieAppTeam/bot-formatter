"""Formatters for Discord.py."""

import libcst as cst
import libcst.matchers as m
from libcst.codemod import VisitorBasedCodemodCommand


class ConvertSetup(VisitorBasedCodemodCommand):
    DESCRIPTION = "Converts setup methods to their asynchronous equivalent."

    ADD_COG = m.Expr(m.Call(m.Attribute(attr=m.Name(value="add_cog"))))

    def __init__(self, context: cst.codemod.CodemodContext):
        super().__init__(context)

    def leave_FunctionDef(
        self, node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        if node.name.value == "setup":
            return updated_node.with_changes(asynchronous=cst.Asynchronous())
        return updated_node

    @m.call_if_inside(ADD_COG)
    def leave_Call(self, node: cst.Call, updated_node: cst.Call) -> cst.Call:
        if isinstance(node.func, cst.Attribute):
            return updated_node.with_changes(func=cst.Await(updated_node.func))
        return updated_node
