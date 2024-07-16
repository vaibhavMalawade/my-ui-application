from flask import Flask, request, render_template, jsonify, send_from_directory
import pandas as pd
import os

app = Flask(__name__)

# Path to CSV files
CSV_DIRECTORY = r'E:\Code Challange\task2'
df = pd.read_csv('E:\\Code Challange\\lookup_table.csv')

@app.route('/')
def query_page():
    return render_template('query.html', email='')

@app.route('/query', methods=['POST'])
def query_superhero():
    country = request.form.get('country')
    invader_species = request.form.get('invader_species')
    role = request.form.get('role')
    
    result = df[
        (df['Country_Code'] == country) &
        (df['Invader_Species'] == invader_species) &
        (df['Role'] == role)
    ]
    
    superhero_email = result['Email'].values[0] if not result.empty else 'No superhero found'
    
    return render_template('query.html', email=superhero_email)

@app.route('/get_countries', methods=['GET'])
def get_countries():
    countries = df['Country_Code'].unique().tolist()
    return jsonify(countries)

@app.route('/get_invader_species', methods=['GET'])
def get_invader_species():
    invader_species = df['Invader_Species'].unique().tolist()
    return jsonify(invader_species)

@app.route('/get_roles', methods=['GET'])
def get_roles():
    roles = df['Role'].unique().tolist()
    return jsonify(roles)

@app.route('/dashboards')
def dashboards():
    return render_template('index.html')

@app.route('/api/superheroes', methods=['GET'])
def list_superheroes():
    files = [f.replace('.csv', '') for f in os.listdir(CSV_DIRECTORY) if f.endswith('.csv')]
    return jsonify(files)

@app.route('/api/superhero/<name>', methods=['GET'])
def get_superhero_data(name):
    filename = f"{name}.csv"
    return send_from_directory(CSV_DIRECTORY, filename)

if __name__ == '__main__':
    app.run(debug=True)
