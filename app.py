import streamlit as st
from datetime import datetime
import requests
import json
import pandas as pd
import os
from PIL import Image

# Sample plant data
plants = [
    {
                "name": "Tulsi (तुळस / तुलसी)",
                "image": "tulsi.jpeg",
                "season": "Summer",
                "care": "Water daily, keep in sunlight.",
                "days_to_grow": 60,
                "water_ltr": 0.25
            },
            {
        "name": "Aloe Vera (कोरफड / घृतकुमारी)",
        "image": "Aloe vera.jpeg",
        "season": "All Seasons",
        "care": "Needs bright light and occasional watering.",
        "days_to_grow": 90,
        "water_ltr": 0.15
            },
    {
        "name": "Marigold (झेंडू / गेंदा)",
        "image": "marigold.jpeg",
        "season": "Winter",
        "care": "Water regularly and keep in sunlight.",
        "days_to_grow": 70,
        "water_ltr": 0.3
    },
    {
        "name": "Spinach (पालक / पालक)",
        "image": "spinach.jpeg",
        "season": "Winter",
        "care": "Water every 2 days, partial sunlight.",
        "days_to_grow": 40,
        "water_ltr": 0.2
    },
    {
        "name": "Money Plant (मनी प्लांट / मनी प्लांट)",
        "image": "money_plant.jpeg",
        "season": "All Seasons",
        "care": "Grows in water or soil, indirect sunlight.",
        "days_to_grow": 30,
        "water_ltr": 0.1
    },
    {
        "name": "Neem (कडुनिंब / नीम)",
        "image": "neem.jpeg",
        "season": "Summer",
        "care": "Needs full sun and well-drained soil.",
        "days_to_grow": 100,
        "water_ltr": 0.3
    },
    {
        "name": "Lemongrass (गवती चहा / लेमनग्रास)",
        "image": "Lemongrass.jpeg",
        "season": "Monsoon",
        "care": "Water regularly, grows fast.",
        "days_to_grow": 75,
        "water_ltr": 0.2
    },
    {
        "name": "Coriander (धणे / धनिया)",
        "image": "Coriander.jpg",
        "season": "Winter",
        "care": "Keep soil moist and well-drained.",
        "days_to_grow": 40,
        "water_ltr": 0.15
    },
    {
        "name": "Mint (पुदिना / पुदीना)",
        "image": "mint.jpeg",
        "season": "Winter",
        "care": "Partial sunlight, water frequently.",
        "days_to_grow": 50,
        "water_ltr": 0.2
    },
    {
        "name": "Curry Leaves (कढीपत्ता / करी पत्ता)",
        "image": "curry leaves.jpeg",
        "season": "Summer",
        "care": "Full sun, moderate watering.",
        "days_to_grow": 80,
        "water_ltr": 0.25
    },
    {
        "name": "Basil (साबा / तुलसी विदेशी)",
        "image": "basil.jpeg",
        "season": "Summer",
        "care": "Water regularly, needs warmth.",
        "days_to_grow": 60,
        "water_ltr": 0.2
    },
    {
        "name": "Tomato (टोमॅटो / टमाटर)",
        "image": "tomato.jpeg",
        "season": "Winter",
        "care": "Full sunlight, daily watering.",
        "days_to_grow": 80,
        "water_ltr": 0.4
    },
    {
        "name": "Chili (मिरची / मिर्च)",
        "image": "chili.jpeg",
        "season": "Summer",
        "care": "Warm climate, daily watering.",
        "days_to_grow": 90,
        "water_ltr": 0.3
    },
    {
        "name": "Brinjal (वांगे / बैंगन)",
        "image": "brinjal.jpeg",
        "season": "Winter",
        "care": "Needs warmth and rich soil.",
        "days_to_grow": 85,
        "water_ltr": 0.4
    },
    {
        "name": "Fenugreek (मेथी / मेथी)",
        "image": "Fenugreek.jpeg",
        "season": "Winter",
        "care": "Moist soil, grows quickly.",
        "days_to_grow": 30,
        "water_ltr": 0.2
    },
    {
        "name": "Peas (हरभरा / मटर)",
        "image": "peas.jpeg",
        "season": "Winter",
        "care": "Cool weather, daily watering.",
        "days_to_grow": 70,
        "water_ltr": 0.35
    },
    {
        "name": "Lady Finger (भेंडी / भिंडी)",
        "image": "lady finger.jpeg",
        "season": "Summer",
        "care": "Water regularly, needs warmth.",
        "days_to_grow": 60,
        "water_ltr": 0.3
    },
    {
        "name": "Bitter Gourd (कारले / करेला)",
        "image": "Bitter Gourd.jpeg",
        "season": "Monsoon",
        "care": "Trellis support, daily watering.",
        "days_to_grow": 95,
        "water_ltr": 0.4
    },
    {
        "name": "Cabbage (कोबी / पत्ता गोभी)",
        "image": "Cabbage.jpeg",
        "season": "Winter",
        "care": "Cool climate, water every 2 days.",
        "days_to_grow": 90,
        "water_ltr": 0.3
    },
            
            {
                "name": "Bottle Gourd (दुधी / लौकी)",
                "image": "Bottle Gourd.jpeg",
                "season": "Monsoon",
                "care": "Trellis required, plenty of water.",
                "days_to_grow": 80,
                "water_ltr": 0.45
            },
            {
                "name" : "Rose (गुलाब / गुलाब)",
                "image" : "rose.jpeg",
                "season" : "Winter",
                "care" : "Water every 2 days, full sunlight.",
                "days_to_grow" : 60,
                "water_ltr" : 0.25
            },
            {
                "name" : "Sunflower (सूर्यमुखी / सूरजमुखी)",
                "image" : "sunflower.jpeg",
                "season" : "Summer",
                "care" : "Water weekly, full sunlight.",
                "days_to_grow" : 70,
                "water_ltr" : 0.5
            },
            {
                "name" : "lily (कमल / कमल)",
                "image" : "lily.jpeg",
                "season" : "Summer",
                "care" : "Water daily, partial sunlight.",
                "days_to_grow" : 50,
                "water_ltr" : 0.2

            },
            {
                "name" : "Hibiscus (जास्वंद / जास्वंद)",
                "image" : "hibiscus.jpeg",
                "season" : "Summer",
                "care" : "Water every 3 days, full sunlight.",
                "days_to_grow" : 60,
                "water_ltr" : 0.3
            }
]

