# full corrected app.py with fertilizer engine & comparison chart
import streamlit as st
import joblib
import pandas as pd
import numpy as np
import datetime
# --- IMPORTS FOR NEW FEATURES ---
from rainfall_predictor_model import RainfallPredictor

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Agro-Advisor: Smart Crop Recommendation",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 2. CUSTOM CSS FOR STYLING ---
st.markdown("""
<style>
    .main { background-color: #F0FFF0; padding: 2rem; }
    .stButton>button {
        background-color: #2E8B57; color: white; border: none; padding: 15px 32px;
        text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer;
        border-radius: 12px; width: 100%; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition-duration: 0.4s;
    }
    .stButton>button:hover { background-color: #3CB371; box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2); }
    h1, h2, h3 { color: #006400; }
    .stAlert { border-radius: 12px; }
    .stSuccess { background-color: #98FB98; }
    .stExpander { border: 1px solid #2E8B57; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# --- Function to generate optimal conditions from the dataset ---
@st.cache_data
def generate_optimal_conditions(df_path):
    try:
        df = pd.read_csv(df_path)
        optimal_conditions = df.groupby('label').mean().reset_index()
        optimal_conditions.rename(columns={'label': 'Crop'}, inplace=True)
        return optimal_conditions
    except FileNotFoundError:
        st.error(f"Dataset file not found at {df_path}. Please make sure it's in the correct directory.")
        return None

# --- 3. KNOWLEDGE BASES & DATA ---
# --- UPDATED TO INCLUDE NEW STATES FOR RAINFALL PREDICTOR ---
CROP_SUITABILITY = {
    'Uttar Pradesh': ['rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas', 'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate', 'mango', 'watermelon', 'muskmelon', 'papaya', 'jute'],
    'Maharashtra': ['grapes', 'mango', 'orange', 'pomegranate', 'cotton', 'pigeonpeas', 'maize', 'chickpea'],
    'Punjab': ['rice', 'maize', 'chickpea', 'lentil', 'cotton', 'apple', 'orange'],
    'Gujarat': ['cotton', 'chickpea', 'maize', 'pomegranate', 'mango', 'banana', 'papaya'],
    'Andhra Pradesh': ['rice', 'cotton', 'maize', 'chickpea', 'mungbean', 'pigeonpeas', 'mango', 'papaya'],
    'Himachal Pradesh': ['apple', 'maize', 'rice', 'kidneybeans', 'lentil', 'pomegranate', 'grapes'],
    'Kerala': ['coconut', 'rice', 'banana', 'papaya', 'coffee'],
    'West Bengal': ['jute', 'rice', 'maize', 'lentil', 'pigeonpeas', 'mungbean', 'papaya']
}
AVERAGE_YIELDS = { 'rice': 55, 'maize': 40, 'chickpea': 15, 'kidneybeans': 12, 'pigeonpeas': 10, 'mothbeans': 8, 'mungbean': 7, 'blackgram': 9, 'lentil': 11, 'pomegranate': 150, 'banana': 450, 'mango': 100, 'grapes': 200, 'watermelon': 250, 'muskmelon': 180, 'apple': 200, 'orange': 180, 'papaya': 600, 'coconut': 100, 'cotton': 15, 'jute': 25, 'coffee': 8 }
CULTIVATION_COSTS = { 'rice': 45000, 'maize': 35000, 'chickpea': 30000, 'kidneybeans': 28000, 'pigeonpeas': 25000, 'mothbeans': 22000, 'mungbean': 24000, 'blackgram': 26000, 'lentil': 29000, 'pomegranate': 150000, 'banana': 120000, 'mango': 80000, 'grapes': 200000, 'watermelon': 40000, 'muskmelon': 38000, 'apple': 250000, 'orange': 90000, 'papaya': 100000, 'coconut': 70000, 'cotton': 55000, 'jute': 38000, 'coffee': 180000 }
MARKET_PRICES = {
    'rice': 2203, 'maize': 2090, 'chickpea': 5335, 'kidneybeans': 5500, 'pigeonpeas': 7000,
    'mothbeans': 5200, 'mungbean': 8558, 'blackgram': 6950, 'lentil': 6000, 'pomegranate': 11000,
    'banana': 1200, 'mango': 7500, 'grapes': 6500, 'watermelon': 1000, 'muskmelon': 1200,
    'apple': 8500, 'orange': 5500, 'papaya': 900, 'coconut': 3500, 'cotton': 6620,
    'jute': 5050, 'coffee': 14000
}
SUSTAINABILITY_SCORES = { 'rice': 0.4, 'maize': 0.7, 'chickpea': 0.8, 'kidneybeans': 0.6, 'pigeonpeas': 0.9, 'mothbeans': 0.9, 'mungbean': 0.8, 'blackgram': 0.8, 'lentil': 0.9, 'pomegranate': 0.7, 'banana': 0.5, 'mango': 0.6, 'grapes': 0.6, 'watermelon': 0.4, 'muskmelon': 0.4, 'apple': 0.6, 'orange': 0.7, 'papaya': 0.5, 'coconut': 0.7, 'cotton': 0.5, 'jute': 0.8, 'coffee': 0.6 }
CRITICAL_THRESHOLDS = { 'temperature': {'min': 5.0, 'max': 45.0}, 'humidity': {'min': 15.0, 'max': 98.0}, 'ph': {'min': 4.5, 'max': 8.5}, 'rainfall': {'min': 25.0, 'max': 280.0}, 'N': {'min': 5, 'max': 140}, 'P': {'min': 5, 'max': 140}, 'K': {'min': 5, 'max': 205} }
UNIT_CONVERSION = { 'Hectare': 1.0, 'Acre': 0.404686, 'Bigha': 0.2529 }

FARMING_ADVICE = {
    'N': { 'increase': "Your soil is low on Nitrogen. Add nitrogen-rich organic matter like compost or manure, or use a nitrogen-based fertilizer like Urea.", 'decrease': "Your soil has excess Nitrogen. Avoid nitrogen-heavy fertilizers. Consider planting cover crops like legumes to help balance the soil." },
    'P': { 'increase': "Phosphorus levels are low. Use a phosphorus-rich fertilizer, such as bone meal or rock phosphate, to promote healthy root development.", 'decrease': "Phosphorus levels are high. Avoid adding phosphorus-based fertilizers for the next few seasons." },
    'K': { 'increase': "Potassium levels are deficient. Apply potash fertilizers or natural sources like wood ash to improve plant strength and disease resistance.", 'decrease': "Your soil has excess Potassium. Limit the use of potash or potassium-rich fertilizers." },
    'ph': { 'increase': "The soil is too acidic. Apply lime or wood ash to raise the pH level and make it more alkaline.", 'decrease': "The soil is too alkaline. Apply sulfur or add acidic organic matter like peat moss or compost to lower the pH." },
    'rainfall': { 'increase': "This crop requires more water than your area's average rainfall provides. Plan for regular irrigation, such as a drip system or sprinklers.", 'decrease': "This crop is sensitive to waterlogging. Ensure your fields have good drainage to prevent root rot during heavy rains." },
    'temperature': { 'increase': "The climate is cooler than ideal for this crop. Consider using mulching to retain soil heat or planting in a protected area like a greenhouse.", 'decrease': "The climate is hotter than ideal. Use shade nets to protect plants from extreme sun and schedule irrigation for cooler parts of the day." },
    'humidity': { 'increase': "Low humidity can stress the plant. Regular misting or irrigation can help increase the moisture in the air around the crop.", 'decrease': "High humidity can promote fungal diseases. Ensure good air circulation around plants by spacing them properly." }
}

CROP_GUIDANCE = {
    'apple': """**1. Planting:** Plant saplings in well-prepared pits during the dormant season (December-January). Ensure proper spacing for good air circulation.
        **2. Training & Pruning:** Prune the trees annually to give them a proper shape and remove dead or diseased wood. This is crucial for fruit production.
        **3. Pollination:** Most apple varieties require cross-pollination. Ensure compatible pollinizer varieties are planted nearby, or use beehives.
        **4. Nutrient Management:** Apply a balanced mix of fertilizers and organic manure based on soil tests.
        **5. Pest & Disease Management:** Monitor for common issues like apple scab, powdery mildew, and codling moth. Follow a regular spray schedule.
        **6. Thinning:** Thin the fruitlets when they are small to ensure the remaining fruits grow to a good size and quality.
        **7. Harvesting:** Harvest when the fruit is firm, crisp, and has developed its characteristic color.""",
    'banana': """**1. Planting:** Use healthy suckers or tissue-cultured plantlets. Plant in pits at the beginning of the monsoon.
        **2. Nutrient Management:** Banana is a heavy feeder. Apply fertilizers frequently in split doses.
        **3. Water Management:** Requires a large amount of water. Irrigate regularly, especially during the dry season. Drip irrigation is highly recommended.
        **4. De-suckering:** Remove unwanted suckers regularly to allow the main plant to grow properly.
        **5. Propping:** Provide support to the plants with bamboo poles when the bunch starts to develop to prevent the plant from falling over.
        **6. Bunch Care:** Cover the bunch with a sleeve to protect it from sun, wind, and pests, which improves quality.
        **7. Harvesting:** Harvest the bunch when the fruits are plump and have turned from dark green to a lighter green.""",
    # ... (remaining guidance omitted here for brevity, unchanged from original)
}

# --- OPTIMAL SOIL REQUIREMENTS FOR ALL CROPS ---
CROP_SOIL_REQUIREMENTS = {
    "rice": {"N": 80, "P": 40, "K": 40, "pH_min": 5.0, "pH_max": 6.5},
    "maize": {"N": 120, "P": 60, "K": 40, "pH_min": 5.5, "pH_max": 7.0},
    "chickpea": {"N": 20, "P": 40, "K": 20, "pH_min": 6.0, "pH_max": 8.0},
    "kidneybeans": {"N": 40, "P": 60, "K": 20, "pH_min": 6.0, "pH_max": 7.5},
    "pigeonpeas": {"N": 25, "P": 50, "K": 25, "pH_min": 6.0, "pH_max": 7.5},
    "mothbeans": {"N": 20, "P": 40, "K": 20, "pH_min": 7.0, "pH_max": 8.5},
    "mungbean": {"N": 20, "P": 40, "K": 20, "pH_min": 6.0, "pH_max": 7.5},
    "blackgram": {"N": 20, "P": 40, "K": 20, "pH_min": 6.0, "pH_max": 7.5},
    "lentil": {"N": 20, "P": 50, "K": 20, "pH_min": 6.0, "pH_max": 7.5},
    "pomegranate": {"N": 150, "P": 60, "K": 60, "pH_min": 6.0, "pH_max": 8.0},
    "banana": {"N": 150, "P": 75, "K": 150, "pH_min": 5.5, "pH_max": 7.0},
    "mango": {"N": 120, "P": 60, "K": 60, "pH_min": 5.5, "pH_max": 7.0},
    "grapes": {"N": 180, "P": 100, "K": 200, "pH_min": 5.5, "pH_max": 7.5},
    "apple": {"N": 70, "P": 40, "K": 70, "pH_min": 5.0, "pH_max": 6.5},
    "orange": {"N": 150, "P": 60, "K": 120, "pH_min": 5.0, "pH_max": 6.5},
    "papaya": {"N": 200, "P": 50, "K": 200, "pH_min": 6.0, "pH_max": 7.0},
    "coconut": {"N": 400, "P": 90, "K": 450, "pH_min": 5.2, "pH_max": 8.0},
    "cotton": {"N": 100, "P": 50, "K": 50, "pH_min": 5.8, "pH_max": 8.0},
    "jute": {"N": 80, "P": 40, "K": 40, "pH_min": 5.0, "pH_max": 7.4},
    "coffee": {"N": 80, "P": 60, "K": 80, "pH_min": 6.0, "pH_max": 6.5}
}

# --- 4. LOAD AI MODELS & DATA ---
try:
    # Model 1: Crop Recommendation
    crop_recommender_model = joblib.load('crop_recommender_model.joblib')
    model_classes = joblib.load('crop_class_names.joblib')
    optimal_conditions_df = generate_optimal_conditions('Crop_recommendation.csv')
    
    # Model 2: Rainfall Prediction
    rainfall_predictor = RainfallPredictor()

except FileNotFoundError as e:
    st.error(f"A required file was not found: {e.filename}. Please ensure all model and data files are present.")
    st.stop()


# --- FUNCTIONS ---
def get_seasonal_advice():
    """
    Determines the current agricultural season in India and provides advice.
    """
    current_month = datetime.date.today().month

    if 6 <= current_month <= 9:
        season_name = "Kharif (Monsoon Season)"
        advice = f"We are currently in the **{season_name}**. This is the ideal time for sowing crops that require significant water, such as **Rice, Maize, Cotton, and Pigeonpeas**."
        return advice
    elif current_month >= 10 or current_month <= 3:
        season_name = "Rabi (Winter Season)"
        advice = f"It's currently the **{season_name}**. This season is perfect for crops that thrive in cooler, drier conditions. Consider planting **Wheat, Gram (Chickpea), Lentils, and Mustard**."
        return advice
    else: 
        season_name = "Zaid (Summer Season)"
        advice = f"This is the **{season_name}**, a short period between the Rabi and Kharif seasons. It's a great opportunity for short-duration crops like **Watermelon, Muskmelon, Mungbean, and Cucumber**."
        return advice

def get_suggestions(crop_name, user_input_dict, optimal_df):
    if optimal_df is None: return ["Could not load optimal conditions data."]

    crop_optimal_data = optimal_df[optimal_df['Crop'].str.lower() == crop_name.lower()]
    if crop_optimal_data.empty: return [f"Could not retrieve optimal conditions for {crop_name}."]

    optimal_vals = crop_optimal_data.iloc[0]
    suggestions = []
    params_to_check = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    for param in params_to_check:
        user_val = user_input_dict[param]
        optimal_val = optimal_vals[param]
        tolerance = 0.15 * optimal_val
        advice = ""
        if user_val < (optimal_val - tolerance):
            advice = FARMING_ADVICE.get(param, {}).get('increase')
        elif user_val > (optimal_val + tolerance):
            advice = FARMING_ADVICE.get(param, {}).get('decrease')
        if advice:
            suggestions.append(f"**{param.capitalize()}:** {advice}")
    if not suggestions:
        suggestions.append("✅ Your soil and climate conditions are nearly optimal for this crop! Great job.")
    return suggestions

# --- 5. SIDEBAR FOR USER INPUTS ---
with st.sidebar:
    st.header('Step 1: Select Your Location')
    # Use keys from rainfall data for a dynamic list of states
    location_list = ["Uttar Pradesh","Maharashtra","Punjab","Gujarat","Andhra Pradesh","Himachal Pradesh","Kerala","West Bengal"]
    location = st.selectbox('Choose your state:', location_list)

    st.header('Step 2: Enter Your Land Area')
    land_size = st.number_input('Land Size', min_value=0.1, value=1.0, step=0.1)
    land_unit = st.selectbox('Unit', ['Hectare', 'Acre', 'Bigha'])
    st.caption(f"Note: 1 Bigha is considered ~0.25 Hectare.")

    # --- NEW FEATURE: AI RAINFALL PREDICTION ---
    with st.expander("🌦️ AI Rainfall Prediction", expanded=True):
        current_year = datetime.date.today().year
        prediction_year = st.number_input("Select Year for Forecast", min_value=current_year, max_value=current_year + 5, value=current_year + 1)
        if st.button("Predict Annual Rainfall"):
            with st.spinner("Running AI forecast..."):
                forecast = rainfall_predictor.predict(location, prediction_year)
                # Store forecast in session state to persist across reruns
                st.session_state['rainfall_forecast'] = forecast
                st.session_state['forecast_year'] = prediction_year
                st.session_state['forecast_location'] = location

    st.header('Step 3: Enter Farm Details')
    N = st.slider('Nitrogen (N) Content (kg/ha)', 0, 150, 70, key="N")
    P = st.slider('Phosphorus (P) Content (kg/ha)', 0, 150, 50, key="P")
    K = st.slider('Potassium (K) Content (kg/ha)', 0, 210, 50, key="K")
    temperature = st.slider('Temperature (°C)', 0.0, 50.0, 25.0, 0.1, key="temp")
    humidity = st.slider('Relative Humidity (%)', 0.0, 100.0, 60.0, 0.1, key="humidity")
    ph = st.slider('Soil pH', 0.0, 14.0, 6.5, 0.1, key="ph")
    rainfall = st.slider('Rainfall (mm)', 0.0, 300.0, 100.0, 0.1, key="rainfall")

    st.header('Step 4: Set Your Priorities')
    st.write("Adjust the importance of each factor in the recommendation.")
    ai_weight = st.slider('Scientific Match Importance', 0, 100, 50, 5)
    profit_weight = st.slider('Profitability Importance', 0, 100, 25, 5)
    location_weight = st.slider('Location Suitability Importance', 0, 100, 25, 5)
    sustainability_weight = st.slider('Sustainability Importance', 0, 100, 15, 5)

    predict_button = st.button('Get Advanced Recommendation')

# --- 6. MAIN PAGE CONTENT ---
st.title('🌾 Agro-Advisor: AI-Powered Farming Success')
st.write(f"Welcome, Dipak! This advanced system provides a **holistic recommendation** by balancing soil data, location, profit forecasts, and sustainability. Make the most informed decision for your farm in **{location}**.")
st.markdown("---")

# Display Seasonal Advice
st.subheader(f"🗓️ Timely Advice for {datetime.date.today().strftime('%B %Y')}")
seasonal_advice = get_seasonal_advice()
st.info(seasonal_advice)
st.markdown("---")

# --- NEW FEATURE: DISPLAY RAINFALL FORECAST ---
if 'rainfall_forecast' in st.session_state:
    st.subheader(f"🌦️ AI Rainfall Forecast for {st.session_state['forecast_location']} in {st.session_state['forecast_year']}")
    forecast_data = st.session_state['rainfall_forecast']
    if forecast_data is not None:
        st.line_chart(forecast_data)
        with st.expander("View Forecast Data Table"):
            st.dataframe(forecast_data)
    else:
        st.warning(f"No historical rainfall data available for {st.session_state['forecast_location']} to make a prediction.")
    st.markdown("---")


# --- 7. RECOMMENDATION LOGIC AND DISPLAY (FULL VERSION) ---
if predict_button:
    conversion_factor = UNIT_CONVERSION.get(land_unit, 1.0)
    land_size_in_hectares = land_size * conversion_factor
    user_inputs_dict = {'N': N, 'P': P, 'K': K, 'temperature': temperature, 'humidity': humidity, 'ph': ph, 'rainfall': rainfall}

    warnings = []
    for param, value in user_inputs_dict.items():
        if not (CRITICAL_THRESHOLDS[param]['min'] <= value <= CRITICAL_THRESHOLDS[param]['max']):
            warnings.append(f"**{param.capitalize()} is extreme** ({value}). This is outside the viable range for most crops.")
    if warnings:
        st.error("⚠️ **Critical Alert: Conditions may be unsuitable for farming!**")
        for warning in warnings: st.warning(f"- {warning}")
        st.stop()

    with st.spinner('Running advanced techno-economic analysis...'):
        feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
        input_df = pd.DataFrame([list(user_inputs_dict.values())], columns=feature_names)
        ai_probabilities = crop_recommender_model.predict_proba(input_df)[0]
        top_n_indices = np.argsort(ai_probabilities)[-5:][::-1]
        top_crops = np.array(model_classes)[top_n_indices]
        top_probs = ai_probabilities[top_n_indices]
        results = []

        # compute profits using normalized keys to avoid mismatches
        def lookup(keydict, name):
            return keydict.get(name.lower(), keydict.get(name, 0))

        profits = [((lookup(AVERAGE_YIELDS, c) * lookup(MARKET_PRICES, c)) - lookup(CULTIVATION_COSTS, c)) for c in model_classes]
        max_profit_per_hectare = max(profits) if profits else 1
        if max_profit_per_hectare <= 0:
            max_profit_per_hectare = max(1, max(profits))  # avoid divide by zero or negative normalization

        total_weight = ai_weight + profit_weight + location_weight + sustainability_weight
        if total_weight == 0: total_weight = 1
        weights = {
            'ai': ai_weight / total_weight,
            'profit': profit_weight / total_weight,
            'location': location_weight / total_weight,
            'sustainability': sustainability_weight / total_weight
        }

        suitable_crops_for_location = CROP_SUITABILITY.get(location, [])
        for crop, prob in zip(top_crops, top_probs):
            c_key = crop.lower()
            ai_score = prob
            location_score = 1.0 if c_key in suitable_crops_for_location else 0.2
            sustainability_score = SUSTAINABILITY_SCORES.get(c_key, 0.5)

            yield_q = lookup(AVERAGE_YIELDS, c_key)
            price_q = lookup(MARKET_PRICES, c_key)
            cost_per_hectare = lookup(CULTIVATION_COSTS, c_key)

            profit_per_hectare = (yield_q * price_q) - cost_per_hectare
            profit_score = max(0, profit_per_hectare / max_profit_per_hectare) if max_profit_per_hectare > 0 else 0
            total_profit = profit_per_hectare * land_size_in_hectares
            total_cost = cost_per_hectare * land_size_in_hectares

            final_score = (ai_score * weights['ai'] +
                           location_score * weights['location'] +
                           profit_score * weights['profit'] +
                           sustainability_score * weights['sustainability'])

            results.append({
                'Crop': str(crop).capitalize(),
                'Final Score': final_score,
                'Total Estimated Profit': total_profit,
                'Total Estimated Cost': total_cost,
                'Details': f"AI Match: {ai_score:.2f} | Location Fit: {location_score:.2f} | Profit Score: {profit_score:.2f} | Sustainability: {sustainability_score:.2f}",
                'Yield per Hectare': yield_q,
                'Price per Quintal': price_q,
                'Cost per Hectare': cost_per_hectare
            })
        ranked_results = sorted(results, key=lambda x: x['Final Score'], reverse=True)

        # Display results table and comparison chart
        results_df = pd.DataFrame(ranked_results)
        st.header("🏆 Your Personalized Farm Plan")
        st.subheader("📊 Top Recommended Crops")
        st.dataframe(results_df)

        # --- Crop Comparison Chart (Profit & Yield) ---
        st.subheader("📈 Crop Comparison Chart")
        if not results_df.empty:
            compare_df = results_df[["Crop", "Yield per Hectare", "Total Estimated Profit"]].copy()
            compare_df = compare_df.set_index("Crop")
            # Normalize profit for chart readability (per hectare)
            compare_df["Profit per Hectare"] = compare_df["Total Estimated Profit"] / max(1, land_size_in_hectares)
            compare_df = compare_df[["Yield per Hectare", "Profit per Hectare"]]
            st.bar_chart(compare_df)

        top_crop_info = ranked_results[0]

        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            st.success(f"### Best Option: **{top_crop_info['Crop']}**")
            st.write(f"This crop presents the best overall balance based on **your selected priorities**.")
            st.markdown(f"**Score Breakdown:** _{top_crop_info['Details']}_")
        with col2:
            st.metric(label=f"Total Est. Cost for {land_size} {land_unit}(s)", value=f"₹{top_crop_info['Total Estimated Cost']:,.0f}")
            st.metric(label=f"Total Est. Profit for {land_size} {land_unit}(s)", value=f"₹{top_crop_info['Total Estimated Profit']:,.0f}")
            st.metric(label="Overall Score", value=f"{top_crop_info['Final Score']:.2f}")

        st.markdown("---")
        st.subheader("✅ Actionable Suggestions for Best Yield")
        suggestions = get_suggestions(top_crop_info['Crop'].lower(), user_inputs_dict, optimal_conditions_df)
        if suggestions:
            suggestion_text = "\n".join([f"{i+1}. {s}" for i, s in enumerate(suggestions)])
            st.info(suggestion_text)

        st.markdown("---")
        with st.expander(f"🧑‍🌾 View Step-by-Step Farming Guide for {top_crop_info['Crop']}"):
            guide = CROP_GUIDANCE.get(top_crop_info['Crop'].lower(), "No detailed guide available for this crop yet.")
            st.markdown(guide)

        # --- Fertilizer Recommendation for top crop (SMART engine) ---
        with st.expander(f"🌱 Fertilizer Recommendation for {top_crop_info['Crop']}"):
            crop = top_crop_info['Crop']
            c_key = crop.lower().replace(" ", "")
            req = CROP_SOIL_REQUIREMENTS.get(c_key, None)

            if req:
                messages = []
                fertilizers = []

                if N < req["N"]:
                    fertilizers.append("Urea (46% N)")
                    messages.append(f"- Nitrogen ({N}) is lower than ideal ({req['N']}). Urea increases vegetative growth.")

                if P < req["P"]:
                    fertilizers.append("DAP / SSP")
                    messages.append(f"- Phosphorus ({P}) is lower than ideal ({req['P']}). DAP/SSP improves root strength and flowering.")

                if K < req["K"]:
                    fertilizers.append("MOP / SOP")
                    messages.append(f"- Potassium ({K}) is below ideal ({req['K']}). Potash improves yield and disease resistance.")

                if ph < req["pH_min"]:
                    fertilizers.append("Lime")
                    messages.append(f"- Soil pH is acidic ({ph}). Lime helps raise pH to the ideal range {req['pH_min']}–{req['pH_max']}.")

                elif ph > req["pH_max"]:
                    fertilizers.append("Gypsum")
                    messages.append(f"- Soil pH is alkaline ({ph}). Gypsum helps lower pH for better nutrient availability.")

                if fertilizers:
                    st.write(f"**Recommended Fertilizers:** {', '.join(set(fertilizers))}")
                    st.write("**Why these?**")
                    for m in messages:
                        st.write(m)
                else:
                    st.success("Your soil nutrients already match ideal conditions for this crop! Minimal fertilizer needed.")
            else:
                st.info("No fertilizer data available for this crop.")

        st.markdown("---")
        with st.expander(f"💰 View Financial Breakdown for {top_crop_info['Crop']}"):
            total_revenue = top_crop_info['Total Estimated Profit'] + top_crop_info['Total Estimated Cost']
            st.markdown(f"""
            **Formula:** Total Revenue - Total Cost = Total Profit
            - **Total Revenue:** Calculated as `(Yield per Hectare * Price per Quintal) * Land Size in Hectares`
                - `({top_crop_info['Yield per Hectare']} * ₹{top_crop_info['Price per Quintal']:,}) * {land_size_in_hectares:.2f} = ₹{total_revenue:,.0f}`
            - **Total Cost:** Calculated as `(Cost per Hectare * Land Size in Hectares)`
                - `(₹{top_crop_info['Cost per Hectare']:,}) * {land_size_in_hectares:.2f} = ₹{top_crop_info['Total Estimated Cost']:,.0f}`
            - **Total Estimated Profit:** `₹{total_revenue:,.0f} - ₹{top_crop_info['Total Estimated Cost']:,.0f} = ₹{top_crop_info['Total Estimated Profit']:,.0f}`
            """)

        st.subheader("🥈 Other Good Alternatives")
        for result in ranked_results[1:]:
            with st.expander(f"{result['Crop']} (Score: {result['Final Score']:.2f}) | Est. Profit: ₹{result['Total Estimated Profit']:,.0f} | Est. Cost: ₹{result['Total Estimated Cost']:,.0f}"):
                st.markdown(f"**Score Breakdown:** _{result['Details']}_")
                st.markdown("---")
                st.markdown("**Actionable Suggestions for this crop:**")
                suggestions_for_alternative = get_suggestions(result['Crop'].lower(), user_inputs_dict, optimal_conditions_df)
                if suggestions_for_alternative:
                    suggestion_text_alt = "\n".join([f"{i+1}. {s}" for i, s in enumerate(suggestions_for_alternative)])
                    st.info(suggestion_text_alt)

                # --- Fertilizer Recommendation for this alternative crop ---
                st.markdown("---")
                crop_alt = result['Crop']
                c_key_alt = crop_alt.lower().replace(" ", "")
                req_alt = CROP_SOIL_REQUIREMENTS.get(c_key_alt, None)

                if req_alt:
                    messages_alt = []
                    fertilizers_alt = []

                    if N < req_alt["N"]:
                        fertilizers_alt.append("Urea (46% N)")
                        messages_alt.append(f"- Nitrogen ({N}) is lower than ideal ({req_alt['N']}). Urea increases vegetative growth.")

                    if P < req_alt["P"]:
                        fertilizers_alt.append("DAP / SSP")
                        messages_alt.append(f"- Phosphorus ({P}) is lower than ideal ({req_alt['P']}). DAP/SSP improves root strength and flowering.")

                    if K < req_alt["K"]:
                        fertilizers_alt.append("MOP / SOP")
                        messages_alt.append(f"- Potassium ({K}) is below ideal ({req_alt['K']}). Potash improves yield and disease resistance.")

                    if ph < req_alt["pH_min"]:
                        fertilizers_alt.append("Lime")
                        messages_alt.append(f"- Soil pH is acidic ({ph}). Lime helps raise pH to the ideal range {req_alt['pH_min']}–{req_alt['pH_max']}.")

                    elif ph > req_alt["pH_max"]:
                        fertilizers_alt.append("Gypsum")
                        messages_alt.append(f"- Soil pH is alkaline ({ph}). Gypsum helps lower pH for better nutrient availability.")

                    if fertilizers_alt:
                        st.write(f"**Recommended Fertilizers:** {', '.join(set(fertilizers_alt))}")
                        st.write("**Why these?**")
                        for m in messages_alt:
                            st.write(m)
                    else:
                        st.success("Your soil nutrients already match ideal conditions for this crop! Minimal fertilizer needed.")
                else:
                    st.info("No fertilizer data available for this crop.")

                st.markdown("---")
                total_revenue_alt = result['Total Estimated Profit'] + result['Total Estimated Cost']
                st.markdown(f"""
                **Financial Breakdown:**
                - Total Revenue: `₹{total_revenue_alt:,.0f}`
                - Total Cost: `₹{result['Total Estimated Cost']:,.0f}`
                - **Total Profit: `₹{result['Total Estimated Profit']:,.0f}`**
                """)

else:
    st.info("Enter your farm's details in the sidebar and click the button to generate your personalized farm plan.")
