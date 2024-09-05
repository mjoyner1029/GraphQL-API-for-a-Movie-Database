from flask import Flask
from flask_graphql import GraphQLView
import graphene
from schema import Query, Mutation

app = Flask(__name__)
app.debug = True

schema = graphene.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True  # Set to True to enable the GraphiQL interface
    )
)

if __name__ == '__main__':
    app.run()
