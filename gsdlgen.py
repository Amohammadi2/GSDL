""" CLI interface to the GDSL preprocessor """
import os
from argparse import ArgumentParser
from pprint import pprint
# local imports
from parser import GSDLParser
from lexer import GSDLLexer
from data_loader import load_data
from preprocessor import GSDLPreprocessor


cli_argument_parser = ArgumentParser("CLI interface to GDSL preprocessor")
cli_argument_parser.add_argument('input', type=str, help="gsdlgen.py --input ./gql/schema.gdsl",)

args = cli_argument_parser.parse_args()

if __name__ == '__main__':

    if (gsdl_schema := load_data(args.input)) is not None:
        lexer = GSDLLexer()
        parser = GSDLParser()
        preprocessor = GSDLPreprocessor()
        parse_tree = parser.parse(lexer.tokenize(gsdl_schema))
        parsed = preprocessor.preprocess(parse_tree)
        pprint(parsed)

    else:
        print("Couldn't find the path specified, here are some useful information:")
        print("Input path: ", args.input)
        print("Current working directory: ", os.getcwd())