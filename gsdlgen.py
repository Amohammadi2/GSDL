""" CLI interface to the GDSL preprocessor """
import os
from argparse import ArgumentParser
from pprint import pprint
# local imports
from parser import GSDLParser
from lexer import GSDLLexer
from data_loader import load_data, write_output
from preprocessor import GSDLPreprocessor
from transpiler import GSDLTranspiler


cli_argument_parser = ArgumentParser("CLI interface to GDSL preprocessor")
cli_argument_parser.add_argument('input', type=str, help="gsdlgen.py ./gql/schema.gdsl",)
cli_argument_parser.add_argument('-o', dest="output", type=str, help="gsdlgen.py ./input.gsdl ./gql/schema.graphql", default="./schema.graphql")

args = cli_argument_parser.parse_args()

if __name__ == '__main__':

    if (gsdl_schema := load_data(args.input)) is not None:
        lexer = GSDLLexer()
        parser = GSDLParser()
        preprocessor = GSDLPreprocessor()
        transpiler = GSDLTranspiler()
        parse_tree = parser.parse(lexer.tokenize(gsdl_schema))
        processed_parse_tree = preprocessor.preprocess(parse_tree)
        schema_output = transpiler.transpile(processed_parse_tree)
        write_output(schema_output, args.output)
        

    else:
        print("Couldn't find the path specified, here are some useful information:")
        print("Input path: ", args.input)
        print("Current working directory: ", os.getcwd())