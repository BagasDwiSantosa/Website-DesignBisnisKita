# ml_model.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

class DesignRecommender:
    def __init__(self):
        # Dataset desain template
        self.design_data = pd.DataFrame({
            'design_id': range(1, 21),  # 20 template desain
            'title': [
                'Modern Restaurant Template', 'Elegant Cafe Design', 'Street Food Branding',
                'Fine Dining Experience', 'Casual Dining Template', 'Fashion Boutique Elite',
                'Streetwear Brand Design', 'Luxury Fashion Template', 'Fast Fashion Design',
                'Minimalist Fashion', 'Tech Startup Modern', 'Corporate Business',
                'Creative Agency Design', 'E-commerce Template', 'Educational Platform',
                'Healthcare Design', 'Fitness Center Template', 'Beauty Salon Design',
                'Real Estate Modern', 'Hotel Booking Template'
            ],
            'business_type': [
                'restaurant', 'cafe', 'food_truck', 'restaurant', 'restaurant', 
                'fashion', 'fashion', 'fashion', 'fashion', 'fashion',
                'technology', 'business', 'creative', 'retail', 'education',
                'healthcare', 'fitness', 'beauty', 'real_estate', 'hospitality'
            ],
            'style': [
                ['modern', 'vibrant', 'clean'],
                ['elegant', 'minimal', 'sophisticated'],
                ['casual', 'energetic', 'bold'],
                ['luxury', 'elegant', 'sophisticated'],
                ['friendly', 'warm', 'casual'],
                ['luxury', 'elegant', 'minimal'],
                ['urban', 'bold', 'modern'],
                ['premium', 'sophisticated', 'elegant'],
                ['trendy', 'affordable', 'young'],
                ['minimal', 'clean', 'modern'],
                ['innovative', 'modern', 'tech'],
                ['professional', 'trustworthy', 'corporate'],
                ['creative', 'bold', 'unique'],
                ['clean', 'efficient', 'trustworthy'],
                ['friendly', 'professional', 'clean'],
                ['trustworthy', 'professional', 'clean'],
                ['energetic', 'modern', 'healthy'],
                ['elegant', 'relaxing', 'luxurious'],
                ['professional', 'modern', 'trustworthy'],
                ['elegant', 'welcoming', 'luxurious']
            ],
            'color_scheme': [
                'warm_tones', 'earth_tones', 'bright_colors', 'dark_elegant', 'warm_tones',
                'monochrome', 'bold_colors', 'luxury_tones', 'vibrant_colors', 'neutral_tones',
                'tech_colors', 'corporate_colors', 'creative_palette', 'trust_colors', 'friendly_colors',
                'medical_colors', 'energetic_colors', 'spa_colors', 'professional_colors', 'luxury_colors'
            ],
            'typography': [
                'modern_sans', 'elegant_serif', 'playful_mixed', 'classic_serif', 'friendly_sans',
                'fashion_serif', 'urban_sans', 'luxury_serif', 'trendy_sans', 'minimal_sans',
                'tech_sans', 'corporate_sans', 'creative_mixed', 'clean_sans', 'professional_sans',
                'medical_sans', 'dynamic_sans', 'elegant_mixed', 'modern_sans', 'elegant_serif'
            ],
            'image_style': [
                'food_photography', 'lifestyle', 'street_food', 'elegant_dishes', 'casual_dining',
                'fashion_editorial', 'street_style', 'luxury_fashion', 'lifestyle', 'minimal_product',
                'tech_minimal', 'corporate_photos', 'creative_shots', 'product_focused', 'educational',
                'medical_professional', 'fitness_lifestyle', 'spa_wellness', 'property_photos', 'hotel_luxury'
            ],
            'features': [
                'menu_showcase, food_gallery, reservation_system',
                'menu_cards, ambiance_photos, contact_form',
                'menu_board, location_tracker, social_media',
                'reservation_system, wine_list, chef_profile',
                'menu_cards, delivery_integration, reviews',
                'product_gallery, size_guide, lookbook',
                'product_showcase, blog, social_feed',
                'collection_viewer, appointment_booking, VIP_area',
                'quick_shop, size_guide, wishlist',
                'minimal_gallery, quick_view, filters',
                'product_demo, support_chat, documentation',
                'service_showcase, team_profiles, contact',
                'portfolio_gallery, case_studies, blog',
                'product_catalog, cart, checkout',
                'course_catalog, learning_dashboard, progress',
                'appointment_booking, doctor_profiles, services',
                'class_schedule, member_portal, trainers',
                'service_catalog, booking_system, gallery',
                'property_listings, virtual_tours, inquiries',
                'room_booking, amenities, virtual_tour'
            ]
        })
        self.design_data = pd.read_excel('./design_data.xlsx')

        # Mengonversi kolom 'style' kembali ke bentuk list
        self.design_data['style'] = self.design_data['style'].apply(eval)

        # Preprocessing
        self.mlb = MultiLabelBinarizer()
        self.style_encoded = self.mlb.fit_transform(self.design_data['style'])
        
        # Create feature matrix
        self.tfidf = TfidfVectorizer()
        # self.features_matrix = self.tfidf.fit_transform(self.design_data['features'])
        
        # Combine style and features
        self.combined_features = np.hstack([
            self.style_encoded,
            # self.features_matrix.toarray()
        ])

    def get_recommendations(self, business_type, preferences):
        """
        Get design recommendations based on business type and preferences
        
        Parameters:
        business_type (str): Type of business
        preferences (dict): Dictionary containing user preferences
            {
                'style': ['modern', 'minimal'],
                'features': 'product_gallery, social_media'
            }
        
        Returns:
        list: List of recommended design templates
        """
        # Filter by business type first
        relevant_designs = self.design_data[
            self.design_data['business_type'] == business_type
        ]
        
        if relevant_designs.empty:
            return []
        
        # Create user preference vector
        user_style = self.mlb.transform([preferences['style']])
        # user_features = self.tfidf.transform([preferences['features']])
        user_vector = np.hstack([
            user_style,
            # user_features.toarray()
        ])
        
        # Calculate similarity scores
        relevant_indices = relevant_designs.index
        similarity_scores = cosine_similarity(
            user_vector,
            self.combined_features[relevant_indices]
        )[0]
        
        # Get top recommendations
        top_index  = similarity_scores.argmax()
        recommendation = relevant_designs.iloc[[top_index]]  # Ambil satu rekomendasi, tetap sebagai DataFrame
        return recommendation.to_dict(orient='records')[0]  

# # Implementasi dalam Flask
# from flask import Flask, request, jsonify, render_template
# import json

# app = Flask(__name__)
# recommender = DesignRecommender()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/get_recommendations', methods=['POST'])
# def get_recommendations():
#     data = request.get_json()
#     business_type = data['business_type'].lower()
#     preferences = {
#         'style': data.get('style', ['modern', 'clean']),
#         'features': data.get('features', '')
#     }
    
#     try:
#         recommendations = recommender.get_recommendations(business_type, preferences)
#         return jsonify({
#             'success': True,
#             'recommendations': recommendations
#         })
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         })

# if __name__ == '__main__':
#     app.run(debug=True)

# Inisialisasi rekomender
recommender = DesignRecommender()

# Preferensi pengguna
user_preferences = {
    'style': ['modern', 'minimal']
}

# Dapatkan rekomendasi untuk bisnis fashion
recommendations = recommender.get_recommendations('fashion', user_preferences)

# Lihat hasil rekomendasi
print(recommendations)
