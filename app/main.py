import streamlit as st
import requests
import json
from typing import Dict, Any
import os

# Configure page
st.set_page_config(
    page_title="PathWeaver AI",
    page_icon="🧭",
    layout="wide"
)

# Constants
API_ENDPOINT = os.getenv("API_ENDPOINT", "http://localhost:8000")

def generate_path(query: str, user_id: str = None) -> Dict[str, Any]:
    """Call the API to generate a learning path."""
    try:
        response = requests.post(
            f"{API_ENDPOINT}/generate-path",
            json={
                "query": query,
                "user_id": user_id
            }
        )
        return response.json()
    except Exception as e:
        st.error(f"Error generating path: {str(e)}")
        return None

def display_learning_path(path: Dict[str, Any]):
    """Display the learning path in a structured format."""
    if not path or "error" in path:
        st.error("Failed to generate learning path")
        return

    # Display prerequisites
    st.subheader("Prerequisites")
    for prereq in path.get("prerequisites", []):
        st.write(f"• {prereq}")

    # Display learning steps
    st.subheader("Learning Path")
    for i, step in enumerate(path.get("steps", []), 1):
        with st.expander(f"Step {i}: {step['title']}"):
            st.write(step["description"])
            st.write(f"⏱️ Estimated time: {step['estimated_time']}")
            
            st.write("📚 Resources:")
            for resource in step.get("resources", []):
                st.write(f"• [{resource.get('title')}]({resource.get('url')})")
                if "description" in resource:
                    st.write(f"  {resource['description']}")

def main():
    # Header
    st.title("🧭 PathWeaver AI")
    st.write("""
    Your personalized learning navigator for advanced technical domains.
    Ask a question about what you want to learn, and we'll create a customized learning path for you.
    """)

    # Sidebar for user profile (MVP version)
    with st.sidebar:
        st.subheader("Your Profile")
        experience_level = st.selectbox(
            "Experience Level",
            ["Beginner", "Intermediate", "Advanced"]
        )
        preferred_learning_style = st.multiselect(
            "Preferred Learning Style",
            ["Theoretical", "Practical", "Visual", "Interactive"],
            ["Practical"]
        )
        available_time = st.slider(
            "Available time per week (hours)",
            min_value=1,
            max_value=40,
            value=10
        )

    # Main query input
    query = st.text_area(
        "What would you like to learn?",
        placeholder="e.g., 'Create a learning plan to understand and implement Graph Neural Networks for drug discovery, assuming I know Python and basic deep learning.'"
    )

    if st.button("Generate Learning Path"):
        if query:
            with st.spinner("Generating your personalized learning path..."):
                # In MVP, we'll just pass these as part of the query
                context = f"""Experience: {experience_level}
                Learning Style: {', '.join(preferred_learning_style)}
                Available Time: {available_time} hours/week"""
                
                full_query = f"{query}\n\nContext:\n{context}"
                path = generate_path(full_query)
                display_learning_path(path)
        else:
            st.warning("Please enter a learning goal")

if __name__ == "__main__":
    main() 