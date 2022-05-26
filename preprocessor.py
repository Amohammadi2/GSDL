class GSDLPreprocessor:

    def __init__(self) -> None:
        self.generic_types: dict = {}
        self.generic_refs = set()
        self.handled_refs = set()

    @property
    def remaining_generic_refs(self):
        return self.generic_refs.difference(self.handled_refs)

    def preprocess(self, parse_tree: tuple) -> tuple:
        node_type, definitions = parse_tree
        parsed_definitions = (node_type, self.definitions_visitor(definitions))
        generated_definitions = self.generate_types()
        return (node_type, (*parsed_definitions, *generated_definitions))

    def generate_types(self):
        generated_definitions = set()
        while refs := self.remaining_generic_refs:
            for gen_ref in refs:
                self.handled_refs.add(gen_ref)
                def_name, gen_type, type_values = gen_ref
                type_def = ('type_def', def_name, self.resolve_field_set(type_values[1], *self.generic_types[gen_type]), None)
                generated_definitions.add(self.definition_visitor(type_def))
        return generated_definitions

    def resolve_field_set(self, gen_type_vals, gen_type_args, gen_field_set):
        return ('field_set', tuple(
            (node_type, field_name, self.substitute_name_space(field_type, gen_type_vals, gen_type_args)) for (node_type, field_name, field_type) in gen_field_set
        ))

    def substitute_name_space(self, field_type, gen_type_vals, gen_type_args: tuple):
        if field_type[0] == "generic_type":
            return (field_type[0], field_type[1], ('type_args', tuple(self.substitute_name_space(ft, gen_type_vals, gen_type_args) for ft in field_type[2][1])))
        if field_type[0] == "type":
            if field_type[1] in gen_type_args:
                coresponding_type_val = gen_type_vals[gen_type_args.index(field_type[1])]
                return coresponding_type_val
            return field_type
        return (field_type[0], self.substitute_name_space(field_type[1], gen_type_vals, gen_type_args))

    def definitions_visitor(self, definitions):
        def not_generic_only(definition):
            def_type, *_ = definition
            if def_type == 'generic_type_def':
                self.generic_types[definition[1]] = (definition[2][1], definition[3][1])
                return False
            return True

        # continue processing, but keep generic type defs aside
        # we'll process them later on
        return tuple(
            self.definition_visitor(definition) 
            for definition in filter(not_generic_only, definitions)
        )

    def definition_visitor(self, definition):
        def_type = definition[0]

        if def_type == 'type_def':
            name, field_set, interface = definition[1::]
            return (def_type, name, self.field_set_visitor(field_set), interface)

        elif def_type == 'interface_def':
            name, field_set = definition[1::]
            return (def_type, name, self.field_set_visitor(field_set))

    def field_set_visitor(self, field_set):
        node_type, fields = field_set
        return (node_type, self.fields_visitor(fields))

    def fields_visitor(self, fields):
        return tuple(
            self.field_visitor(field) for field in fields
        )

    def field_visitor(self, field):
        node_type, field_name, field_type = field
        return (
            node_type, field_name, self.field_type_visitor(field_type) 
        )

    def field_type_visitor(self, field_type):
        type = field_type[0]

        if type == "generic_type":
            final_name = self.handle_generic_type_name(field_type)
            type_name, type_args = field_type[1::]
            self.generic_refs.add((final_name, type_name, type_args))
            return ('type', final_name)
        elif type == "type":
            return field_type
        return (type, self.field_type_visitor(field_type[1]))


    def handle_generic_type_name(self, field_type):
        type = field_type[0]

        match type:
            case "type": return field_type[1]
            case "required_type": return f"{self.handle_generic_type_name(field_type[1])}!"
            case "array_type": return f"{self.handle_generic_type_name(field_type[1])}Arr"
            case "generic_type":
                type_name, type_args = field_type[1::]
                name_list = []
                for type_arg in type_args[1]:
                    name_list.append(self.handle_generic_type_name(type_arg))
                return f"{'_'.join(name_list)}__{type_name}"