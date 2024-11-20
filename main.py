from flask import Flask, render_template, request, jsonify
import asyncio
from rasa.core.agent import Agent
from rasa.shared.utils.io import json_to_string
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

app = Flask(__name__)

model_path = "./static/models/20241118-203538-mode-maple.tar.gz"
agent = Agent.load(model_path)

class DesignRecommender:
    def __init__(self):
        self.design_data = pd.read_excel('./static/data/design_data2.xlsx')

        self.design_data['style'] = self.design_data['style'].apply(eval)
        self.mlb = MultiLabelBinarizer()
        self.style_encoded = self.mlb.fit_transform(self.design_data['style'])
        self.tfidf = TfidfVectorizer()
        
        self.combined_features = np.hstack([
            self.style_encoded
        ])

    def get_recommendations(self, business_type, preferences):
        relevant_designs = self.design_data[
            self.design_data['business_type'] == business_type
        ]
        
        if relevant_designs.empty:
            return []
        
        user_style = self.mlb.transform([preferences['style']])
        user_vector = np.hstack([
            user_style,
        ])
        
        relevant_indices = relevant_designs.index
        similarity_scores = cosine_similarity(
            user_vector,
            self.combined_features[relevant_indices]
        )[0]
        
        top_indices = np.argsort(similarity_scores)[-2:][::-1]
        
        recommendations = relevant_designs.iloc[top_indices]
        return recommendations.to_dict(orient='records')

design_recommender = DesignRecommender()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
async def webhook():
    message = request.json.get('message', '')
    
    # Gunakan model Rasa untuk mendapatkan respons
    response = await agent.handle_text(message)
    
    # Ambil teks respons dari bot
    if response and len(response) > 0:
        bot_response = response[0].get('text', 'Maaf, saya tidak mengerti.')
    else:
        bot_response = 'Maaf, saya tidak mengerti.'
    
    return jsonify({'response': bot_response})

@app.route('/get_recommendations', methods=['POST'])
async def get_recommendations():
    business_type = request.form.get('business_type')
    style = request.form.get('stylee')

    recommendations = design_recommender.get_recommendations(business_type, {'style': style})

    if recommendations:
        top_recommendation = recommendations[0]
        second_recommendation = recommendations[1]

        return jsonify({
            'title_1': top_recommendation['title'],
            'style_1': top_recommendation['style'],
            'color_scheme_1': top_recommendation['color_scheme'],
            'typography_1': top_recommendation['typography'],
            'image_style_1': top_recommendation['image_style'],
            'image_link_1': top_recommendation['image_link'],
            'title_2': second_recommendation['title'] if second_recommendation else '',
            'style_2': second_recommendation['style'] if second_recommendation else '',
            'color_scheme_2': second_recommendation['color_scheme'] if second_recommendation else '',
            'typography_2': second_recommendation['typography'] if second_recommendation else '',
            'image_style_2': second_recommendation['image_style'] if second_recommendation else '',
            'image_link_2': second_recommendation['image_link'] if second_recommendation else ''
        })
    else:
        return jsonify({'response': 'Sorry, no recommendations available.'})

if __name__ == '__main__':
    app.run(debug=True)