from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load the recommendations data
recommendations_df = pd.read_pickle('recommendations.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    applicant_id = request.args.get('applicant_id')
    
    # Check if the applicant ID is missing
    if not applicant_id:
        return jsonify({'error': 'Applicant ID is missing'}), 400
    
    # Find recommendations for the given applicant ID
    recommendations = recommendations_df[recommendations_df['applicantId'] == applicant_id]

    # Check if no recommendations were found
    if recommendations.empty:
        return jsonify({'error': 'No recommendations found for this applicant'}), 404

    # Convert the filtered DataFrame to a list of dictionaries
    recommendations_list = recommendations.to_dict(orient='records')
    return jsonify(recommendations_list)

if __name__ == "__main__":
    app.run(debug=True)
