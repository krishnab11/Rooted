import streamlit as st
from datetime import datetime, timedelta
import requests
import json
import pandas as pd
import os
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
from fpdf import FPDF
import tempfile
import unicodedata
import random
import calendar
from streamlit_option_menu import option_menu

# Load custom fonts and CSS
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&family=Playfair+Display:wght@400;600;700&display=swap');
    
    :root {
        --primary: #2e8b57;
        --primary-light: #3cb371;
        --primary-dark: #1f6140;
        --secondary: #ff7f50;
        --light: #f8f9fa;
        --dark: #343a40;
        --gray: #6c757d;
        --light-gray: #e9ecef;
        --success: #28a745;
        --info: #17a2b8;
        --warning: #ffc107;
        --danger: #dc3545;
    }
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Playfair Display', serif;
        color: var(--primary-dark);
    }
    
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Navbar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--primary), var(--primary-dark));
        color: white;
    }
    
    [data-testid="stSidebar"] .sidebar-content {
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] .sidebar-title {
        color: white !important;
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        margin-bottom: 2rem;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
        padding: 0 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        padding: 0 20px;
        background-color: white;
        border-radius: 8px 8px 0 0;
        border: 1px solid var(--light-gray);
        color: var(--dark);
        font-weight: 600;
        transition: all 0.3s ease;
        margin: 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: var(--light);
        color: var(--primary);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white;
        color: var(--primary) !important;
        border-bottom: 3px solid var(--primary);
        box-shadow: none;
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: none;
        background-color: var(--primary);
        color: white;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(46, 139, 87, 0.3);
        background-color: var(--primary-light);
        color: white;
    }
    
    .stButton>button:focus {
        background-color: var(--primary-dark);
        color: white;
    }
    
    /* Input styling */
    .stTextInput>div>div>input, 
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>div,
    .stSlider>div>div>div>div {
        border-radius: 8px !important;
        border: 1px solid var(--light-gray) !important;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid var(--light-gray);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .plant-card {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .plant-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .weather-card {
        background: linear-gradient(135deg, #6e8efb, #a777e3);
        color: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    /* Badge styling */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 16px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    
    .badge-easy {
        background-color: #d4edda;
        color: #155724;
    }
    
    .badge-medium {
        background-color: #fff3cd;
        color: #856404;
    }
    
    .badge-hard {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    .badge-primary {
        background-color: #d1e7dd;
        color: var(--primary-dark);
    }
    
    .badge-secondary {
        background-color: #ffe3e3;
        color: var(--secondary);
    }
    
    /* Icon styling */
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: var(--primary);
    }
    
    /* Testimonial styling */
    .testimonial-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-left: 4px solid var(--primary);
    }
    
    .testimonial-author {
        font-weight: 600;
        color: var(--primary);
        margin-top: 10px;
    }
    
    /* Footer styling */
    .footer {
        padding: 30px 0;
        text-align: center;
        color: var(--gray);
        font-size: 14px;
        border-top: 1px solid var(--light-gray);
        margin-top: 40px;
        background-color: white;
    }
    
    /* Hero section */
    .hero {
        background: linear-gradient(135deg, var(--primary), var(--primary-dark));
        color: white;
        padding: 4rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .hero h1 {
        color: white !important;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .hero p {
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    /* Stats counter */
    .stat-card {
        text-align: center;
        padding: 1.5rem;
        border-radius: 12px;
        background: white;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0.5rem;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: var(--gray);
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .stTabs [data-baseweb="tab"] {
            padding: 0 15px;
            font-size: 14px;
            height: 40px;
        }
        
        .hero {
            padding: 2rem 1rem;
        }
        
        .hero h1 {
            font-size: 1.8rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

# Sample plant data with enhanced fields
plants = [
    {
        "name": "Tulsi (तुळस / तुलसी)",
        "image": "tulsi.jpeg",
        "season": "Summer",
        "care": "Water daily, keep in sunlight. Prefers warm temperatures and well-drained soil.",
        "days_to_grow": 60,
        "water_ltr": 0.25,
        "category": "Herb",
        "sunlight": "Full Sun",
        "difficulty": "Easy",
        "uses": ["Medicinal", "Religious", "Culinary"],
        "companions": ["Tomato", "Pepper"],
        "pests": ["Aphids", "Whiteflies"],
        "soil": "Well-drained, loamy",
        "fun_fact": "Considered sacred in Hinduism and often planted in courtyards."
    },
    {
        "name": "Aloe Vera (कोरफड / घृतकुमारी)",
        "image": "Aloe vera.jpeg",
        "season": "All Seasons",
        "care": "Needs bright light and occasional watering. Allow soil to dry between waterings.",
        "days_to_grow": 90,
        "water_ltr": 0.15,
        "category": "Succulent",
        "sunlight": "Partial Sun",
        "difficulty": "Easy",
        "uses": ["Medicinal", "Cosmetic"],
        "companions": ["Garlic", "Onion"],
        "pests": ["Mealybugs"],
        "soil": "Sandy, well-drained",
        "fun_fact": "The gel inside the leaves can be used to treat burns and skin irritations."
    },
    {
        "name": "Marigold (झेंडू / गेंदा)",
        "image": "marigold.jpeg",
        "season": "Winter",
        "care": "Water regularly and keep in sunlight. Deadhead flowers to encourage more blooms.",
        "days_to_grow": 70,
        "water_ltr": 0.3,
        "category": "Flower",
        "sunlight": "Full Sun",
        "difficulty": "Easy",
        "uses": ["Ornamental", "Pest control"],
        "companions": ["Tomato", "Cucumber"],
        "pests": ["Aphids", "Spider mites"],
        "soil": "Well-drained",
        "fun_fact": "Marigolds are often used in festivals and religious ceremonies in India."
    },
    {
        "name": "Spinach (पालक / पालक)",
        "image": "spinach.jpeg",
        "season": "Winter",
        "care": "Water every 2 days, partial sunlight. Harvest outer leaves to allow center to keep growing.",
        "days_to_grow": 40,
        "water_ltr": 0.2,
        "category": "Vegetable",
        "sunlight": "Partial Sun",
        "difficulty": "Easy",
        "uses": ["Culinary"],
        "companions": ["Strawberry", "Peas"],
        "pests": ["Leaf miners"],
        "soil": "Loamy, rich in organic matter",
        "fun_fact": "Spinach is rich in iron and other nutrients, making it a superfood."
    },
    {
        "name": "Money Plant (मनी प्लांट / मनी प्लांट)",
        "image": "money_plant.jpeg",
        "season": "All Seasons",
        "care": "Grows in water or soil, indirect sunlight. Wipe leaves occasionally to remove dust.",
        "days_to_grow": 30,
        "water_ltr": 0.1,
        "category": "Indoor",
        "sunlight": "Indirect Light",
        "difficulty": "Very Easy",
        "uses": ["Ornamental", "Air purifier"],
        "companions": [],
        "pests": ["Spider mites"],
        "soil": "Well-drained",
        "fun_fact": "Believed to bring good luck and prosperity according to Feng Shui."
    },
    {
        "name": "Neem (कडुनिंब / नीम)",
        "image": "neem.jpeg",
        "season": "Summer",
        "care": "Needs full sun and well-drained soil. Drought tolerant once established.",
        "days_to_grow": 100,
        "water_ltr": 0.3,
        "category": "Tree",
        "sunlight": "Full Sun",
        "difficulty": "Medium",
        "uses": ["Medicinal", "Pest control"],
        "companions": [],
        "pests": ["Scale insects"],
        "soil": "Well-drained",
        "fun_fact": "Neem has antibacterial and antifungal properties, used in many traditional remedies."
    },
    {
        "name": "Lemongrass (गवती चहा / लेमनग्रास)",
        "image": "Lemongrass.jpeg",
        "season": "Monsoon",
        "care": "Water regularly, grows fast. Divide clumps every few years to maintain vigor.",
        "days_to_grow": 75,
        "water_ltr": 0.2,
        "category": "Grass",
        "sunlight": "Full Sun",
        "difficulty": "Easy",
        "uses": ["Culinary", "Mosquito repellent"],
        "companions": ["Mint", "Basil"],
        "pests": ["Rust"],
        "soil": "Well-drained",
        "fun_fact": "Contains citronella, a natural mosquito repellent."
    },
    {
        "name": "Coriander (धणे / धनिया)",
        "image": "Coriander.jpg",
        "season": "Winter",
        "care": "Keep soil moist and well-drained. Sow seeds successively for continuous harvest.",
        "days_to_grow": 40,
        "water_ltr": 0.15,
        "category": "Herb",
        "sunlight": "Partial Sun",
        "difficulty": "Easy",
        "uses": ["Culinary"],
        "companions": ["Peas", "Spinach"],
        "pests": ["Aphids"],
        "soil": "Loamy",
        "fun_fact": "Both leaves (cilantro) and seeds (coriander) are used in cooking."
    },
    {
        "name": "Mint (पुदिना / पुदीना)",
        "image": "mint.jpeg",
        "season": "Winter",
        "care": "Partial sunlight, water frequently. Best grown in containers as it spreads aggressively.",
        "days_to_grow": 50,
        "water_ltr": 0.2,
        "category": "Herb",
        "sunlight": "Partial Sun",
        "difficulty": "Easy",
        "uses": ["Culinary", "Medicinal"],
        "companions": ["Carrot", "Cabbage"],
        "pests": ["Spider mites"],
        "soil": "Moist",
        "fun_fact": "There are over 600 varieties of mint with different flavors and aromas."
    },
    {
        "name": "Curry Leaves (कढीपत्ता / करी पत्ता)",
        "image": "curry leaves.jpeg",
        "season": "Summer",
        "care": "Full sun, moderate watering. Protect from frost in winter.",
        "days_to_grow": 80,
        "water_ltr": 0.25,
        "category": "Tree",
        "sunlight": "Full Sun",
        "difficulty": "Medium",
        "uses": ["Culinary"],
        "companions": [],
        "pests": ["Scale insects"],
        "soil": "Well-drained",
        "fun_fact": "Essential ingredient in South Indian cuisine, adds distinctive flavor to dishes."
    },
    {
        "name": "Basil (साबा / तुलसी विदेशी)",
        "image": "basil.jpeg",
        "season": "Summer",
        "care": "Water regularly, needs warmth. Pinch off flower buds to encourage leaf growth.",
        "days_to_grow": 60,
        "water_ltr": 0.2,
        "category": "Herb",
        "sunlight": "Full Sun",
        "difficulty": "Easy",
        "uses": ["Culinary", "Medicinal"],
        "companions": ["Tomato", "Pepper"],
        "pests": ["Aphids"],
        "soil": "Well-drained",
        "fun_fact": "Considered a sacred herb in many cultures and used in religious ceremonies."
    },
    {
        "name": "Tomato (टोमॅटो / टमाटर)",
        "image": "tomato.jpeg",
        "season": "Winter",
        "care": "Full sunlight, daily watering. Provide support for vines to climb.",
        "days_to_grow": 80,
        "water_ltr": 0.4,
        "category": "Vegetable",
        "sunlight": "Full Sun",
        "difficulty": "Medium",
        "uses": ["Culinary"],
        "companions": ["Basil", "Carrot"],
        "pests": ["Whiteflies"],
        "soil": "Well-drained, rich",
        "fun_fact": "Botanically a fruit but legally declared a vegetable by the US Supreme Court in 1893."
    },
    {
        "name": "Chili (मिरची / मिर्च)",
        "image": "chili.jpeg",
        "season": "Summer",
        "care": "Warm climate, daily watering. Harvest regularly to encourage more fruit production.",
        "days_to_grow": 90,
        "water_ltr": 0.3,
        "category": "Vegetable",
        "sunlight": "Full Sun",
        "difficulty": "Medium",
        "uses": ["Culinary"],
        "companions": ["Basil", "Onion"],
        "pests": ["Aphids"],
        "soil": "Well-drained",
        "fun_fact": "The spiciness of chili peppers is measured in Scoville Heat Units (SHU)."
    },
    {
        "name": "Brinjal (वांगे / बैंगन)",
        "image": "brinjal.jpeg",
        "season": "Winter",
        "care": "Needs warmth and rich soil. Stake plants to support heavy fruit.",
        "days_to_grow": 85,
        "water_ltr": 0.4,
        "category": "Vegetable",
        "sunlight": "Full Sun",
        "difficulty": "Medium",
        "uses": ["Culinary"],
        "companions": ["Beans", "Spinach"],
        "pests": ["Fruit borers"],
        "soil": "Well-drained, rich",
        "fun_fact": "Technically a berry and comes in many colors including purple, white, green and striped."
    },
    {
        "name": "Fenugreek (मेथी / मेथी)",
        "image": "Fenugreek.jpeg",
        "season": "Winter",
        "care": "Moist soil, grows quickly. Harvest leaves when young for best flavor.",
        "days_to_grow": 30,
        "water_ltr": 0.2,
        "category": "Herb",
        "sunlight": "Full Sun",
        "difficulty": "Easy",
        "uses": ["Culinary", "Medicinal"],
        "companions": ["Peas", "Spinach"],
        "pests": ["Aphids"],
        "soil": "Loamy",
        "fun_fact": "Seeds are used as a spice and leaves as a herb in Indian cuisine."
    },
    {
        "name": "Peas (हरभरा / मटर)",
        "image": "peas.jpeg",
        "season": "Winter",
        "care": "Cool weather, daily watering. Provide trellis for climbing varieties.",
        "days_to_grow": 70,
        "water_ltr": 0.35,
        "category": "Vegetable",
        "sunlight": "Full Sun",
        "difficulty": "Easy",
        "uses": ["Culinary"],
        "companions": ["Carrot", "Radish"],
        "pests": ["Aphids"],
        "soil": "Loamy",
        "fun_fact": "One of the first food crops cultivated by humans, dating back to 4800 BC."
    },
    {
        "name": "Lady Finger (भेंडी / भिंडी)",
        "image": "lady finger.jpeg",
        "season": "Summer",
        "care": "Water regularly, needs warmth. Harvest pods when young and tender.",
        "days_to_grow": 60,
        "water_ltr": 0.3,
        "category": "Vegetable",
        "sunlight": "Full Sun",
        "difficulty": "Medium",
        "uses": ["Culinary"],
        "companions": ["Corn", "Beans"],
        "pests": ["Aphids"],
        "soil": "Well-drained",
        "fun_fact": "Also known as okra, the mucilaginous texture is great for thickening stews."
    },
    {
        "name": "Bitter Gourd (कारले / करेला)",
        "image": "Bitter Gourd.jpeg",
        "season": "Monsoon",
        "care": "Trellis support, daily watering. Harvest when fruits are young to reduce bitterness.",
        "days_to_grow": 95,
        "water_ltr": 0.4,
        "category": "Vegetable",
        "sunlight": "Full Sun",
        "difficulty": "Medium",
        "uses": ["Culinary", "Medicinal"],
        "companions": ["Beans", "Corn"],
        "pests": ["Fruit flies"],
        "soil": "Well-drained",
        "fun_fact": "Used in traditional medicine to help regulate blood sugar levels."
    },
    {
        "name": "Cabbage (कोबी / पत्ता गोभी)",
        "image": "Cabbage.jpeg",
        "season": "Winter",
        "care": "Cool climate, water every 2 days. Protect from cabbage worms with row covers.",
        "days_to_grow": 90,
        "water_ltr": 0.3,
        "category": "Vegetable",
        "sunlight": "Full Sun",
        "difficulty": "Medium",
        "uses": ["Culinary"],
        "companions": ["Beets", "Celery"],
        "pests": ["Cabbage worms"],
        "soil": "Loamy",
        "fun_fact": "The largest cabbage on record weighed over 62 kg (138 lb)."
    },
    {
        "name": "Bottle Gourd (दुधी / लौकी)",
        "image": "Bottle Gourd.jpeg",
        "season": "Monsoon",
        "care": "Trellis required, plenty of water. Harvest when skin is still tender.",
        "days_to_grow": 80,
        "water_ltr": 0.45,
        "category": "Vegetable",
        "sunlight": "Full Sun",
        "difficulty": "Medium",
        "uses": ["Culinary"],
        "companions": ["Beans", "Corn"],
        "pests": ["Powdery mildew"],
        "soil": "Well-drained",
        "fun_fact": "Dried gourds are used as water containers, musical instruments, and birdhouses."
    },
    {
        "name": "Rose (गुलाब / गुलाब)",
        "image": "rose.jpeg",
        "season": "Winter",
        "care": "Water every 2 days, full sunlight. Prune in late winter to encourage new growth.",
        "days_to_grow": 60,
        "water_ltr": 0.25,
        "category": "Flower",
        "sunlight": "Full Sun",
        "difficulty": "Medium",
        "uses": ["Ornamental"],
        "companions": ["Garlic", "Marigold"],
        "pests": ["Aphids"],
        "soil": "Well-drained",
        "fun_fact": "There are over 300 species of roses and thousands of cultivars."
    },
    {
        "name": "Sunflower (सूर्यमुखी / सूरजमुखी)",
        "image": "sunflower.jpeg",
        "season": "Summer",
        "care": "Water weekly, full sunlight. May need staking in windy areas.",
        "days_to_grow": 70,
        "water_ltr": 0.5,
        "category": "Flower",
        "sunlight": "Full Sun",
        "difficulty": "Easy",
        "uses": ["Ornamental", "Edible seeds"],
        "companions": ["Cucumber", "Squash"],
        "pests": ["Birds"],
        "soil": "Well-drained",
        "fun_fact": "Sunflower heads track the sun's movement from east to west (heliotropism)."
    },
    {
        "name": "Lily (कमल / कमल)",
        "image": "lily.jpeg",
        "season": "Summer",
        "care": "Water daily, partial sunlight. Remove spent flowers to encourage more blooms.",
        "days_to_grow": 50,
        "water_ltr": 0.2,
        "category": "Flower",
        "sunlight": "Partial Sun",
        "difficulty": "Medium",
        "uses": ["Ornamental"],
        "companions": ["Rose", "Marigold"],
        "pests": ["Aphids"],
        "soil": "Well-drained",
        "fun_fact": "In many cultures, lilies symbolize purity and refined beauty."
    },
    {
        "name": "Hibiscus (जास्वंद / जास्वंद)",
        "image": "hibiscus.jpeg",
        "season": "Summer",
        "care": "Water every 3 days, full sunlight. Prune to maintain shape and encourage flowering.",
        "days_to_grow": 60,
        "water_ltr": 0.3,
        "category": "Flower",
        "sunlight": "Full Sun",
        "difficulty": "Easy",
        "uses": ["Ornamental", "Medicinal"],
        "companions": ["Marigold", "Basil"],
        "pests": ["Whiteflies"],
        "soil": "Well-drained",
        "fun_fact": "Hibiscus tea is popular worldwide and known for its tart, cranberry-like flavor."
    }
]

# Page Setup
st.set_page_config(
    page_title="Rooted - Plant Care Buddy", 
    layout="wide",
    page_icon="🌿",
    initial_sidebar_state="collapsed"
)

# Load CSS
load_css()

# Load plant data from CSV
@st.cache_data
def load_plant_data():
    try:
        plant_df = pd.read_csv('plant_data.csv')
        return plant_df
    except:
        st.error("Could not load plant data. Using sample data instead.")
        return None

plant_df = load_plant_data()

# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🏠 Home", 
    "🌱 Plant Library", 
    "✨ Recommendations", 
    "📝 Care Guide", 
    "🧠 Plant Quiz",
    "⛅ Weather", 
    "💬 Feedback"
])

with tab1:
    # Hero Section
    st.markdown("""
    <div class='hero'>
        <h1>🌿 Rooted - Your Plant Care Buddy</h1>
        <p>Grow green, stay rooted! Discover the joy of gardening with our smart plant care system.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Counter
    st.subheader("🌍 Our Community")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>50+</div>
            <div class='stat-label'>Plant Varieties</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>10K+</div>
            <div class='stat-label'>Happy Gardeners</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>95%</div>
            <div class='stat-label'>Success Rate</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>24/7</div>
            <div class='stat-label'>Support</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Features section
    st.subheader("🌟 Key Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <div class='feature-icon'>🌱</div>
            <h4>Plant Library</h4>
            <p>Comprehensive database of 50+ plants with detailed care instructions</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <div class='feature-icon'>✨</div>
            <h4>Smart Recommendations</h4>
            <p>Get personalized plant suggestions based on your environment</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class='card' style='text-align: center;'>
            <div class='feature-icon'>📝</div>
            <h4>Care Guides</h4>
            <p>Generate and download customized care guides for your plants</p>
        </div>
        """, unsafe_allow_html=True)
    
    # How It Works
    st.subheader("🛠️ How It Works")
    st.markdown("""
    <div class='card'>
        <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;'>
            <div style='text-align: center;'>
                <h3>1</h3>
                <p><b>Select Your Plants</b></p>
                <p>Choose from our extensive plant library or add your own</p>
            </div>
            <div style='text-align: center;'>
                <h3>2</h3>
                <p><b>Get Care Plan</b></p>
                <p>Receive personalized care instructions based on your plants</p>
            </div>
            <div style='text-align: center;'>
                <h3>3</h3>
                <p><b>Track Progress</b></p>
                <p>Monitor your plants' growth and health over time</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Testimonials
    st.subheader("💚 What Our Users Say")
    testimonial_col1, testimonial_col2 = st.columns(2)
    with testimonial_col1:
        st.markdown("""
        <div class='testimonial-card'>
            <p>"Rooted transformed my brown thumb into a green one! My plants have never been healthier."</p>
            <div class='testimonial-author'>- Priya K., Mumbai</div>
        </div>
        """, unsafe_allow_html=True)
    with testimonial_col2:
        st.markdown("""
        <div class='testimonial-card'>
            <p>"The personalized care guides are a game-changer. My urban garden is thriving!"</p>
            <div class='testimonial-author'>- Rajesh P., Bangalore</div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.header("🌿 Plant Library")
    st.markdown("Explore our comprehensive plant database with detailed care information.")
    
    # Search and filters
    with st.expander("🔍 Search & Filters", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            search_query = st.text_input("Search plants by name")
        with col2:
            category_filter = st.multiselect(
                "Filter by category",
                options=["All"] + sorted(list(set(p["category"] for p in plants if "category" in p))),
                default=["All"]
            )
        with col3:
            difficulty_filter = st.multiselect(
                "Filter by difficulty",
                options=["All", "Easy", "Medium", "Hard"],
                default=["All"]
            )
    
    # Filter plants
    filtered_plants = plants
    if search_query:
        filtered_plants = [p for p in filtered_plants if search_query.lower() in p["name"].lower()]
    if "All" not in category_filter:
        filtered_plants = [p for p in filtered_plants if p.get("category") in category_filter]
    if "All" not in difficulty_filter:
        filtered_plants = [p for p in filtered_plants if p.get("difficulty") in difficulty_filter]
    
    # Display plants in a grid
    if not filtered_plants:
        st.warning("No plants match your filters. Try adjusting your search criteria.")
    else:
        cols = st.columns(3)
        for i, plant in enumerate(filtered_plants):
            with cols[i % 3]:
                with st.container():
                    st.markdown(f"""
                    <div class='card plant-card'>
                        <div style='text-align: center;'>
                            <img src='https://source.unsplash.com/300x200/?{plant["name"].split()[0]},plant' width='100%' style='border-radius: 8px; margin-bottom: 10px;'>
                            <h4>{plant["name"]}</h4>
                            <div style='display: flex; margin-bottom: 10px;'>
                                <span class='badge badge-{plant.get("difficulty", "easy").lower()}'>{plant.get("difficulty", "Easy")}</span>
                                <span class='badge' style='background-color: #e2f0fb; color: #0d6efd;'>{plant.get("category", "Plant")}</span>
                            </div>
                            <p><b>Season:</b> {plant["season"]}</p>
                            <p><b>Care Level:</b> {'⭐' if plant['days_to_grow'] <= 60 else '⭐⭐' if plant['days_to_grow'] <= 90 else '⭐⭐⭐'}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Detailed view when a plant is selected
        selected_plant_name = st.selectbox("Select a plant to view detailed information:", [p["name"] for p in filtered_plants])
        selected_plant = next(p for p in filtered_plants if p["name"] == selected_plant_name)
        
        with st.container():
             plant_details_html = f"""
    <div class='card' style='margin-top: 20px;'>
        <div style='display: flex; gap: 20px;'>
            <div style='flex: 1;'>
                <img src='https://source.unsplash.com/400x300/?{selected_plant["name"].split()[0]},plant' width='100%' style='border-radius: 8px;'>
            </div>
            <div style='flex: 2;'>
                <h2 style='color: var(--primary-dark);'>{selected_plant["name"]}</h2>
                <div style='display: flex; gap: 10px; margin-bottom: 15px;'>
                    <span class='badge badge-{selected_plant.get("difficulty", "easy").lower()}'>{selected_plant.get("difficulty", "Easy")}</span>
                    <span class='badge' style='background-color: #e2f0fb; color: #0d6efd;'>{selected_plant.get("category", "Plant")}</span>
                    <span class='badge' style='background-color: #fff3cd; color: #856404;'>🌱 {selected_plant["season"]} Season</span>
                </div>
                
                <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-bottom: 20px;'>
                    <div style='background-color: #f8f9fa; padding: 10px; border-radius: 8px;'>
                        <div style='font-size: 12px; color: var(--gray);'>SUNLIGHT</div>
                        <div style='font-weight: 600;'>{selected_plant.get("sunlight", "Full Sun")}</div>
                    </div>
                    <div style='background-color: #f8f9fa; padding: 10px; border-radius: 8px;'>
                        <div style='font-size: 12px; color: var(--gray);'>WATER</div>
                        <div style='font-weight: 600;'>{selected_plant["water_ltr"]} L per day</div>
                    </div>
                    <div style='background-color: #f8f9fa; padding: 10px; border-radius: 8px;'>
                        <div style='font-size: 12px; color: var(--gray);'>GROWTH TIME</div>
                        <div style='font-weight: 600;'>{selected_plant["days_to_grow"]} days</div>
                    </div>
                    <div style='background-color: #f8f9fa; padding: 10px; border-radius: 8px;'>
                        <div style='font-size: 12px; color: var(--gray);'>DIFFICULTY</div>
                        <div style='font-weight: 600;'>{selected_plant.get("difficulty", "Easy")}</div>
                    </div>
                </div>
                
                <h4 style='color: var(--primary-dark);'>Care Instructions</h4>
                <p>{selected_plant["care"]}</p>
                
                <div style='margin-top: 20px;'>
                    <h4 style='color: var(--primary-dark);'>Plant Details</h4>
                    <div style='display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;'>
                        <div>
                            <p><b>Common Uses:</b> {', '.join(selected_plant.get('uses', ['N/A']))}</p>
                            <p><b>Companion Plants:</b> {', '.join(selected_plant.get('companions', ['N/A']))}</p>
                        </div>
                        <div>
                            <p><b>Common Pests:</b> {', '.join(selected_plant.get('pests', ['N/A']))}</p>
                            <p><b>Ideal Soil:</b> {selected_plant.get('soil', 'N/A')}</p>
                        </div>
                    </div>
                </div>
                
                <div style='margin-top: 20px;'>
                    <h4 style='color: var(--primary-dark);'>Did You Know?</h4>
                    <div class='card' style='background-color: #f0f8f4; padding: 15px;'>
                        <p>{selected_plant.get('fun_fact', 'No fun fact available for this plant.')}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(plant_details_html, unsafe_allow_html=True)


with tab3:
    st.header("✨ Plant Recommendations")
    st.markdown("Get personalized plant suggestions based on your environment and preferences.")
    
    with st.container():
        st.markdown("""
        <div class='card'>
            <h3 style='color: var(--primary-dark);'>Tell Us About Your Space</h3>
            <p>Answer a few questions to get the best plant recommendations for your home or garden.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.form("recommendation_form"):
        col1, col2 = st.columns(2)
        with col1:
            season = st.selectbox("Current Season:", ["Summer", "Winter", "Monsoon", "All Seasons"])
            space = st.selectbox("Available Space:", ["Small pots", "Medium pots", "Large pots", "Garden"])
            sunlight = st.selectbox("Sunlight Availability:", ["Full Sun (6+ hours)", "Partial Sun (3-6 hours)", "Shade (<3 hours)", "Indirect Light"])
        with col2:
            experience = st.selectbox("Your Experience Level:", ["Beginner", "Intermediate", "Expert"])
            purpose = st.multiselect("Plant Purpose:", ["Ornamental", "Edible", "Medicinal", "Air Purification"])
            care_time = st.select_slider("Weekly Care Time Available:", ["<1 hour", "1-3 hours", "3-5 hours", "5+ hours"])
        
        submitted = st.form_submit_button("Get Recommendations")
        
        if submitted:
            st.success("Here are plants that match your criteria:")
            
            # Filter plants based on user input
            filtered_plants = [p for p in plants if p["season"] == season or p["season"] == "All Seasons"]
            
            # Space filtering
            if space == "Small pots":
                filtered_plants = [p for p in filtered_plants if p["water_ltr"] <= 0.2]
            elif space == "Medium pots":
                filtered_plants = [p for p in filtered_plants if p["water_ltr"] <= 0.3]
            
            # Experience filtering
            if experience == "Beginner":
                filtered_plants = [p for p in filtered_plants if p.get("difficulty") in ["Easy", None]]
            elif experience == "Intermediate":
                filtered_plants = [p for p in filtered_plants if p.get("difficulty") in ["Easy", "Medium", None]]
            
            # Sunlight filtering
            if sunlight == "Full Sun (6+ hours)":
                filtered_plants = [p for p in filtered_plants if p.get("sunlight") in ["Full Sun"]]
            elif sunlight == "Partial Sun (3-6 hours)":
                filtered_plants = [p for p in filtered_plants if p.get("sunlight") in ["Partial Sun", "Full Sun"]]
            elif sunlight == "Shade (<3 hours)":
                filtered_plants = [p for p in filtered_plants if p.get("sunlight") in ["Partial Sun", "Shade"]]
            elif sunlight == "Indirect Light":
                filtered_plants = [p for p in filtered_plants if p.get("sunlight") in ["Indirect Light", "Shade"]]
            
            # Purpose filtering
            if purpose:
                filtered_plants = [p for p in filtered_plants if any(use.lower() in [u.lower() for u in p.get("uses", [])] for use in purpose)]
            
            # Care time filtering
            if care_time == "<1 hour":
                filtered_plants = [p for p in filtered_plants if p["days_to_grow"] >= 60]
            elif care_time == "1-3 hours":
                filtered_plants = [p for p in filtered_plants if p["days_to_grow"] >= 30]
            
            if filtered_plants:
                # Sort by difficulty (easy first)
                filtered_plants.sort(key=lambda x: 0 if x.get("difficulty") == "Easy" else 1 if x.get("difficulty") == "Medium" else 2)
                
                # Display recommendations
                cols = st.columns(3)
                for i, plant in enumerate(filtered_plants[:6]):  # Show top 6 results
                    with cols[i % 3]:
                        with st.container():
                            st.markdown(f"""
                            <div class='card plant-card'>
                                <div style='text-align: center;'>
                                    <img src='https://source.unsplash.com/300x200/?{plant["name"].split()[0]},plant' width='100%' style='border-radius: 8px; margin-bottom: 10px;'>
                                    <h4>{plant["name"]}</h4>
                                    <div style='display: flex; margin-bottom: 10px;'>
                                        <span class='badge badge-{plant.get("difficulty", "easy").lower()}'>{plant.get("difficulty", "Easy")}</span>
                                        <span class='badge' style='background-color: #e2f0fb; color: #0d6efd;'>{plant.get("category", "Plant")}</span>
                                    </div>
                                    <p><b>Season:</b> {plant["season"]}</p>
                                    <p><b>Water:</b> {plant["water_ltr"]} L/day</p>
                                    <p><b>Sunlight:</b> {plant.get("sunlight", "Full Sun")}</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
            else:
                st.warning("No plants match all your criteria. Try adjusting your selections.")

with tab4:
    st.header("📝 Personalized Care Guide Generator")
    st.markdown("Create a customized care guide for your specific plant and environment.")
    
    with st.container():
        st.markdown("""
        <div class='card'>
            <h3 style='color: var(--primary-dark);'>Plant Information</h3>
            <p>Provide details about your plant to generate a personalized care guide.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.form("care_guide_form"):
        col1, col2 = st.columns(2)
        with col1:
            selected_plant = st.selectbox("Select your plant:", [p["name"] for p in plants])
            plant_age = st.slider("Plant age (days):", 0, 365, 30)
            location = st.selectbox("Plant location:", ["Indoor", "Outdoor", "Balcony", "Terrace", "Garden"])
        with col2:
            experience_level = st.selectbox("Your experience level:", ["Beginner", "Intermediate", "Advanced"])
            soil_type = st.selectbox("Soil type:", ["Potting Mix", "Garden Soil", "Sandy", "Clay", "Loamy", "Other"])
            has_pests = st.checkbox("Currently has pest issues")
        
        submitted = st.form_submit_button("Generate Care Guide")
        
        if submitted:
            # Find the selected plant
            plant = next(p for p in plants if p["name"] == selected_plant)
            
            # Determine plant stage
            if plant_age < plant['days_to_grow']/3:
                stage = "Seedling"
                stage_tips = """- Keep soil consistently moist but not waterlogged
                - Provide gentle light (avoid direct harsh sunlight)
                - Maintain stable temperatures"""
            elif plant_age < plant['days_to_grow']*2/3:
                stage = "Vegetative Growth"
                stage_tips = """- Increase watering as plant grows
                - Begin fertilizing with diluted nutrients
                - Provide support if needed (staking)"""
            else:
                stage = "Mature"
                stage_tips = """- Watch for flowering/fruiting signs
                - Reduce nitrogen fertilizer
                - Harvest regularly to encourage production"""
            
            # Generate detailed care guide
            guide = f"""
            # {selected_plant.split('(')[0].strip()} Care Guide  
            ## 🌿 Basic Information  
            - **Type:** {plant.get('category', 'N/A')}  
            - **Best Season:** {plant['season']}  
            - **Growth Time:** {plant['days_to_grow']} days  
            - **Current Stage:** {stage} ({plant_age} days old)  
            - **Location:** {location}  
            
            ## ☀️ Light Requirements  
            - **Ideal Sunlight:** {plant.get('sunlight', 'Full Sun')}  
            - **Location Tips:** {'Keep near bright window' if location == 'Indoor' else 'Morning sun with afternoon shade' if location in ['Balcony', 'Terrace'] else '6+ hours direct sunlight'}  
            
            ## 💧 Watering Guide  
            - **Frequency:** {'Every 3-4 days' if location == 'Indoor' else 'Daily in summer' if location == 'Garden' else 'When top 1" of soil is dry'}  
            - **Amount:** {plant['water_ltr']} liters per watering  
            - **Best Time:** Early morning (6-9 AM)  
            - **Watering Tips:**  
              • Use room temperature water  
              • Water at base of plant, not leaves  
              • Ensure proper drainage  
            
            ## 🌱 Soil & Fertilization  
            - **Soil Type:** {soil_type}  
            - **Fertilizer:** {plant.get('fertilizer', 'Balanced NPK (10-10-10)')}  
            - **Fertilizing Schedule:**  
              • {stage}: {'Every 2 weeks' if stage == 'Vegetative Growth' else 'Monthly' if stage == 'Mature' else 'Not needed yet'}  
            - **Soil pH:** 6.0-7.0 (most plants prefer slightly acidic)  
            
            ## 🐛 Pest & Disease Management  
            - **Common Issues:** {', '.join(plant.get('pests', ['Aphids', 'Spider mites']))}  
            - **Prevention:**  
              • Neem oil spray weekly  
              • Proper air circulation  
              • Avoid overwatering  
            - **Current Issues:** {'Treat with neem oil or insecticidal soap' if has_pests else 'No current issues reported'}  
            
            ## 📅 Monthly Care Calendar  
            | Month        | Key Tasks                 |
            |--------------|---------------------------|
            | 1-{plant['days_to_grow']//3} | Watering, Gentle light |
            | {plant['days_to_grow']//3}-{plant['days_to_grow']*2//3} | Fertilizing, Pruning |
            | {plant['days_to_grow']*2//3}-{plant['days_to_grow']} | Harvesting, Disease watch |
            
            ## 💡 Expert Tips for {experience_level}  
            {stage_tips}  
            - **Companion Plants:** {', '.join(plant.get('companions', ['N/A']))}  
            - **Avoid Planting With:** {['Onions', 'Walnut trees', 'Fennel'][hash(selected_plant)%3]}  
            - **Harvesting Tip:** {'Morning harvest has best flavor' if 'Vegetable' in plant.get('category', '') else ''}  
            """
            
            # Display in app
            with st.container():
                st.markdown("""
                <div class='card'>
                    <h3 style='color: var(--primary-dark);'>Your Personalized Care Guide</h3>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(guide)
                
                # PDF Generation
                from fpdf import FPDF
                import tempfile
                import unicodedata
                
                def clean_text(text):
                    """Remove problematic characters while preserving structure"""
                    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
                
                # Initialize PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                
                # Add title
                pdf.set_font("Arial", size=16, style='B') 
                pdf.cell(200, 10, txt=clean_text(f"{selected_plant.split('(')[0].strip()} Care Guide"), ln=1, align='C')
                pdf.ln(10)
                
                # Process guide sections
                sections = guide.split('## ')[1:]
                for section in sections:
                    if not section.strip():
                        continue
                        
                    title, *content = section.split('\n', 1)
                    content = content[0] if content else ""
                    
                    # Section title
                    pdf.set_font("Arial", style='B')
                    pdf.multi_cell(0, 10, txt=clean_text(title.strip()))
                    pdf.set_font("Arial")
                    
                    # Section content
                    for line in content.strip().split('\n'):
                        line = line.strip()
                        if line.startswith('|'):  # Skip markdown tables
                            continue
                        if line.startswith(('- ', '* ', '• ')):
                            line = "• " + line[2:].lstrip()
                        if line and not line.startswith('#'):  # Skip headers
                            pdf.multi_cell(0, 10, txt=clean_text(line))
                    
                    pdf.ln(5)
                
                # Generate PDF file
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                    pdf_filename = tmp.name
                    pdf.output(pdf_filename)
                
                # Download button
                with open(pdf_filename, "rb") as f:
                    st.download_button(
                        label="📄 Download Care Guide (PDF)",
                        data=f,
                        file_name=f"{selected_plant.split('(')[0].strip().replace(' ', '_')}_Care_Guide.pdf",
                        mime="application/pdf"
                    )
                
                # Clean up
                try:
                    os.unlink(pdf_filename)
                except:
                    pass

with tab5:
    st.header("🧠 Plant Knowledge Quiz")
    st.markdown("Test your gardening knowledge with our interactive quiz!")
    
    # Initialize session state for quiz
    if 'quiz_started' not in st.session_state:
        st.session_state.quiz_started = False
    if 'quiz_questions' not in st.session_state:
        st.session_state.quiz_questions = []
    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    
    # Large question bank (50+ questions)
    full_question_bank = [
        {
            "question": "Which of these plants is best suited for winter season?",
            "options": ["Tomato", "Chili", "Tulsi", "Aloe Vera"],
            "answer": "Tomato",
            "image": "tomato.jpeg",
            "explanation": "Tomatoes thrive in winter! They need cooler temperatures (15-25°C) to grow well.",
            "difficulty": "Medium"
        },
        # ... (include all your quiz questions from the original code)
    ]
    
    # Quiz setup form (only shown before quiz starts)
    if not st.session_state.quiz_started:
        with st.form("quiz_setup"):
            st.markdown("""
            <div class='card'>
                <h3 style='color: var(--primary-dark);'>Quiz Settings</h3>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                num_questions = st.slider("Number of questions:", 5, 20, 10)
            with col2:
                difficulty = st.multiselect(
                    "Select difficulty levels:",
                    ["Easy", "Medium", "Hard"],
                    ["Easy", "Medium"]
                )
            
            if st.form_submit_button("Start Quiz"):
                # Filter questions by selected difficulty
                filtered_questions = [q for q in full_question_bank if q["difficulty"] in difficulty]
                
                # Select random questions
                st.session_state.quiz_questions = random.sample(
                    filtered_questions,
                    min(num_questions, len(filtered_questions))
                )
                
                st.session_state.quiz_started = True
                st.session_state.quiz_score = 0
                st.session_state.current_question = 0
                st.session_state.quiz_completed = False
                st.session_state.user_answers = {}
                st.rerun()
    
    # Main quiz interface
    if st.session_state.quiz_started and not st.session_state.quiz_completed:
        # Quiz progress header
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div class='card'>
                <h3 style='color: var(--primary-dark);'>Question {st.session_state.current_question + 1} of {len(st.session_state.quiz_questions)}</h3>
                <p>Difficulty: <span class='badge badge-{st.session_state.quiz_questions[st.session_state.current_question]["difficulty"].lower()}'>{st.session_state.quiz_questions[st.session_state.current_question]["difficulty"]}</span></p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class='card' style='text-align: center;'>
                <h3 style='color: var(--primary-dark);'>Score</h3>
                <p style='font-size: 1.5rem; font-weight: bold; color: var(--primary);'>{st.session_state.quiz_score}/{len(st.session_state.quiz_questions)}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Progress bar
        progress = (st.session_state.current_question) / len(st.session_state.quiz_questions)
        st.progress(progress)
        
        # Current question
        current_q = st.session_state.quiz_questions[st.session_state.current_question]
        
        # Question card with optional image
        with st.container():
            st.markdown(f"""
            <div class='card'>
                <h3 style='color: var(--primary-dark);'>{current_q['question']}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Try to display image if available
            try:
                image_path = os.path.join("images", current_q.get("image", ""))
                if os.path.exists(image_path):
                    st.image(image_path, width=300, caption="Can you guess?")
            except:
                pass
        
        # Answer options as buttons for better interaction
        user_answer = st.radio(
            "Select your answer:",
            current_q['options'],
            key=f"q{st.session_state.current_question}",
            index=None
        )
        
        # Submit button with conditional logic
        if user_answer:
            if st.button("Submit Answer", key=f"submit_{st.session_state.current_question}"):
                # Check answer and provide feedback
                if user_answer == current_q['answer']:
                    st.session_state.quiz_score += 1
                    st.balloons()
                    st.success(f"Correct! 🎉 {current_q['explanation']}")
                else:
                    st.error(f"Oops! The correct answer is: {current_q['answer']}. {current_q['explanation']}")
                
                # Store user answer
                st.session_state.user_answers[st.session_state.current_question] = {
                    "user_answer": user_answer,
                    "correct": user_answer == current_q['answer'],
                    "difficulty": current_q['difficulty']
                }
                
                # Move to next question or complete quiz
                if st.session_state.current_question < len(st.session_state.quiz_questions) - 1:
                    st.session_state.current_question += 1
                    st.rerun()
                else:
                    st.session_state.quiz_completed = True
                    st.rerun()
        else:
            st.warning("Please select an answer before submitting.")
    
    # Quiz completion screen
    elif st.session_state.quiz_completed:
        st.balloons()
        st.markdown("""
        <div class='card'>
            <h2 style='color: var(--primary-dark); text-align: center;'>🎉 Quiz Completed! 🎉</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Calculate final score and badge
        final_score = st.session_state.quiz_score
        total_questions = len(st.session_state.quiz_questions)
        percentage = (final_score / total_questions) * 100
        
        # Determine badge based on score
        if percentage >= 90:
            badge = "🏆 Master Gardener"
            badge_color = "var(--primary)"
            feedback = "Perfect score! Your plant knowledge is truly exceptional."
        elif percentage >= 75:
            badge = "🌿 Expert Gardener"
            badge_color = "var(--success)"
            feedback = "Excellent work! You clearly have a green thumb."
        elif percentage >= 50:
            badge = "🌱 Growing Enthusiast"
            badge_color = "var(--info)"
            feedback = "Good job! Your gardening knowledge is coming along nicely."
        else:
            badge = "🍃 Budding Beginner"
            badge_color = "var(--warning)"
            feedback = "Keep learning! Every expert gardener started somewhere."
        
        # Display results
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='card'>
                <h3 style='color: var(--primary-dark);'>Your Results</h3>
                <div style='text-align: center; margin: 20px 0;'>
                    <div style='font-size: 3rem; font-weight: bold; color: {badge_color};'>{percentage:.0f}%</div>
                    <div style='font-size: 1.5rem; font-weight: bold; color: var(--dark);'>{badge}</div>
                </div>
                <p style='text-align: center;'>{feedback}</p>
                
                <div style='margin-top: 20px;'>
                    <p><b>Score:</b> {final_score}/{total_questions}</p>
                    <p><b>Percentage:</b> {percentage:.0f}%</p>
                </div>
                
                <div style='margin-top: 20px;'>
                    <h4 style='color: var(--primary-dark);'>📊 Performance by Difficulty</h4>
            """, unsafe_allow_html=True)
            
            # Detailed performance by difficulty
            difficulty_stats = {
                "Easy": {"correct": 0, "total": 0},
                "Medium": {"correct": 0, "total": 0},
                "Hard": {"correct": 0, "total": 0}
            }
            
            for i, ans in st.session_state.user_answers.items():
                diff = ans['difficulty']
                difficulty_stats[diff]["total"] += 1
                if ans['correct']:
                    difficulty_stats[diff]["correct"] += 1
            
            for diff, stats in difficulty_stats.items():
                if stats["total"] > 0:
                    st.markdown(f"- **{diff}:** {stats['correct']}/{stats['total']} ({stats['correct']/stats['total']*100:.0f}%)")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            # Score visualization
            st.plotly_chart(
                px.pie(
                    names=["Correct", "Incorrect"],
                    values=[final_score, total_questions - final_score],
                    color=["Correct", "Incorrect"],
                    color_discrete_map={"Correct": "#2e8b57", "Incorrect": "#e9ecef"},
                    hole=0.4,
                    width=300,
                    height=300
                ).update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0)),
                use_container_width=True
            )
            
            # Difficulty distribution
            diff_counts = {
                "Easy": sum(1 for q in st.session_state.quiz_questions if q["difficulty"] == "Easy"),
                "Medium": sum(1 for q in st.session_state.quiz_questions if q["difficulty"] == "Medium"),
                "Hard": sum(1 for q in st.session_state.quiz_questions if q["difficulty"] == "Hard")
            }
            
            st.plotly_chart(
                px.bar(
                    x=list(diff_counts.keys()),
                    y=list(diff_counts.values()),
                    color=list(diff_counts.keys()),
                    color_discrete_map={
                        "Easy": "#d4edda",
                        "Medium": "#fff3cd",
                        "Hard": "#f8d7da"
                    },
                    labels={"x": "Difficulty", "y": "Count"},
                    width=300,
                    height=300
                ).update_layout(showlegend=False, margin=dict(t=0, b=0, l=0, r=0)),
                use_container_width=True
            )
        
        # Review answers section
        st.markdown("""
        <div class='card'>
            <h3 style='color: var(--primary-dark);'>📝 Review Your Answers</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for i, q in enumerate(st.session_state.quiz_questions):
            user_ans = st.session_state.user_answers.get(i, {})
            with st.expander(f"Question {i+1} ({q['difficulty']}): {q['question']}"):
                st.markdown(f"**Your answer:** {user_ans.get('user_answer', 'Not answered')}")
                st.markdown(f"**Correct answer:** {q['answer']}")
                st.markdown(f"**Explanation:** {q['explanation']}")
                
                # Show emoji based on correctness
                if user_ans.get('correct', False):
                    st.markdown("✅ **You got it right!**")
                else:
                    st.markdown("❌ **Better luck next time!**")
        
        # Quiz actions
        col1, col2 = st.columns(2)
        with col1:
            if st.button("♻️ Take New Quiz"):
                st.session_state.quiz_started = False
                st.rerun()
        with col2:
            if st.button("🏠 Return to Home"):
                st.session_state.quiz_started = False
                st.session_state.quiz_completed = False
                st.rerun()

with tab6:
    st.header("⛅ Weather Information")
    st.markdown("Get current weather data and gardening recommendations for your location.")
    
    with st.container():
        st.markdown("""
        <div class='card'>
            <h3 style='color: var(--primary-dark);'>Weather for Gardeners</h3>
            <p>Enter your location to get weather-based gardening advice.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Use a predefined API key (replace with your actual key)
    API_KEY = "ec8ecd486662eb30efb5e29afc7851c5"  # Replace with your actual OpenWeatherMap API key
    city = st.text_input("Enter your city name:")
    
    if city:
        try:
            # Get current weather
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = f"{base_url}appid={API_KEY}&q={city}&units=metric"
            response = requests.get(complete_url)
            weather_data = response.json()
            
            if weather_data["cod"] != "404":
                main_data = weather_data["main"]
                current_temp = main_data["temp"]
                current_humidity = main_data["humidity"]
                weather_desc = weather_data["weather"][0]["description"]
                
                # Get additional useful data
                wind_speed = weather_data["wind"]["speed"]
                cloudiness = weather_data["clouds"]["all"]
                sunrise = datetime.fromtimestamp(weather_data["sys"]["sunrise"]).strftime('%H:%M')
                sunset = datetime.fromtimestamp(weather_data["sys"]["sunset"]).strftime('%H:%M')
                
                # Display weather metrics
                st.markdown("""
                <div class='card'>
                    <h3 style='color: var(--primary-dark);'>Current Weather Conditions</h3>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class='card' style='text-align: center;'>
                        <div style='font-size: 2rem; font-weight: bold; color: var(--primary);'>{current_temp}°C</div>
                        <div>Temperature</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class='card' style='text-align: center;'>
                        <div style='font-size: 2rem; font-weight: bold; color: var(--primary);'>{current_humidity}%</div>
                        <div>Humidity</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class='card' style='text-align: center;'>
                        <div style='font-size: 2rem; font-weight: bold; color: var(--primary);'>{weather_desc.title()}</div>
                        <div>Conditions</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class='card' style='text-align: center;'>
                        <div style='font-size: 2rem; font-weight: bold; color: var(--primary);'>{wind_speed} m/s</div>
                        <div>Wind Speed</div>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class='card' style='text-align: center;'>
                        <div style='font-size: 2rem; font-weight: bold; color: var(--primary);'>{sunrise}</div>
                        <div>Sunrise</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class='card' style='text-align: center;'>
                        <div style='font-size: 2rem; font-weight: bold; color: var(--primary);'>{sunset}</div>
                        <div>Sunset</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Plant-specific recommendations based on weather
                st.markdown("""
                <div class='card'>
                    <h3 style='color: var(--primary-dark);'>🌱 Gardening Recommendations</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if current_temp < 10:
                    st.warning("""
                    <div class='card' style='background-color: #fff3cd; border-left: 4px solid #ffc107;'>
                        <h4>❄️ Cold Weather Alert</h4>
                        <p>Too cold for most plants. Protect sensitive plants from frost with covers or bring them indoors.</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif current_temp > 35:
                    st.warning("""
                    <div class='card' style='background-color: #f8d7da; border-left: 4px solid #dc3545;'>
                        <h4>🔥 Heat Wave Alert</h4>
                        <p>Extreme heat! Water plants early morning and provide shade if possible. Consider mulching to retain soil moisture.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if current_humidity > 80:
                    st.info("""
                    <div class='card' style='background-color: #d1e7dd; border-left: 4px solid #198754;'>
                        <h4>💧 High Humidity</h4>
                        <p>Reduce watering frequency to prevent fungal diseases. Ensure good air circulation around plants.</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif current_humidity < 30:
                    st.info("""
                    <div class='card' style='background-color: #cfe2ff; border-left: 4px solid #0d6efd;'>
                        <h4>🏜️ Low Humidity</h4>
                        <p>Consider misting plants or using a humidity tray. Water more frequently as soil will dry out faster.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                if "rain" in weather_desc.lower():
                    st.info("""
                    <div class='card' style='background-color: #cfe2ff; border-left: 4px solid #0d6efd;'>
                        <h4>☔ Rain Expected</h4>
                        <p>You may skip watering today. Check soil moisture before additional watering.</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif "clear" in weather_desc.lower():
                    st.info("""
                    <div class='card' style='background-color: #fff3cd; border-left: 4px solid #ffc107;'>
                        <h4>☀️ Sunny Day</h4>
                        <p>Check if plants need extra water. Some may need afternoon shade to prevent scorching.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Frost warning
                if current_temp < 5:
                    st.error("""
                    <div class='card' style='background-color: #f8d7da; border-left: 4px solid #dc3545;'>
                        <h4>⚠️ Frost Warning!</h4>
                        <p>Cover sensitive plants overnight with frost cloth or bring containers indoors.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Watering time recommendation
                current_hour = datetime.now().hour
                if 6 <= current_hour <= 9:
                    st.success("""
                    <div class='card' style='background-color: #d1e7dd; border-left: 4px solid #198754;'>
                        <h4>🌅 Perfect Watering Time</h4>
                        <p>Now is the ideal time for morning watering! Plants will have all day to absorb moisture.</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif 17 <= current_hour <= 19:
                    st.success("""
                    <div class='card' style='background-color: #d1e7dd; border-left: 4px solid #198754;'>
                        <h4>🌇 Good Watering Time</h4>
                        <p>Evening watering is recommended, especially in hot weather.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 5-day forecast
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
                forecast_response = requests.get(forecast_url)
                forecast_data = forecast_response.json()
                
                if forecast_data.get("list"):
                    st.markdown("""
                    <div class='card'>
                        <h3 style='color: var(--primary-dark);'>5-Day Forecast</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Process forecast data
                    forecast_days = {}
                    for item in forecast_data["list"]:
                        date = datetime.fromtimestamp(item["dt"]).strftime('%Y-%m-%d')
                        if date not in forecast_days:
                            forecast_days[date] = {
                                "temps": [],
                                "humidity": [],
                                "conditions": [],
                                "date": date
                            }
                        forecast_days[date]["temps"].append(item["main"]["temp"])
                        forecast_days[date]["humidity"].append(item["main"]["humidity"])
                        forecast_days[date]["conditions"].append(item["weather"][0]["description"])
                    
                    # Display forecast cards
                    cols = st.columns(5)
                    for i, (date, data) in enumerate(list(forecast_days.items())[:5]):
                        avg_temp = sum(data["temps"]) / len(data["temps"])
                        common_condition = max(set(data["conditions"]), key=data["conditions"].count)
                        
                        day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%a')
                        
                        with cols[i]:
                            st.markdown(f"""
                            <div class='card' style='text-align: center;'>
                                <div style='font-weight: bold;'>{day_name}</div>
                                <div style='font-size: 0.8rem; color: var(--gray);'>{date.split('-')[2]}/{date.split('-')[1]}</div>
                                <div style='font-size: 1.2rem; font-weight: bold; margin: 10px 0;'>{avg_temp:.1f}°C</div>
                                <div style='font-size: 0.9rem;'>{common_condition.title()}</div>
                            </div>
                            """, unsafe_allow_html=True)
                
            else:
                st.error("City not found. Please try another location.")
                
        except Exception as e:
            st.error(f"Could not fetch weather data. Error: {str(e)}")

with tab7:
    st.header("💬 Feedback & Support")
    st.markdown("We'd love to hear your feedback to improve Rooted!")
    
    with st.container():
        st.markdown("""
        <div class='card'>
            <h3 style='color: var(--primary-dark);'>Share Your Thoughts</h3>
            <p>Your feedback helps us make Rooted better for all gardeners.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.form("feedback_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Your Name:")
            email = st.text_input("Email (optional):")
        with col2:
            rating = st.slider("How would you rate Rooted?", 1, 5, 3)
            contact_back = st.checkbox("I'd like to be contacted about my feedback")
        
        feedback = st.text_area("Your Feedback:")
        suggestions = st.text_area("Suggestions for improvement:")
        
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            st.success("""
            <div class='card' style='background-color: #d1e7dd; border-left: 4px solid #198754;'>
                <h4>Thank you for your feedback!</h4>
                <p>We appreciate your time and will use your input to improve Rooted.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # In a real app, you would store this data in a database
            st.write(f"Received feedback from {name} (Rating: {rating}/5)")

# Footer
st.markdown("""
<div class='footer'>
    <p>🌿 Rooted - Your Plant Care Buddy | Made with ❤️ for green thumbs everywhere</p>
    <p>© 2023 Rooted App. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)