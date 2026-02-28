import streamlit as st
import requests
import webbrowser

# --- CONFIGURATION ---
# Replace 'YOUR_FAL_KEY' with your actual key from fal.ai
FAL_API_KEY = "dfdea7e3-3255-46de-94e5-8ea632f9d69a:30cfc7098fd85e3e9e6fc93fa63cedd8" 

st.set_page_config(page_title="AI Fashion Design Generator", layout="wide")

# --- UI HEADER ---
st.title("Dream it. Design it. Wear it.")
st.write("Type a clothing concept to generate a design and find affordable matches.")

# --- USER INPUT ---
col1, col2 = st.columns([4, 1])
with col1:
    user_prompt = st.text_input("Describe your fashion idea...", placeholder="e.g., A vintage denim jacket with neon embroidery")
with col2:
    generate_btn = st.button("Generate", use_container_width=True)

# Style Tags
tags = ["Casual", "Formal", "Streetwear", "Bohemian", "Minimalist", "Vintage", "Sporty", "Y2K"]
selected_tag = st.multiselect("Add Styles:", tags)

# --- AI GENERATION LOGIC ---
if generate_btn and user_prompt:
    full_prompt = f"{user_prompt}, {', '.join(selected_tag)} fashion design, professional photography, white background"
    
    with st.spinner("Creating your unique design..."):
        try:
            # API Call to Fal.ai (Flux Model)
            headers = {
                "Authorization": f"Key {FAL_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {"prompt": full_prompt, "image_size": "square_hd"}
            
            response = requests.post("https://queue.fal.run/fal-ai/flux/kontext-pro", json=payload, headers=headers)
            
            if response.status_code == 200:
                img_url = response.json().get("image", {}).get("url")
                
                # Show Result
                st.subheader("Your AI Generated Design")
                st.image(img_url, width=500)
                
                # --- AFFORDABLE PRODUCT SEARCH ---
                st.divider()
                st.subheader("Find Affordable Versions")
                shopping_url = f"https://www.google.com/search?tbm=shop&q={user_prompt.replace(' ', '+')}+affordable"
                
                st.write("Ready to buy something similar?")
                st.link_button("View Affordable Items on Google Shopping", shopping_url)
                
            else:
                st.error("AI Service busy. Please check your API Key.")
        except Exception as e:
            st.error(f"Error: {e}")

elif generate_btn and not user_prompt:
    st.warning("Please enter a description first!")
