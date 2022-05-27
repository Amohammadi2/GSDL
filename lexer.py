from sly import Lexer


class GSDLLexer(Lexer):
    tokens = {ID, TYPE_DEF, GENERIC_MODIFIER, INTERFACE_IMPL, INTERFACE_DEF, ENUM_DEF}
    literals = {
        "!", "{", "}", "[", "]", "<", ">", ":"
    }

    ID = r'[a-zA-Z_]\w*'
    ID['type'] = TYPE_DEF
    ID['generic'] = GENERIC_MODIFIER
    ID['implements'] = INTERFACE_IMPL
    ID['interface'] = INTERFACE_DEF
    ID['enum'] = ENUM_DEF

    ignore = ' \t\n,'
    ignore_comment=r'\#.*'