html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Feed FastAPI</title>
    </head>
    <body onload="">
        <h1>Feed FastAPI</h1>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("wss://https://1h86jt.deta.dev/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
        </script>
    </body>
</html>
"""


