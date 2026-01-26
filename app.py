import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime, timedelta

# --- CONFIGURATION & MOCK DATA ---
st.set_page_config(page_title="Multilingual Mandi", page_icon="🌾", layout="wide")

# 1. Simulated Database of APMC Market Rates
# In a real app, this comes from a live API/Database
MARKET_DATA = {
    "Tomato": {"price": 20, "trend": "up", "demand": "high"},
    "Onion": {"price": 35, "trend": "stable", "demand": "medium"},
    "Potato": {"price": 18, "trend": "down", "demand": "low"},
    "Wheat": {"price": 22, "trend": "up", "demand": "high"},
    "Rice": {"price": 28, "trend": "up", "demand": "high"},
    "Carrot": {"price": 25, "trend": "stable", "demand": "medium"},
    "Cabbage": {"price": 15, "trend": "down", "demand": "low"},
    "Cauliflower": {"price": 30, "trend": "up", "demand": "high"},
    "Brinjal": {"price": 22, "trend": "stable", "demand": "medium"},
    "Okra": {"price": 40, "trend": "up", "demand": "high"},
    "Green Chili": {"price": 60, "trend": "up", "demand": "high"},
    "Coriander": {"price": 80, "trend": "stable", "demand": "medium"},
    "Spinach": {"price": 20, "trend": "down", "demand": "low"},
    "Garlic": {"price": 120, "trend": "up", "demand": "high"},
    "Ginger": {"price": 100, "trend": "stable", "demand": "medium"}
}

# 2. Simulated Translation Layer (The "Bridge")
# In production, use APIs like: Google Translate, Azure Translator, or Bhashini (India)
TRANSLATIONS = {
    "hi": {
        "title": "बहुभाषी मंडी (Multilingual Mandi)",
        "welcome": "नमस्ते! आप आज क्या बेचना चाहते हैं?",
        "ask_crop": "फसल का नाम बताएं (जैसे: टमाटर, प्याज)",
        "market_rate": "बाजार भाव",
        "negotiate": "भाव-ताव करें",
        "offer_accepted": "बधाई हो! सौदा पक्का हुआ।",
        "offer_rejected": "माफ कीजिये, भाव बहुत कम है।",
        "analyzing": "एआई बाजार का विश्लेषण कर रहा है...",
        "your_offer": "आपकी कीमत (₹/kg):"
    },
    "pb": {
        "title": "ਬਹੁ-ਭਾਸ਼ਾਈ ਮੰਡੀ (Multilingual Mandi)",
        "welcome": "ਸਤਿ ਸ਼੍ਰੀ ਅਕਾਲ! ਤੁਸੀਂ ਅੱਜ ਕੀ ਵੇਚਣਾ ਚਾਹੁੰਦੇ ਹੋ?",
        "ask_crop": "ਫਸਲ ਦਾ ਨਾਮ ਦੱਸੋ (ਜਿਵੇਂ: ਟਮਾਟਰ, ਪਿਆਜ਼)",
        "market_rate": "ਮੰਡੀ ਦਾ ਭਾਅ",
        "negotiate": "ਗੱਲਬਾਤ ਕਰੋ",
        "offer_accepted": "ਵਧਾਈਆਂ! ਸੌਦਾ ਪੱਕਾ ਹੋ ਗਿਆ।",
        "offer_rejected": "ਮਾਫ ਕਰਨਾ, ਭਾਅ ਬਹੁਤ ਘੱਟ ਹੈ।",
        "analyzing": "AI ਮਾਰਕੀਟ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰ ਰਿਹਾ ਹੈ...",
        "your_offer": "ਤੁਹਾਡੀ ਕੀਮਤ (₹/kg):"
    },
    "en": {
        "title": "The Multilingual Mandi",
        "welcome": "Hello! What do you want to sell today?",
        "ask_crop": "Name the crop (e.g., Tomato, Onion)",
        "market_rate": "Market Rate",
        "negotiate": "Negotiate Deal",
        "offer_accepted": "Congratulations! Deal confirmed.",
        "offer_rejected": "Sorry, that price is too low.",
        "analyzing": "AI is analyzing the market...",
        "your_offer": "Your Offer (₹/kg):"
    }
}

# --- HELPER FUNCTIONS ---

def get_dynamic_price(base_price, crop_name):
    """Simulate daily price fluctuations based on date and market factors"""
    today = datetime.now()
    
    # Use date as seed for consistent daily prices
    random.seed(int(today.strftime("%Y%m%d")) + hash(crop_name))
    
    # Market factors that affect price
    seasonal_factor = 1 + (random.random() - 0.5) * 0.3  # ±15% seasonal variation
    demand_factor = 1 + (random.random() - 0.5) * 0.2   # ±10% demand variation
    weather_factor = 1 + (random.random() - 0.5) * 0.25  # ±12.5% weather impact
    
    # Calculate dynamic price
    dynamic_price = int(base_price * seasonal_factor * demand_factor * weather_factor)
    
    # Ensure price doesn't go too extreme
    min_price = int(base_price * 0.6)  # Not below 60% of base
    max_price = int(base_price * 1.4)  # Not above 140% of base
    
    return max(min_price, min(max_price, dynamic_price))

def get_price_trend(base_price, current_price):
    """Determine if price is trending up, down, or stable"""
    change_percent = ((current_price - base_price) / base_price) * 100
    
    if change_percent > 5:
        return "up"
    elif change_percent < -5:
        return "down"
    else:
        return "stable"

def get_translation(lang_code, key):
    """Fetches text based on selected language."""
    return TRANSLATIONS.get(lang_code, TRANSLATIONS['en']).get(key, key)

