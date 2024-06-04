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
    sub_category = request.form.get('subCategory', '')  # Get subCategory, default to empty string
    sub_sub_category = request.form.get('subSubCategory', '')  # Get subSubCategory, default to empty string

    # Initial filter by CAT
    filtered_tools = df if tool_type.lower() == 'all' else df[df['CAT'].astype(str).str.lower() == tool_type.lower()]

    # Filter by SUB_CAT if provided and not empty
    if sub_category and sub_category.lower() != 'all':
        filtered_tools = filtered_tools[filtered_tools['SUB_CAT'].astype(str).str.lower() == sub_category.lower()]

    # Filter by SUB_SUB_CAT if provided and not empty
    if sub_sub_category and sub_sub_category.lower() != 'all':
        filtered_tools = filtered_tools[filtered_tools['SUB_SUB_CAT'].astype(str).str.lower() == sub_sub_category.lower()]
    
    # Filter by POPULAR if popularOnly is true
    popular_only = request.form.get('popularOnly') == 'true'
    if popular_only:
        filtered_tools = filtered_tools[filtered_tools['POPULAR'] == 1]
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




@app.route('/get_subsubcategories', methods=['POST'])
def get_subsubcategories():
    tool_type = request.form['toolType']
    sub_category = request.form['subCategory']

    # Filter by tool type and sub-category
    filtered_df = df[(df['CAT'].astype(str).str.lower() == tool_type.lower()) & 
                     (df['SUB_CAT'].astype(str).str.lower() == sub_category.lower())]

    # Get unique sub-sub-categories
    sub_sub_categories = filtered_df['SUB_SUB_CAT'].unique().tolist()
    if sub_sub_categories:
        sub_sub_categories.insert(0, "All")

    return jsonify(sub_sub_categories)


if __name__ == '__main__':
    app.run(debug=True)