# Page Setup
#st.set_page_config(page_title="Rooted - Plant Care Buddy", layout="wide",page_icon="🌿")
st.set_page_config(
    page_title="Rooted - Plant Care Buddy",
    page_icon="favicon.ico",  # Can also use "🌿" emoji
    layout="wide"
)
st.title("🌿 Rooted - Your Plant Care Buddy")
st.markdown("Grow green, stay rooted! 🌱")


 

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

# Add this CSS styling right after your page setup (after st.set_page_config)
st.markdown("""
    <style>
    /* Main menu (tabs) styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 10px 20px;
        background-color: white;
        border-radius: 10px 10px 0px 0px;
        border: 1px solid #e0e0e0;
        color: black;
        font-weight: bold;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: #f5f5f5;
        color: black;
    }

    .stTabs [aria-selected="true"] {
        background-color: #f0f0f0;
        color: #2e8b57;  /* Green color for selected tab */
        border-bottom: 3px solid #2e8b57;
    }
    </style>
""", unsafe_allow_html=True)





# Create tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Home", "Plant Details", "Recommendations", "Care Guide Generator", "Plant Quiz" ,"Weather", "Feedback"])


# Image directory selection



with tab1:
    st.header("Welcome to Rooted!")
    st.image("https://images.unsplash.com/photo-1501004318641-b39e6451bec6?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", width=800)
    st.markdown("""
    ### Your Personal Plant Care Assistant
    
    Rooted helps you grow and care for your plants with:
    - 🌱 Detailed plant care information
    - ⛅ Weather-based recommendations
    - 📝 Personalized care guides
    - ❓ Fun quizzes to test your knowledge
    """)

