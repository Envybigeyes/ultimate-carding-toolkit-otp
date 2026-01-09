def render_ui(scripts):
    options = "".join([f"<option>{k}</option>" for k in scripts])

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Cyber Call Ops</title>
<style>
body {{
  background: #0b0f1a;
  color: #00f6ff;
  font-family: monospace;
}}
.card {{
  border: 1px solid #00f6ff;
  padding: 20px;
  margin: 40px;
}}
button {{
  background: #00f6ff;
  border: none;
  padding: 10px;
}}
</style>
</head>
<body>
<div class="card">
<h2>Live Call Console</h2>
<form method="post" action="/call">
<input name="phone" placeholder="Phone Number"/><br><br>
<select name="script">{options}</select><br><br>
<button>Initiate Call</button>
</form>
</div>
</body>
</html>
"""
