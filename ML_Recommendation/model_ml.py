import pandas as pd
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

# Membuat dataset sintesis
business_types = [
    'Makanan', 'Minuman', 'Fashion', 'Teknologi', 'Kesehatan', 
    'Pendidikan', 'Otomotif', 'Kecantikan', 'Perhiasan', 'Olahraga'
]

design_elements = {
    'color_scheme': [
        'Cerah (merah, oranye, kuning)', 
        'Sejuk (biru, hijau)', 
        'Netral (putih, abu-abu, hitam)', 
        'Pastel (pink muda, mint, lavender)',
        'Monokromatik'
    ],
    'imagery': [
        'Foto Produk', 
        'Ilustrasi', 
        'Icon Minimalis', 
        'Grafis Abstrak',
        'Foto Lifestyle'
    ],
    'typography': [
        'Modern Sans-serif', 
        'Klasik Serif', 
        'Playful Display', 
        'Clean Minimalist',
        'Bold Statement'
    ],
    'additional_elements': [
        'Pattern Geometris', 
        'Tekstur Organik', 
        'Elemen 3D', 
        'Hand-drawn Elements',
        'Gradien'
    ]
}

# Membuat dataset dengan aturan rekomendasi berdasarkan jenis bisnis
design_rules = {
    'Makanan': {
        'color_scheme': ['Cerah (merah, oranye, kuning)', 'Pastel (pink muda, mint, lavender)'],
        'imagery': ['Foto Produk', 'Icon Minimalis'],
        'typography': ['Playful Display', 'Clean Minimalist'],
        'additional_elements': ['Pattern Geometris', 'Hand-drawn Elements']
    },
    'Minuman': {
        'color_scheme': ['Sejuk (biru, hijau)', 'Pastel (pink muda, mint, lavender)'],
        'imagery': ['Foto Produk', 'Ilustrasi'],
        'typography': ['Modern Sans-serif', 'Clean Minimalist'],
        'additional_elements': ['Elemen 3D', 'Gradien']
    },
    # ... tambahkan aturan untuk jenis bisnis lainnya
}

def create_training_data():
    data = []
    
    for business in business_types:
        # Membuat beberapa variasi rekomendasi untuk setiap jenis bisnis
        num_variations = 5
        for _ in range(num_variations):
            if business in design_rules:
                rules = design_rules[business]
                entry = {
                    'business_type': business,
                    'color_scheme': np.random.choice(rules['color_scheme']),
                    'imagery': np.random.choice(rules['imagery']),
                    'typography': np.random.choice(rules['typography']),
                    'additional_elements': np.random.choice(rules['additional_elements']),
                    'success_score': np.random.uniform(0.7, 1.0)  # Simulasi skor kesuksesan
                }
            else:
                # Untuk bisnis yang belum memiliki aturan khusus
                entry = {
                    'business_type': business,
                    'color_scheme': np.random.choice(design_elements['color_scheme']),
                    'imagery': np.random.choice(design_elements['imagery']),
                    'typography': np.random.choice(design_elements['typography']),
                    'additional_elements': np.random.choice(design_elements['additional_elements']),
                    'success_score': np.random.uniform(0.5, 1.0)
                }
            data.append(entry)
    
    return pd.DataFrame(data)

class DesignRecommendationSystem:
    def __init__(self):
        self.df = create_training_data()
        self.mlb = MultiLabelBinarizer()
        
    def prepare_features(self):
        # Mengubah categorical features menjadi binary features
        features = []
        for col in ['color_scheme', 'imagery', 'typography', 'additional_elements']:
            feature_matrix = pd.get_dummies(self.df[col], prefix=col)
            features.append(feature_matrix)
        
        # Menggabungkan semua features
        self.features = pd.concat(features, axis=1)
        
    def get_recommendations(self, business_type, top_n=4):
        # Filter data berdasarkan jenis bisnis
        business_data = self.df[self.df['business_type'] == business_type]
        
        if len(business_data) == 0:
            return "Jenis bisnis tidak ditemukan dalam database."
        
        # Urutkan berdasarkan success_score
        top_designs = business_data.sort_values('success_score', ascending=False).head(top_n)
        
        recommendations = []
        for _, design in top_designs.iterrows():
            recommendation = {
                'color_scheme': design['color_scheme'],
                'imagery': design['imagery'],
                'typography': design['typography'],
                'additional_elements': design['additional_elements'],
                'confidence_score': f"{design['success_score']*100:.1f}%"
            }
            recommendations.append(recommendation)
            
        return recommendations

# Contoh penggunaan
recommender = DesignRecommendationSystem()
recommender.prepare_features()

def get_design_recommendations(business_type):
    recommendations = recommender.get_recommendations(business_type)
    
    if isinstance(recommendations, str):
        return recommendations
    
    print(f"\nRekomendasi Desain untuk Bisnis {business_type}:")
    for i, rec in enumerate(recommendations, 1):
        print(f"\nRekomendasi #{i} (Confidence: {rec['confidence_score']})")
        print("=" * 50)
        print(f"1. Skema Warna: {rec['color_scheme']}")
        print(f"2. Gambar/Visual: {rec['imagery']}")
        print(f"3. Tipografi: {rec['typography']}")
        print(f"4. Elemen Tambahan: {rec['additional_elements']}")

inputan = input('Your Bussiness : ')
get_design_recommendations()