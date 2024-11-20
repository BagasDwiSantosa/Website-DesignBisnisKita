import pandas as pd
from openpyxl.workbook import Workbook
data = pd.DataFrame({
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
                'restoran', 'kafe', 'makanan', 'restoran', 'restoran',
                'fashion', 'fashion', 'fashion', 'fashion', 'fashion',
                'teknologi', 'bisnis', 'kreasi', 'ritel', 'pendidikan',
                'kesehatan', 'fitness', 'kecantikan', 'real_estate', 'perhotelan'
            ],
            'style': [
                ['modern', 'cerah', 'bersih'],
                ['elegan', 'minimalis', 'sofistikasi'],
                ['kasual', 'enerjik', 'berani'],
                ['kemewahan', 'elegan', 'sofistikasi'],
                ['ramah', 'hangat', 'kasual'],
                ['kemewahan', 'elegan', 'minimalis'],
                ['perkotaan', 'berani', 'modern'],
                ['premium', 'sofistikasi', 'elegan'],
                ['trendi', 'terjangkau', 'muda'],
                ['minimalis', 'bersih', 'modern'],
                ['inovatif', 'modern', 'teknologi'],
                ['profesional', 'terpercaya', 'korporat'],
                ['kreasi', 'berani', 'unik'],
                ['bersih', 'efisien', 'terpercaya'],
                ['ramah', 'profesional', 'bersih'],
                ['terpercaya', 'profesional', 'bersih'],
                ['enerjik', 'modern', 'sehat'],
                ['elegan', 'relaksasi', 'kemewahan'],
                ['profesional', 'modern', 'terpercaya'],
                ['elegan', 'ramah', 'kemewahan']
            ],
            'color_scheme': [
                'nuansa_hangat', 'nuansa_tanah', 'warna_cerah', 'elegan_gelap', 'nuansa_hangat',
                'monokrom', 'warna_berani', 'nuansa_kemewahan', 'warna_vibran', 'nuansa_netral',
                'warna_teknologi', 'warna_korporat', 'palet_kreasi', 'warna_terpercaya', 'warna_ramah',
                'warna_medis', 'warna_enerjik', 'warna_spa', 'warna_profesional', 'warna_kemewahan'
            ],
            'typography': [
                'sans_modern', 'serif_elegan', 'campuran_playful', 'serif_klasik', 'sans_ramah',
                'serif_fashion', 'sans_perkotaan', 'serif_kemewahan', 'sans_trendi', 'sans_minimalis',
                'sans_teknologi', 'sans_korporat', 'campuran_kreasi', 'sans_bersih', 'sans_profesional',
                'sans_medis', 'sans_dinamis', 'campuran_elegan', 'sans_modern', 'serif_elegan'
            ],
            'image_style': [
                'fotografi_makanan', 'gaya_hidup', 'makanan_jalanan', 'hidangan_elegan', 'dining_kasual',
                'editorial_fashion', 'gaya_jalanan', 'fashion_kemewahan', 'gaya_hidup', 'produk_minimalis',
                'minimal_teknologi', 'foto_korporat', 'potret_kreasi', 'fokus_produk', 'pendidikan',
                'medis_profesional', 'gaya_hidup_fitness', 'spa_kesehatan', 'foto_properti', 'kemewahan_hotel'
            ]
        })

data.to_excel('design_data.xlsx', index=False)
print("Data berhasil disimpan ke 'design_data.xlsx'")