def ai_negotiator(crop, user_price, market_price):
    """
    Simple rule-based AI for negotiation.
    In production, this would use an LLM (Large Language Model).
    """
    margin = 0.10  # 10% negotiation margin
    min_acceptable = market_price * (1 - margin)
    
    if user_price >= market_price:
        return "accept", f"Great! Locking price at ₹{user_price}. (Market avg: ₹{market_price})"
    elif user_price >= min_acceptable:
        return "accept", f"It's slightly below market, but we accept ₹{user_price} for instant payment."
    else:
        counter_offer = int(min_acceptable)
        return "reject", f"Too low. Market is at ₹{market_price}. Best we can do is ₹{counter_offer}."

# --- MAIN APP UI ---

def main():
    # Sidebar for Settings
    st.sidebar.header("⚙️ Settings / सेटिंग्स")
    lang = st.sidebar.selectbox("Select Language / भाषा चुनें", 
                                ["English (en)", "Hindi (hi)", "Punjabi (pb)"])
    lang_code = lang.split("(")[1].strip(")")
    
    # Quick Stats in Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🌾 Today's Market")
    st.sidebar.metric("Active Traders", "1,247")
    st.sidebar.metric("Deals Closed", "89")
    st.sidebar.metric("Avg Savings", "₹2.5/kg")
    
    # App Header
    st.title("🌾 " + get_translation(lang_code, "title"))
    st.markdown("---")

    # 1. Voice/Input Simulation
    st.subheader("🎙️ " + get_translation(lang_code, "welcome"))
    
    # Voice input simulation
    if st.button("🎤 Voice Input / आवाज़ से बोलें"):
        st.info("🔊 Voice recognition activated... (Demo mode)")
        time.sleep(1)
        st.success("✅ Voice captured: 'मैं टमाटर बेचना चाहता हूं'")
    
    # Option 1: Select from dropdown
    crop_input = st.selectbox(get_translation(lang_code, "ask_crop"), 
                              ["", "Tomato", "Onion", "Potato", "Wheat", "Rice", "Carrot", 
                               "Cabbage", "Cauliflower", "Brinjal", "Okra", "Green Chili", 
                               "Coriander", "Spinach", "Garlic", "Ginger"])
    
    # Option 2: Or type crop name
    if not crop_input:
        crop_text = st.text_input("Or type crop name / या फसल का नाम टाइप करें")
        if crop_text:
            # Find matching crop (case insensitive)
            for crop in MARKET_DATA.keys():
                if crop.lower() in crop_text.lower() or crop_text.lower() in crop.lower():
                    crop_input = crop
                    break
            if not crop_input:
                st.warning(f"Crop '{crop_text}' not found. Available: {', '.join(MARKET_DATA.keys())}")

    # 2. Market Intelligence Dashboard
    if crop_input:
        base_data = MARKET_DATA[crop_input]
        
        # Get dynamic price for today
        current_price = get_dynamic_price(base_data['price'], crop_input)
        trend = get_price_trend(base_data['price'], current_price)
        
        # Show price update timestamp
        st.info(f"🔍 {get_translation(lang_code, 'analyzing')} | Last updated: {datetime.now().strftime('%H:%M:%S')}")
        time.sleep(1) # Simulate AI processing delay
        
        # Display Stats Card
        # Display Stats Card with Dynamic Pricing
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            price_change = current_price - base_data['price']
            st.metric(
                label=get_translation(lang_code, "market_rate"), 
                value=f"₹{current_price}/kg",
                delta=f"₹{price_change:+d} from base"
            )
        with col2:
            trend_emoji = "📈" if trend == "up" else "📉" if trend == "down" else "➡️"
            st.metric(label="Trend", value=trend.upper(), delta=trend_emoji)
        with col3:
            demand_emoji = "🔥" if base_data['demand'] == "high" else "⚡" if base_data['demand'] == "medium" else "❄️"
            st.metric(label="Demand", value=base_data['demand'].upper())
        with col4:
            # Show tomorrow's predicted price
            tomorrow_price = get_dynamic_price(base_data['price'], crop_input + "_tomorrow")
            price_diff = tomorrow_price - current_price
            st.metric(
                label="Tomorrow's Forecast", 
                value=f"₹{tomorrow_price}/kg",
                delta=f"₹{price_diff:+d}"
            )

        st.markdown("---")

        # 3. Negotiation Bot
        st.write(f"### 🤝 {get_translation(lang_code, 'negotiate')}")
        
        # User makes an offer
        user_offer = st.number_input(get_translation(lang_code, "your_offer"), min_value=1, max_value=200, value=current_price)
        
        if st.button("Confirm Offer / भाव पक्का करें"):
            decision, message = ai_negotiator(crop_input, user_offer, current_price)
            
            if decision == "accept":
                st.success(f"✅ {get_translation(lang_code, 'offer_accepted')}")
                st.caption(f"📝 {message}") # Digital Contract Note
                st.balloons()
            else:
                st.error(f"❌ {get_translation(lang_code, 'offer_rejected')}")
                st.warning(f"🤖 AI: {message}")
    
    # Impact Dashboard
    st.markdown("---")
    st.markdown("### 📊 Digital India Impact")
    
    impact_col1, impact_col2, impact_col3, impact_col4 = st.columns(4)
    with impact_col1:
        st.metric("Farmers Helped", "2,500+", "↗️ 15%")
    with impact_col2:
        st.metric("Languages", "3", "🌍")
    with impact_col3:
        st.metric("Fair Deals", "₹50L+", "💰")
    with impact_col4:
        st.metric("Villages", "150+", "🏘️")
    
    st.markdown("---")
    st.markdown("🇮🇳 **Built for Bharat - AI for Every Farmer** 🌾")
    st.markdown("*Breaking language barriers, building digital bridges*")

if __name__ == "__main__":
    main()