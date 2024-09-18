import os
from dash_extensions.enrich import DashProxy, html, dcc, Input, Output, State
from dash_extensions import SSE
from dash.exceptions import PreventUpdate
from dash_extensions.streaming import sse_options

from models import Query

app = DashProxy()
app.layout = html.Div(
    [
        dcc.Input(id="query", value="What is Plotly Dash?", type="text"),
        html.Button("Submit", id="submit"),
        dcc.Markdown(id="response", dangerously_allow_html=True, dedent=False),
        # Configure the SSE component to concatenate the stream values, and animate the result.
        SSE(id="sse", concat=True, animate_chunk=5, animate_delay=10),
    ]
)
# Expose server variable for gunicon to run the server.
server = app.server
# Configure the stream URL dependent on the environment.
stream_url = os.getenv("STREAM_URL", "http://127.0.0.1:8000/stream")


@app.callback([Output("sse", "url"), Output("sse", "options")], Input("submit", "n_clicks"), State("query", "value"))
def submit_query(n_clicks, query) -> tuple[str, dict[str, list[dict[str, str]]]]:
    if n_clicks is None:
        raise PreventUpdate
    # Create message structure to be consumed by the Azure OpenAI API.
    messages = [{"role": "user", "content": query}]
    # Pass the messages to the stream endpoint to trigger streaming.
    return stream_url, sse_options(payload=Query(messages=messages))


# Render (concatenated, animated) text from the SSE component into response div.
app.clientside_callback("function(x){return x};", Output("response", "children"), Input("sse", "animation"))


if __name__ == "__main__":
    app.run_server()
