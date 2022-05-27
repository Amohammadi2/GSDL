TYPE_DEF_TEMPLATE = """
type %s %s {
%s
}
"""

INTERFACE_DEF_TEMPLATE = """
interface %s {
%s
}
"""

FIELD_TEMPLATE = """    %s: %s"""


class GSDLTranspiler:
    """ Turns the parse tree into GraphQL SDL format """

    def transpile(self, parse_tree):
        definitions = parse_tree[1]

        def handle_definitions(definition):
            match definition[0]:
                case "type_def": return self.transpile_type_def(definition)
                case "interface_def": return self.transpile_interface_def(definition)

        return "".join(map(handle_definitions, definitions))

    def transpile_type_def(self, type_def):
        _, name, field_set, interface = type_def

        return TYPE_DEF_TEMPLATE % (
            name,
            f"implements {interface}" if interface is not None else "",
            self.transpile_field_set(field_set),
        )

    def transpile_interface_def(self, interface_def):
        _, name, field_set = interface_def

        return INTERFACE_DEF_TEMPLATE % (
            name,
            self.transpile_field_set(field_set)
        )


    def transpile_field_set(self, field_set):
        _, fields = field_set
        return "\n".join(FIELD_TEMPLATE % (
            field[1],
            self.transpile_field_type(field[2])
        ) for field in fields)

    def transpile_field_type(self, field_type):
        type, inner = field_type

        match type:
            case "type": return inner
            case "required_type": return f"{self.transpile_field_type(inner)}!"
            case "array_type": return f"[{self.transpile_field_type(inner)}]"