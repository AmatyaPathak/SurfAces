#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    return '''
     <!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>SurfAces🎾</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@0.9.4/css/bulma.min.css">
  <script src="https://unpkg.com/htmx.org@1.9.4"></script>
</head>
<body>
  <section class="section">
    <h1><b>SurfAces Tennis Stats🎾</b></h1>
    <div class="columns">
      <div class="column is-one-third">
        <input type="text" class="input" placeholder="Search Any Active Tennis Player🔎" name="q" hx-get="/search" hx-trigger="keyup changed delay:500ms" hx-target="#results">
      </div>
    </div>
    <table class="table is-fullwidth">
      <thead>
      </thead>
      <tbody id="results"></tbody>
    </table>
  </section>
</body>

</html>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text