with tab2:
    st.header("Plant Care Information")
    
    # Select a plant
    plant_names = [plant["name"] for plant in plants]
    selected = st.selectbox("Select a plant to learn how to care for it:", plant_names)
    
    # Show info for selected plant
    for plant in plants:
        if plant["name"] == selected:
            col1, col2 = st.columns([1, 2])
            with col1:
                # Try to load local image from images folder
                try:
                    image_path = os.path.join("images", plant["image"])
                    st.image(image_path, width=400, caption=plant["name"])
                except Exception as e:
                    st.error(f"Could not load plant image: {str(e)}")
                    st.warning(f"Image path attempted: {image_path}")
            
            with col2:
                st.subheader(f"🌸 {plant['name']}")
                
                # Extract base name (without Hindi text) for matching
                base_name = plant['name'].split('(')[0].strip()
                
                # Try to get additional data from CSV
                csv_data = None
                if plant_df is not None:
                    try:
                        # First try exact match with base name
                        mask = plant_df['Plant Name'].str.strip().str.lower() == base_name.lower()
                        if not mask.any():
                            # If no exact match, try partial match
                            mask = plant_df['Plant Name'].str.lower().str.contains(base_name.lower())
                        
                        csv_data = plant_df[mask]
                        if not csv_data.empty:
                            csv_data = csv_data.iloc[0]  # Get the first matching row
                            plant_info = csv_data.to_dict()
                        else:
                            plant_info = None
                    except Exception as e:
                        st.error(f"Error loading plant data: {str(e)}")
                        plant_info = None
                
                # Display plant information
                if plant_info:
                    # Create two columns for better layout
                    col_info1, col_info2 = st.columns(2)
                    
                    with col_info1:
                        st.markdown("### 🌱 Basic Information")
                        st.markdown(f"**Type:** {plant_info.get('Type', 'N/A')}")
                        st.markdown(f"**Best Season:** {plant_info.get('Best Season', plant['season'])}")
                        st.markdown(f"**Growth Time:** {plant_info.get('Growth Time', f"{plant['days_to_grow']} days")}")
                        st.markdown(f"**Plant Height:** {plant_info.get('Plant Height', 'N/A')}")
                        st.markdown(f"**Temperature Range:** {plant_info.get('Temperature Range', 'N/A')}")
                        
                    with col_info2:
                        st.markdown("### 💧 Care Guide")
                        st.markdown(f"**Sunlight:** {plant_info.get('Sunlight', 'N/A')}")
                        st.markdown(f"**Watering:** {plant_info.get('Watering', f"{plant['water_ltr']} L")}")
                        st.markdown(f"**Soil Type:** {plant_info.get('Soil Type', 'N/A')}")
                        st.markdown(f"**Fertilizer:** {plant_info.get('Fertilizer Recommendation', 'N/A')}")
                
                    st.markdown("### 🐛 Pests & Problems")
                    st.markdown(f"**Common Pests/Diseases:** {plant_info.get('Pests/Diseases', 'N/A')}")
                    
                    st.markdown("### 🌿 Additional Info")
                    st.markdown(f"**Common Uses:** {plant_info.get('Common Uses', 'N/A')}")
                    st.markdown(f"**Companion Plants:** {plant_info.get('Companion Plants', 'N/A')}")
                else:
                    # Fall back to basic sample data
                    st.markdown("### 🌱 Basic Information")
                    st.markdown(f"**Best Season to Grow:** {plant['season']}")
                    st.markdown(f"**Days to Grow:** {plant['days_to_grow']} days")
                    
                    st.markdown("### 💧 Care Guide")
                    st.markdown(f"**Care Tips:** {plant['care']}")
                    st.markdown(f"**Watering Requirement:** {plant['water_ltr']} L")
                
                # Watering notification
                current_hour = datetime.now().hour
                if 6 <= current_hour <= 9 or 17 <= current_hour <= 19:
                    water_rec = plant_info.get('Watering', f"{plant['water_ltr']} L") if plant_info else f"{plant['water_ltr']} L"
                    st.info(f"🔔 It's time to water your plant! Watering recommendation: {water_rec}")
                else:
                    st.warning("💧 Avoid watering now. Best time: early morning or evening.")

with tab3:                                                              
    st.header("Plant Recommendations")
    season = st.selectbox("Select current season:", ["Summer", "Winter", "Monsoon", "All Seasons"])
    space = st.selectbox("Available space:", ["Small pots", "Medium pots", "Large pots", "Garden"])
    experience = st.selectbox("Your experience level:", ["Beginner", "Intermediate", "Expert"])
    
    if st.button("Get Recommendations"):
        filtered_plants = [p for p in plants if p["season"] == season or p["season"] == "All Seasons"]
        
        # Simple filtering logic (can be enhanced)
        if space == "Small pots":
            filtered_plants = [p for p in filtered_plants if p["water_ltr"] <= 0.2]
        elif space == "Medium pots":
            filtered_plants = [p for p in filtered_plants if p["water_ltr"] <= 0.3]
        
        if experience == "Beginner":
            filtered_plants = [p for p in filtered_plants if p["days_to_grow"] <= 60]
        elif experience == "Intermediate":
            filtered_plants = [p for p in filtered_plants if p["days_to_grow"] <= 90]
        
        if filtered_plants:
            st.success("Here are plants that match your criteria:")
            for plant in filtered_plants[:5]:  # Show top 5 results
                with st.expander(plant["name"]):
                    #st.image(plant["image"], width=400)
                    st.markdown(f"**Season:** {plant['season']}")
                    st.markdown(f"**Care Level:** {'Easy' if plant['days_to_grow'] <= 60 else 'Moderate' if plant['days_to_grow'] <= 90 else 'Advanced'}")
        else:
            st.warning("No plants match all your criteria. Try adjusting your selections.")

