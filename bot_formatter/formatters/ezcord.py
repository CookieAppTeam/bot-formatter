"""Formatters for Ezcord."""

import libcst as cst
import libcst.matchers as m
from libcst.codemod import VisitorBasedCodemodCommand


class ConvertContext(VisitorBasedCodemodCommand):
    DESCRIPTION = "Converts discord.ApplicationContext to ezcord.EzContext."

    SLASH_DECORATOR = m.FunctionDef(
        decorators=[m.Decorator(decorator=m.Call(func=m.Name("slash_command")))]
    )

    IMPORT_EZCORD = m.Import(names=[m.ImportAlias(name=m.Name(value="ezcord"))])

    EZ_ANNOTATION_1 = m.Annotation(m.Attribute(value=m.Name("ezcord"), attr=m.Name("EzContext")))
    EZ_ANNOTATION_2 = m.Annotation(m.Name(value="EzContext"))

    def __init__(self, context: cst.codemod.CodemodContext):
        super().__init__(context)
        self.has_changes = False
        self.has_ezcord_import = False

    def leave_Import(self, original_node: cst.Import, updated_node: cst.Import) -> cst.Import:
        """Checks if Ezcord is already imported."""

        if m.matches(updated_node, self.IMPORT_EZCORD):
            self.has_ezcord_import = True

        return updated_node

    @m.call_if_inside(SLASH_DECORATOR)
    def leave_FunctionDef(
        self, node: cst.FunctionDef, updated_node: cst.FunctionDef
    ) -> cst.FunctionDef:
        """Replaces discord.ApplicationContext with ezcord.EzContext if it doesn't already exist."""

        new_params = []
        for param in node.params.params:
            if param.annotation:
                if m.matches(param.annotation, self.EZ_ANNOTATION_1) or m.matches(
                    param.annotation, self.EZ_ANNOTATION_2
                ):
                    new_params.append(param)
                    continue

            if param.name.value != "ctx":
                new_params.append(param)
                continue

            modified_param = cst.Param(
                cst.Name("ctx"),
                cst.Annotation(cst.Attribute(value=cst.Name("ezcord"), attr=cst.Name("EzContext"))),
            )
            new_params.append(modified_param)
            self.has_changes = True

        return updated_node.with_changes(params=cst.Parameters(params=new_params))

    def leave_Module(self, node: cst.Module, updated_node: cst.Module) -> cst.Module:
        """Adds an import for ezcord if it doesn't exist and if changes were made."""

        if self.has_changes and not self.has_ezcord_import:
            new_import = cst.Import(names=[cst.ImportAlias(name=cst.Name("ezcord"))])
            new_body = [
                cst.SimpleStatementLine(body=[new_import]),
                cst.Newline(),
            ] + list(updated_node.body)
            return updated_node.with_changes(body=new_body)

        return updated_node
