# ml_model.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

class DesignRecommender:
    def __init__(self):
        self.design_data = pd.read_excel('./design_data2.xlsx')

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
        
        top_indices = np.argsort(similarity_scores)[-2:][::-1]  # Sort and take the top 2
        
        # Get recommendations
        recommendations = relevant_designs.iloc[top_indices]
        return recommendations.to_dict(orient='records')

recommender = DesignRecommender()

user_preferences = {
    'style': ['modern', 'minimal']
}

recommendations = recommender.get_recommendations('fashion', user_preferences)

print(recommendations)
