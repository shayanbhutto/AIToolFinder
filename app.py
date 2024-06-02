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
    sub_category = request.form['subCategory']

    filtered_tools = df.copy()

    # Filter by tool type (CAT) if not "All"
    if tool_type.lower() != 'all':
        filtered_tools = filtered_tools[filtered_tools['CAT'].astype(str).str.lower() == tool_type.lower()]

    # Filter by sub-category (SUB_CAT) if provided and not "All"
    if sub_category and sub_category.lower() != 'all':
        filtered_tools = filtered_tools[filtered_tools['SUB_CAT'].astype(str).str.lower() == sub_category.lower()]

    # Sort tools by rating in descending order and convert to JSON
    filtered_tools_json = filtered_tools.sort_values(by='RATING', ascending=False).to_json(orient='records')
    return jsonify(filtered_tools_json)

# Get categories (unchanged from your previous code)
@app.route('/get_categories', methods=['GET'])
def get_categories():
    categories = df['CAT'].unique().tolist()
    categories.insert(0, "All") 
    return jsonify(categories)

# Get sub-categories (unchanged from your previous code)
@app.route('/get_subcategories', methods=['POST'])
def get_subcategories():
    tool_type = request.form['toolType']

    # Filter by tool type (CAT)
    filtered_df = df[df['CAT'].astype(str).str.lower() == tool_type.lower()]

    # Get unique sub-categories 
    sub_categories = filtered_df['SUB_CAT'].unique().tolist()  

    # Add "All" only if there are sub-categories for this type
    if sub_categories:
        sub_categories.insert(0, "All")

    return jsonify(sub_categories)



if __name__ == '__main__':
    app.run(debug=True)
