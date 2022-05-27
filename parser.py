from sly import Parser
from lexer import GSDLLexer

class GSDLParser(Parser):
    tokens =  GSDLLexer.tokens
    literals = GSDLLexer.literals

    debugfile = 'parser.out'

    @_("definition", "schema_def definition")
    def schema_def(self, p):
        if hasattr(p, 'schema_def'):
            return ('schema_def', (*p.schema_def[1], p.definition))
        return ('schema_def', (p.definition,))

    @_('type_def', 'generic_type_def', 'interface_def', 'enum_def')
    def definition(self, p):
        if hasattr(p, 'type_def'):
            return p.type_def
        elif hasattr(p, 'generic_type_def'):
            return p.generic_type_def
        elif hasattr(p, 'interface_def'):
            return p.interface_def
        elif hasattr(p, 'enum_def'):
            return p.enum_def

    @_('GENERIC_MODIFIER TYPE_DEF ID "<" generic_args ">" "{" field_set "}"')
    def generic_type_def(self, p):
        return ('generic_type_def', p.ID, p.generic_args, p.field_set)

    @_('ID', 'generic_args ID')
    def generic_args(self, p):
        if hasattr(p, 'generic_args'):
            return ('generic_args', (*p.generic_args, p.ID))
        return ('generic_args', (p.ID,))

    @_('ENUM_DEF ID "{" id_set "}"')
    def enum_def(self, p):
        return ('enum_def', p.ID, p.id_set)

    @_('ID', 'id_set ID')
    def id_set(self, p):
        if hasattr(p, 'id_set'):
            return ('id_set', (*p.id_set[1], p.ID))
        return ('id_set', (p.ID,))

    @_('INTERFACE_DEF ID "{" field_set "}"')
    def interface_def(self, p):
        return ('interface_def', p.ID, p.field_set)

    @_('TYPE_DEF ID "{" field_set "}"', 'TYPE_DEF ID INTERFACE_IMPL ID "{" field_set "}"')
    def type_def(self, p):
        if hasattr(p, 'INTERFACE_IMPL'):
            return ('type_def', p.ID0, p.field_set, p.ID1)
        return ('type_def', p.ID, p.field_set, None)

    @_('field', 'field_set field')
    def field_set(self, p):
        if hasattr(p, 'field_set'):
            return ('field_set', (*p.field_set[1], p.field))
        return ('field_set', (p.field,))

    @_('ID ":" type')
    def field(self, p):
        return ('field', p.ID, p.type)

    @_('ID', 'generic_type' , 'required_type', 'array_type')
    def type(self, p):
        if hasattr(p, 'ID'):
            return ('type', p.ID)
        elif hasattr(p, 'generic_type'):
            return p.generic_type
        elif hasattr(p, 'required_type'):
            return p.required_type
        elif hasattr(p, 'array_type'):
            return p.array_type
    
    @_('type "!"')
    def required_type(self, p):
        if (p.type[0] == 'required_type'):
            raise SyntaxError("You can't make a double required type (!!)")
        return ('required_type', p.type)

    @_('"[" type "]"')
    def array_type(self, p):
        return ('array_type', p.type)

    @_('ID "<" type_args ">"')
    def generic_type(self, p):
        return ('generic_type', p.ID, p.type_args)

    @_('ID', 'type_args ID')
    def type_args(self, p):
        if hasattr(p, 'type_args'):
            return ('type_args', (*p.type_args[1], ('type', p.ID)))
        return ('type_args', (('type', p.ID),))