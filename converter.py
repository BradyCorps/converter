from flask import Flask, request, render_template_string, redirect, url_for
import shelve
import os

app = Flask(__name__)

def convert_column_to_semicolon_list(data):
    data = data.strip().split('\n')
    data = [item.strip() for item in data]
    semicolon_separated_list = ";".join(data)
    return semicolon_separated_list

def save_conversion(conversion):
    with shelve.open('conversions.db') as db:
        if 'conversions' not in db:
            db['conversions'] = []
        conversions = db['conversions']
        conversions.insert(0, conversion)
        if len(conversions) > 5:
            conversions = conversions[:5]
        db['conversions'] = conversions

def load_last_conversions():
    with shelve.open('conversions.db') as db:
        return db.get('conversions', [])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_data = request.form['input_data']
        result = convert_column_to_semicolon_list(input_data)
        save_conversion(result)
        return redirect(url_for('index'))

    last_conversions = load_last_conversions()
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
            <title>Column to Semicolon List Converter</title>
        </head>
        <body>
            <div class="container mt-5">
                <h1 class="mb-4">Column to Semicolon List Converter</h1>
                <form method="post">
                    <div class="form-group">
                        <label for="inputData">Input Column Data:</label>
                        <textarea class="form-control" id="inputData" name="input_data" rows="10"></textarea>
                    </div>
                    <button type="submit" class="btn btn-primary">Convert</button>
                </form>
                <h2 class="mt-4">Semicolon-Separated List:</h2>
                <div class="alert alert-info" role="alert">
                    {{ last_conversions[0] if last_conversions else "No conversions yet." }}
                </div>
                <h2 class="mt-4">Last 5 Conversions:</h2>
                <ul class="list-group">
                    {% for conversion in last_conversions %}
                        <li class="list-group-item">{{ conversion }}</li>
                    {% endfor %}
                </ul>
            </div>
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.2/dist/umd/popper.min.js"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
        </body>
        </html>
    ''', last_conversions=load_last_conversions())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