with tab4:
    st.header("🌱 Personalized Care Guide Generator")
    
    selected_plant = st.selectbox("Select your plant:", [p["name"] for p in plants])
    plant_age = st.slider("Plant age (days):", 0, 365, 30)
    location = st.selectbox("Plant location:", ["Indoor", "Outdoor", "Balcony", "Terrace", "Garden"])
    experience_level = st.selectbox("Your experience level:", ["Beginner", "Intermediate", "Advanced"])
    
    if st.button("Generate Care Guide"):
        # Find the selected plant
        plant = next(p for p in plants if p["name"] == selected_plant)
        
        # Try to get additional data from CSV
        csv_data = None
        if plant_df is not None:
            base_name = selected_plant.split('(')[0].strip()
            mask = plant_df['Plant Name'].str.contains(base_name, case=False)
            csv_data = plant_df[mask].iloc[0].to_dict() if not plant_df[mask].empty else None
        
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
        # {selected_plant} Care Guide  
        ## 🌿 Basic Information  
        - **Type:** {csv_data.get('Type', 'N/A') if csv_data else 'N/A'}  
        - **Best Season:** {plant['season']}  
        - **Growth Time:** {plant['days_to_grow']} days  
        - **Current Stage:** {stage} ({plant_age} days old)  
        
        ## ☀️ Light Requirements  
        - **Ideal Sunlight:** {csv_data.get('Sunlight', 'Full Sun') if csv_data else 'Full Sun'}  
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
        - **Soil Type:** {csv_data.get('Soil Type', 'Well-draining potting mix') if csv_data else 'Well-draining potting mix'}  
        - **Fertilizer:** {csv_data.get('Fertilizer Recommendation', 'Balanced NPK (10-10-10)') if csv_data else 'Balanced NPK (10-10-10)'}  
        - **Fertilizing Schedule:**  
          • {stage}: {'Every 2 weeks' if stage == 'Vegetative Growth' else 'Monthly' if stage == 'Mature' else 'Not needed yet'}  
        - **Soil pH:** 6.0-7.0 (most plants prefer slightly acidic)  
        
        ## 🐛 Pest & Disease Management  
        - **Common Issues:** {csv_data.get('Pests/Diseases', 'Aphids, Spider mites') if csv_data else 'Aphids, Spider mites'}  
        - **Prevention:**  
          • Neem oil spray weekly  
          • Proper air circulation  
          • Avoid overwatering  
        - **Organic Treatment Recipe:**  
          1. Mix 1 tsp neem oil + 1/2 tsp liquid soap in 1L water  
          2. Spray every 7-10 days  
        
        ## 📅 Monthly Care Calendar  
        | Month        | Key Tasks                 |
        |--------------|---------------------------|
        | 1-{plant['days_to_grow']//3} | Watering, Gentle light |
        | {plant['days_to_grow']//3}-{plant['days_to_grow']*2//3} | Fertilizing, Pruning |
        | {plant['days_to_grow']*2//3}-{plant['days_to_grow']} | Harvesting, Disease watch |
        
        ## 💡 Expert Tips for {experience_level}  
        {stage_tips}  
        - **Companion Plants:** {csv_data.get('Companion Plants', 'N/A') if csv_data else 'N/A'}  
        - **Avoid Planting With:** {['Onions', 'Walnut trees', 'Fennel'][hash(selected_plant)%3]}  
        - **Harvesting Tip:** {'Morning harvest has best flavor' if 'Vegetable' in csv_data.get('Type', '') else ''}  
        """
        
        # Display in app
        st.markdown(guide)
        
        # PDF Generation
        from fpdf import FPDF
        import requests
        import os
        import unicodedata
        import tempfile
        
        def clean_text(text):
            """Remove problematic characters while preserving structure"""
            return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
        
        # Initialize PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)  # Default font
        
        # Try to use DejaVu font if available
        dejavu_path = "DejaVuSansCondensed.ttf"
        if not os.path.exists(dejavu_path):
            try:
                font_url = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSansCondensed.ttf"
                response = requests.get(font_url, timeout=10)
                with open(dejavu_path, "wb") as f:
                    f.write(response.content)
            except:
                st.warning("Using Arial font (limited Unicode support)")
        
        if os.path.exists(dejavu_path):
            try:
                pdf.add_font("DejaVu", "", dejavu_path, uni=True)
                pdf.set_font("DejaVu", size=12)
            except:
                pass
        
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
            pdf.set_font("Arial",style='B')
            pdf.multi_cell(0, 10, txt=clean_text(title.strip()))
            pdf.set_font("Arial",style='B')
            
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
            if os.path.exists(dejavu_path):
                os.unlink(dejavu_path)
        except:
            pass

        
with tab5:
    st.header("🌱 Plant Knowledge Quiz")
    st.markdown("Test your gardening knowledge with new questions each time! 🔄")
    
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
        {
            "question": "How often should you water a Money Plant?",
            "options": ["Daily", "Weekly", "Only when soil is dry", "Twice a day"],
            "answer": "Only when soil is dry",
            "image": "money_plant.jpeg",
            "explanation": "Money Plants prefer their soil to dry out between waterings. Overwatering can cause root rot!",
            "difficulty": "Easy"
        },
        {
            "question": "Which plant is known as the 'Queen of Herbs' in India?",
            "options": ["Marigold", "Neem", "Tulsi", "Mint"],
            "answer": "Tulsi",
            "image": "tulsi.jpeg",
            "explanation": "Tulsi (Holy Basil) is revered in India for its medicinal and spiritual significance.",
            "difficulty": "Easy"
        },
        {
            "question": "What's the best time of day to water your plants?",
            "options": ["Noon", "Early morning", "Midnight", "Any time"],
            "answer": "Early morning",
            "image": "watering.jpeg",
            "explanation": "Morning watering allows plants to absorb water before the heat of the day and prevents fungal growth.",
            "difficulty": "Easy"
        },
        {
            "question": "Which of these helps improve soil fertility?",
            "options": ["Chemical fertilizers", "Compost", "Both", "Neither"],
            "answer": "Compost",
            "image": "compost.jpeg",
            "explanation": "Compost enriches soil naturally with organic matter and beneficial microorganisms!",
            "difficulty": "Medium"
        },
        {
            "question": "What is the ideal pH range for most garden plants?",
            "options": ["3.0-4.5", "5.5-7.0", "7.5-9.0", "It doesn't matter"],
            "answer": "5.5-7.0",
            "image": "ph_test.jpeg",
            "explanation": "Most plants prefer slightly acidic to neutral soil (pH 5.5-7.0). Some plants have specific requirements.",
            "difficulty": "Hard"
        },
        {
            "question": "Which plant is known for repelling mosquitoes?",
            "options": ["Basil", "Lemongrass", "Brinjal", "Cabbage"],
            "answer": "Lemongrass",
            "image": "Lemongrass.jpeg",
            "explanation": "Lemongrass contains citronella, a natural mosquito repellent. Plant it near seating areas!",
            "difficulty": "Medium"
        },
        {
        "question": "Which plant is known as 'Nature's Band-Aid' for its healing properties?",
        "options": ["Aloe Vera", "Tulsi", "Neem", "Mint"],
        "answer": "Aloe Vera",
        "explanation": "Aloe Vera gel is used to soothe burns and skin irritations.",
        "difficulty": "Easy"
    },
    {
        "question": "What is the best way to check if a plant needs water?",
        "options": ["Check the weather forecast", "Feel the soil moisture", "Look at leaf color", "Wait until it wilts"],
        "answer": "Feel the soil moisture",
        "explanation": "Stick your finger 1-2 inches into the soil - if dry, it needs water.",
        "difficulty": "Easy"
    },
    {
        "question": "Which of these plants can grow in water without soil?",
        "options": ["Money Plant", "Tomato", "Marigold", "Sunflower"],
        "answer": "Money Plant",
        "explanation": "Money Plants (Pothos) can grow hydroponically in just water.",
        "difficulty": "Easy"
    },
    {
        "question": "What does 'NPK' stand for in fertilizers?",
        "options": ["Nitrogen, Phosphorus, Potassium", "Natural Plant Knowledge", "New Plant Kind", "Nutrient Power Kit"],
        "answer": "Nitrogen, Phosphorus, Potassium",
        "explanation": "These are the three primary nutrients plants need.",
        "difficulty": "Medium"
    },
    {
        "question": "Which plant's leaves are traditionally used to make herbal tea in India?",
        "options": ["Lemongrass", "Tulsi", "Mint", "All of these"],
        "answer": "All of these",
        "explanation": "All three plants are used to make different types of herbal teas.",
        "difficulty": "Easy"
    },
    {
        "question": "What is the purpose of adding pebbles at the bottom of plant pots?",
        "options": ["Decoration", "Improve drainage", "Prevent insects", "Help roots grow faster"],
        "answer": "Improve drainage",
        "explanation": "Pebbles help prevent waterlogging and root rot.",
        "difficulty": "Easy"
    },
    {
        "question": "Which plant is considered sacred in Hindu culture?",
        "options": ["Tulsi", "Neem", "Banyan", "All of these"],
        "answer": "All of these",
        "explanation": "All three plants hold religious significance in Hinduism.",
        "difficulty": "Easy"
    },
    {
        "question": "What is the best natural pesticide among these options?",
        "options": ["Neem oil", "Vinegar", "Salt water", "Baking soda"],
        "answer": "Neem oil",
        "explanation": "Neem oil is effective against many common plant pests.",
        "difficulty": "Medium"
    },
    {
        "question": "Which plant's seeds are used to make the spice 'dhania'?",
        "options": ["Fenugreek", "Coriander", "Mustard", "Cumin"],
        "answer": "Coriander",
        "explanation": "Coriander seeds are dried and used as the spice dhania.",
        "difficulty": "Medium"
    },
    {
        "question": "What is the main benefit of companion planting?",
        "options": ["Looks pretty", "Saves space", "Natural pest control", "Makes harvesting easier"],
        "answer": "Natural pest control",
        "explanation": "Certain plant combinations repel pests or attract beneficial insects.",
        "difficulty": "Medium"
    },
    {
        "question": "Which plant is NOT recommended for indoor growing?",
        "options": ["Snake Plant", "Money Plant", "Sunflower", "Peace Lily"],
        "answer": "Sunflower",
        "explanation": "Sunflowers need full sun and grow too tall for most indoor spaces.",
        "difficulty": "Easy"
    },
    {
        "question": "What is the edible part of a potato plant?",
        "options": ["Root", "Stem", "Leaf", "Flower"],
        "answer": "Stem",
        "explanation": "Potatoes are modified stems called tubers, not roots.",
        "difficulty": "Hard"
    },
    {
        "question": "Which plant is known to repel mosquitoes naturally?",
        "options": ["Citronella", "Marigold", "Basil", "All of these"],
        "answer": "All of these",
        "explanation": "All three plants have mosquito-repelling properties.",
        "difficulty": "Easy"
    },
    {
        "question": "What is vermicompost?",
        "options": ["Compost made with worms", "Liquid fertilizer", "Chemical compost", "Manure compost"],
        "answer": "Compost made with worms",
        "explanation": "Vermicompost uses earthworms to break down organic matter.",
        "difficulty": "Medium"
    },
    {
        "question": "Which plant's leaves are used to make 'pudina chutney'?",
        "options": ["Coriander", "Mint", "Curry Leaves", "Basil"],
        "answer": "Mint",
        "explanation": "Pudina is the Hindi name for mint.",
        "difficulty": "Easy"
    },
    {
        "question": "What causes yellow leaves in plants?",
        "options": ["Overwatering", "Nutrient deficiency", "Pests", "All of these"],
        "answer": "All of these",
        "explanation": "Yellowing can indicate multiple problems needing investigation.",
        "difficulty": "Medium"
    },
    {
        "question": "Which plant grows the fastest from seeds?",
        "options": ["Fenugreek", "Tomato", "Brinjal", "Sunflower"],
        "answer": "Fenugreek",
        "explanation": "Fenugreek (methi) sprouts in 2-3 days and grows quickly.",
        "difficulty": "Easy"
    },
    {
        "question": "What is the white powder sometimes seen on plant leaves?",
        "options": ["Dust", "Powdery mildew", "Natural wax", "Insect eggs"],
        "answer": "Powdery mildew",
        "explanation": "A fungal disease that needs treatment with fungicides.",
        "difficulty": "Medium"
    },
    {
        "question": "Which plant is NOT a member of the mint family?",
        "options": ["Basil", "Tulsi", "Lemongrass", "Oregano"],
        "answer": "Lemongrass",
        "explanation": "Lemongrass belongs to the grass family, not Lamiaceae (mint family).",
        "difficulty": "Hard"
    },
    {
        "question": "What is the purpose of pruning plants?",
        "options": ["Encourage bushier growth", "Remove dead parts", "Improve air circulation", "All of these"],
        "answer": "All of these",
        "explanation": "Pruning serves multiple beneficial purposes for plant health.",
        "difficulty": "Easy"
    },
    {
        "question": "Which plant is known as 'Indian Ginseng'?",
        "options": ["Tulsi", "Ashwagandha", "Giloy", "Aloe Vera"],
        "answer": "Ashwagandha",
        "explanation": "Ashwagandha is called Indian Ginseng for its adaptogenic properties.",
        "difficulty": "Medium"
    },
    {
        "question": "What is the best time to harvest coriander leaves?",
        "options": ["Early morning", "Midday", "Evening", "Night"],
        "answer": "Early morning",
        "explanation": "Leaves contain maximum moisture and freshness in early morning.",
        "difficulty": "Medium"
    },
    {
        "question": "Which plant's flowers are edible?",
        "options": ["Marigold", "Hibiscus", "Rose", "All of these"],
        "answer": "All of these",
        "explanation": "All three flowers are used in various culinary applications.",
        "difficulty": "Easy"
    },
    {
        "question": "What is the main benefit of adding banana peels to plants?",
        "options": ["Potassium supply", "Pest control", "Improve fragrance", "Increase acidity"],
        "answer": "Potassium supply",
        "explanation": "Banana peels decompose to release potassium, important for flowering.",
        "difficulty": "Medium"
    },
    {
        "question": "Which plant is most drought-resistant?",
        "options": ["Aloe Vera", "Ferns", "Mint", "Spinach"],
        "answer": "Aloe Vera",
        "explanation": "Aloe's succulent leaves store water for dry periods.",
        "difficulty": "Easy"
    },
    {
        "question": "What is 'pinching' in gardening?",
        "options": ["Removing flower buds", "Squeezing stems", "Removing growing tips", "Handling seedlings gently"],
        "answer": "Removing growing tips",
        "explanation": "Pinching encourages bushier growth by removing apical dominance.",
        "difficulty": "Hard"
    },
    {
        "question": "Which plant is considered a natural air purifier?",
        "options": ["Snake Plant", "Areca Palm", "Money Plant", "All of these"],
        "answer": "All of these",
        "explanation": "NASA studies show all these plants remove indoor air pollutants.",
        "difficulty": "Easy"
    },
    {
        "question": "What is the white sap that comes from broken money plant stems?",
        "options": ["Toxic latex", "Healing resin", "Excess water", "Plant nutrients"],
        "answer": "Toxic latex",
        "explanation": "Can cause skin irritation - wash hands after handling broken stems.",
        "difficulty": "Medium"
    },
    {
        "question": "Which plant's seeds are used to make the spice 'methi'?",
        "options": ["Fenugreek", "Mustard", "Cumin", "Coriander"],
        "answer": "Fenugreek",
        "explanation": "Methi is the Hindi name for fenugreek seeds.",
        "difficulty": "Easy"
    },
    {
        "question": "What is the purpose of rotating potted plants?",
        "options": ["Even growth", "Prevent disease", "Confuse pests", "Exercise the stems"],
        "answer": "Even growth",
        "explanation": "Ensures all sides get equal light exposure.",
        "difficulty": "Easy"
    },
    {
        "question": "Which plant is NOT grown from seeds?",
        "options": ["Potato", "Tomato", "Sunflower", "Marigold"],
        "answer": "Potato",
        "explanation": "Potatoes are grown from 'seed potatoes' (tubers), not seeds.",
        "difficulty": "Medium"
    },
    {
        "question": "What is the best container material for plants?",
        "options": ["Plastic", "Clay", "Metal", "Depends on the plant"],
        "answer": "Depends on the plant",
        "explanation": "Different materials have pros/cons based on plant needs.",
        "difficulty": "Medium"
    },
    {
        "question": "Which plant can grow from just a single leaf cutting?",
        "options": ["Money Plant", "Rose", "Sunflower", "Neem"],
        "answer": "Money Plant",
        "explanation": "Money Plants easily propagate from leaf/node cuttings.",
        "difficulty": "Easy"
    },
    {
        "question": "What causes tiny holes in plant leaves?",
        "options": ["Insects", "Fungal disease", "Water droplets", "Natural pores"],
        "answer": "Insects",
        "explanation": "Commonly caused by chewing insects like caterpillars or beetles.",
        "difficulty": "Easy"
    },
    {
        "question": "Which plant is most sensitive to overwatering?",
        "options": ["Cactus", "Mint", "Ferns", "Peace Lily"],
        "answer": "Cactus",
        "explanation": "Succulents like cacti easily rot with excess water.",
        "difficulty": "Easy"
    },
    {
        "question": "What is 'hardening off' in gardening?",
        "options": ["Making soil harder", "Toughening seedlings", "Drying herbs", "Pruning heavily"],
        "answer": "Toughening seedlings",
        "explanation": "Gradually acclimating indoor-started plants to outdoor conditions.",
        "difficulty": "Hard"
    },
    {
        "question": "Which plant's leaves close at night?",
        "options": ["Tulsi", "Touch-Me-Not", "Neem", "Aloe Vera"],
        "answer": "Touch-Me-Not",
        "explanation": "Mimosa pudica (Touch-Me-Not) shows nyctinasty (sleep movement).",
        "difficulty": "Medium"
    },
    {
        "question": "What is the black gold of gardening?",
        "options": ["Compost", "Vermicompost", "Manure", "Cocopeat"],
        "answer": "Compost",
        "explanation": "Rich compost is invaluable for plant growth, hence 'black gold'.",
        "difficulty": "Easy"
    },
    {
        "question": "Which plant is most sensitive to cold temperatures?",
        "options": ["Basil", "Spinach", "Peas", "Cabbage"],
        "answer": "Basil",
        "explanation": "Basil is heat-loving and damaged by cold below 10°C.",
        "difficulty": "Medium"
    },
    {
        "question": "What is the purpose of staking plants?",
        "options": ["Support growth", "Mark location", "Prevent animals", "Guide direction"],
        "answer": "Support growth",
        "explanation": "Provides support to prevent bending/breaking of stems.",
        "difficulty": "Easy"
    }
    ]
    
    # Quiz setup form (only shown before quiz starts)
    if not st.session_state.quiz_started:
        with st.form("quiz_setup"):
            st.subheader("Quiz Settings")
            num_questions = st.slider("Number of questions:", 5, 20, 10)
            difficulty = st.multiselect(
                "Select difficulty levels:",
                ["Easy", "Medium", "Hard"],
                ["Easy", "Medium"]
            )
            
            if st.form_submit_button("Start Quiz"):
                # Filter questions by selected difficulty
                filtered_questions = [q for q in full_question_bank if q["difficulty"] in difficulty]
                
                # Select random questions
                import random
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
            st.subheader(f"Question {st.session_state.current_question + 1} of {len(st.session_state.quiz_questions)}")
            st.caption(f"Difficulty: {st.session_state.quiz_questions[st.session_state.current_question]['difficulty']}")
        with col2:
            st.metric("Score", f"{st.session_state.quiz_score}/{len(st.session_state.quiz_questions)}")
        
        # Progress bar
        progress = (st.session_state.current_question) / len(st.session_state.quiz_questions)
        st.progress(progress)
        
        # Current question
        current_q = st.session_state.quiz_questions[st.session_state.current_question]
        
        # Question card with optional image
        with st.container():
            st.markdown(f"""
            <div style='background-color:#f0f8f0; padding:20px; border-radius:10px; margin-bottom:20px;'>
                <h3 style='color:#2e8b57;'>{current_q['question']}</h3>
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
        st.success("### 🎉 Quiz Completed! 🎉")
        
        # Calculate final score and badge
        final_score = st.session_state.quiz_score
        total_questions = len(st.session_state.quiz_questions)
        percentage = (final_score / total_questions) * 100
        
        # Determine badge based on score
        if percentage >= 90:
            badge = "🏆 Master Gardener"
            feedback = "Perfect score! Your plant knowledge is truly exceptional."
        elif percentage >= 75:
            badge = "🌿 Expert Gardener"
            feedback = "Excellent work! You clearly have a green thumb."
        elif percentage >= 50:
            badge = "🌱 Growing Enthusiast"
            feedback = "Good job! Your gardening knowledge is coming along nicely."
        else:
            badge = "🍃 Budding Beginner"
            feedback = "Keep learning! Every expert gardener started somewhere."
        
        # Display results
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style='background-color:#f0f8f0; padding:20px; border-radius:10px;'>
                <h3 style='color:#2e8b57;'>Your Results</h3>
                <p><b>Score:</b> {final_score}/{total_questions}</p>
                <p><b>Percentage:</b> {percentage:.0f}%</p>
                <p><b>Badge Earned:</b> {badge}</p>
                <p>{feedback}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Detailed performance by difficulty
            st.markdown("#### 📊 Performance by Difficulty")
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
        
        with col2:
            # Score visualization
            st.vega_lite_chart({
                "mark": {"type": "arc", "innerRadius": 50},
                "encoding": {
                    "theta": {"field": "value", "type": "quantitative"},
                    "color": {"field": "category", "type": "nominal"}
                },
                "data": {
                    "values": [
                        {"category": "Correct", "value": final_score},
                        {"category": "Incorrect", "value": total_questions - final_score}
                    ]
                },
                "width": 200,
                "height": 200
            })
            
            # Difficulty distribution
            st.markdown("#### ⚖️ Question Difficulty")
            diff_counts = {
                "Easy": sum(1 for q in st.session_state.quiz_questions if q["difficulty"] == "Easy"),
                "Medium": sum(1 for q in st.session_state.quiz_questions if q["difficulty"] == "Medium"),
                "Hard": sum(1 for q in st.session_state.quiz_questions if q["difficulty"] == "Hard")
            }
            st.vega_lite_chart({
                "mark": {"type": "bar", "color": "#2e8b57"},
                "encoding": {
                    "x": {"field": "difficulty", "type": "nominal"},
                    "y": {"field": "count", "type": "quantitative"}
                },
                "data": {
                    "values": [
                        {"difficulty": "Easy", "count": diff_counts["Easy"]},
                        {"difficulty": "Medium", "count": diff_counts["Medium"]},
                        {"difficulty": "Hard", "count": diff_counts["Hard"]}
                    ]
                },
                "width": 200,
                "height": 200
            })
        
        # Review answers section
        st.markdown("### 📝 Review Your Answers")
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
    st.header("Weather Information for Gardeners")
    
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
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Temperature", f"{current_temp}°C")
                    st.metric("Humidity", f"{current_humidity}%")
                with col2:
                    st.metric("Conditions", weather_desc.title())
                    st.metric("Wind Speed", f"{wind_speed} m/s")
                with col3:
                    st.metric("Sunrise", sunrise)
                    st.metric("Sunset", sunset)
                
                # Plant-specific recommendations based on weather
                st.subheader("Gardening Recommendations")
                
                if current_temp < 10:
                    st.warning("❄️ Too cold for most plants. Protect sensitive plants from frost.")
                elif current_temp > 35:
                    st.warning("🔥 Extreme heat! Water plants early morning and provide shade if possible.")
                
                if current_humidity > 80:
                    st.info("💧 High humidity - reduce watering frequency to prevent fungal diseases")
                elif current_humidity < 30:
                    st.info("🏜️ Low humidity - consider misting plants or using a humidity tray")
                
                if "rain" in weather_desc.lower():
                    st.info("☔ Rain expected - you may skip watering today")
                elif "clear" in weather_desc.lower():
                    st.info("☀️ Sunny day - check if plants need extra water")
                
                # Frost warning
                if current_temp < 5:
                    st.error("⚠️ Frost warning! Cover sensitive plants overnight.")
                
                # Watering time recommendation
                current_hour = datetime.now().hour
                if 6 <= current_hour <= 9:
                    st.success("🌅 Perfect time for morning watering!")
                elif 17 <= current_hour <= 19:
                    st.success("🌇 Good time for evening watering!")
                
            else:
                st.error("City not found. Please try another location.")
                
        except Exception as e:
            st.error(f"Could not fetch weather data. Error: {str(e)}")


with tab7:
    st.header("Feedback Form")
    st.markdown("We'd love to hear your feedback to improve Rooted!")
    
    with st.form("feedback_form"):
        name = st.text_input("Your Name:")
        email = st.text_input("Email (optional):")
        rating = st.slider("How would you rate Rooted?", 1, 5, 3)
        feedback = st.text_area("Your Feedback:")
        suggestions = st.text_area("Suggestions for improvement:")
        
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            st.success("Thank you for your feedback! We appreciate your time.")
            # In a real app, you would store this data in a database
            st.write(f"Received feedback from {name} (Rating: {rating}/5)")

st.markdown("---")
st.markdown("💡 *Pro Tip: Use rainwater or filtered water for better results!*")