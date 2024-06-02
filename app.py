from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load AI tools data from Excel into DataFrame
df = pd.read_excel('database/tools.xlsx')  # Adjust the path as needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/filter_tools', methods=['POST'])
def filter_tools():
    tool_type = request.form['toolType']

    # Filter based on category or display all if 'All' is selected
    if tool_type.lower() == 'all':
        filtered_tools = df
    else:
        filtered_tools = df[df['CAT'].astype(str).str.lower() == tool_type.lower()]

    # Sort tools by rating in descending order and convert to JSON
    filtered_tools_json = filtered_tools.sort_values(by='RATING', ascending=False).to_json(orient='records')
    return jsonify(filtered_tools_json)

# Suggestion function remains the same...

@app.route('/get_subcategories', methods=['POST'])
def get_subcategories():
    tool_type = request.form['toolType']
    sub_categories = df[df['CAT'].astype(str).str.lower() == tool_type.lower()]['SUB_CAT'].unique().tolist()
    return jsonify(sub_categories)


if __name__ == '__main__':
    app.run(debug=True)
