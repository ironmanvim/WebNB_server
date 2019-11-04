from flask import Flask
from flask_cors import CORS
from flask_graphql import GraphQLView
from schema import schema

app = Flask(__name__)
CORS(app)
app.debug = True

response_html = '''\
<html>
    <body>
        Welcome to VebPy Server. For Querying use <a href="/graphql">/graphql</a>
    </body>
</html>
'''


@app.route('/')
def index():
    return response_html


app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=schema,
        graphiql=True
    )
)

if __name__ == '__main__':
    app.run()
