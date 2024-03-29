# GSDL (Generic Schema Definition Language)

GSDL is a GraphQL SDL preprocessor that adds generic type declaration capabilities to the original GraphQL SDL language. The goal of this project is to reduce code repetition using generic types and type templates (like C++). The idea behind this project comes from this issue that was posted on graphql-spec repo [#190](https://github.com/graphql/graphql-spec/issues/190)

```graphql
type Query {
  me: User
}

type User {
  feed(first: Int!, after: String): Connection<Post>!
}

generic type Connection <EdgeType> {
  pageInfo: PageInfo
  edges: [Edge<EdgeType>!]!
}

generic type Edge <NodeType> {
  cursor: String!
  node: NodeType!
}

type PageInfo {
  startCursor: String!
  endCursor: String!
  hasNextPage: Boolean!
  hasPrevPage: Boolean!
}
```

This can reduce a lot code repetition in case of implementing a Relay-compilant GraphQL APIs. You can use this library in combination with a schema-first GraphQL server library to implement your APIs more quickly and efficiently.

Currently, the project is not production ready and It might have a lot of edge-cases and bugs that are still unknown. I don't recomand using this project in a real project yet but if you like, you can contribute to this project in order to make it better (or probably production ready)

## Project status

You can see the current status of the project [HERE](https://github.com/Amohammadi2/GSDL/projects/1)

## Project structure

This project is based on python [SLY package](https://sly.readthedocs.io/en/latest/sly.html) and the file structure of this project is as follows:

- `lexer.py`: Contains the lexer and the tokens
- `parser.py`: Contains the parser and the grammer rules
- `preprocessor.py`: Contains the preprocessor and the node visitors that make changes to the `GSDL` parse tree to turn it into a `GraphQL` parse tree.
- `transpiler.py`: Contains the GraphQL transipler that will output the modified parse tree to a file or ...
