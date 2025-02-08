import streamlit as st
import requests

# Flask API URL 
API_URL = "http://127.0.0.1:5000/search"  

# Streamlit UI
st.title("BrainLox Course Search Chatbot 🔍")

st.write("Ask me anything about BrainLox courses, and I'll find the best matches for you!")

# User input
query = st.text_input("Enter your query:", "")

if st.button("Search"):
    if query:
        response = requests.post(API_URL, json={"query": query})

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])

            if results:
                st.subheader("Top Matching Courses:")
                for idx, result in enumerate(results, start=1):
                    st.write(f"**{idx}. {result['course']}**")
                    st.write(f"📖 **Description:** {result['metadata'].get('description', 'No description available')}")
                    st.write("---")  # Divider
            else:
                st.warning("No matching courses found. Try a different query!")
        else:
            st.error("Error fetching results. Please try again later.")
    else:
        st.warning("Please enter a query before searching!")

