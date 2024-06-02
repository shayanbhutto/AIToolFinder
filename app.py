from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load AI tools data from Excel into DataFrame
df = pd.read_excel('database/tools.xlsx')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter_tools', methods=['POST'])
def filter_tools():
    tool_type = request.form['toolType']
    filtered_tools = df[df['CAT'] == tool_type]
    filtered_tools_json = filtered_tools.to_json(orient='records')
    return jsonify(filtered_tools_json)

if __name__ == '__main__':
    app.run(debug=True)
