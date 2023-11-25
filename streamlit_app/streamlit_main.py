import streamlit as st
import os
from datetime import date, datetime

# Initialize session state
if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

# Function to display login page
def login_page():
    st.title("Travel Plan Creator - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        st.session_state['login_status'] = True
        st.session_state['username'] = username
        st.experimental_rerun()

# Function to save questionnaire data
def save_questionnaire(username, responses):
    folder_path = f"./{username}"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a new file with the timestamp in its name
    file_name = f"{folder_path}/{username}_questionaire_data_{timestamp}.txt"
    
    with open(file_name, "w") as file:
        for question, answer in responses.items():
            file.write(f"{question}: {answer}\n")

# Function to display questionnaire
def user_questionnaire(username):
    # Layout with columns for logout button
    if st.sidebar.button("Logout"):
        st.session_state['login_status'] = False
        st.session_state['username'] = ''
        st.rerun()
    # Place the logout button in the second column (top right

    # Use the first column for the questionnaire content
    st.title(f"Welcome {username}, let's plan your trip!")
    
    # Trip Duration
    st.header("Trip Duration")
    days = st.number_input("How many days are you planning to spend in India?")
    # Travel Dates and Season
    st.header("Travel Dates and Season")
    start_date = st.date_input("Trip Start Date", min_value=date.today())
    end_date = st.date_input("Trip End Date", min_value=start_date)
    season_pref = st.text_input("Are there any seasonal preferences or constraints?")
    # Interests and Preferences
    st.header("Interests and Preferences")
    interests = st.multiselect("Are you interested in historical sites, cultural experiences, natural scenery, or urban attractions?",
                               ["Historical Sites", "Cultural Experiences", "Natural Scenery", "Urban Attractions"])
    specific_interests = st.text_input("Do you have any specific interests such as wildlife, culinary exploration, spirituality, or adventure sports?")
    # Travel Style
    st.header("Travel Style")
    travel_style = st.radio("Do you prefer a relaxed or an active, adventure-packed itinerary?", ["Relaxed", "Active"])
    accommodation_pref = st.text_input("What type of accommodations do you prefer (luxury, budget, boutique, hostels)?")
    # Regions of Interest
    st.header("Regions of Interest")
    regions = st.text_input("Are there specific regions or cities in India you are particularly keen to explore?")
    # Previous Visits
    st.header("Previous Visits")
    previous_visits = st.text_input("Have you visited India before? If yes, which parts?")
    # Mobility and Accessibility
    st.header("Mobility and Accessibility")
    mobility_requirements = st.text_input("Do you have any special mobility or accessibility requirements?")
    # Budget
    st.header("Budget")
    budget = st.number_input("What is your approximate budget (Rupees) for this trip?", min_value=0)
    # Travel Companions
    st.header("Travel Companions")
    travel_companions = st.selectbox("Are you traveling solo, with family, friends, or as a couple?", 
                                     ["Solo", "Family", "Friends", "Couple"])
    children_info = st.text_input("Are there any children in the group, and if so, what are their ages?")
    # Special Events or Experiences
    st.header("Special Events or Experiences")
    special_events = st.text_input("Are you interested in attending any festivals, events, or specific experiences (e.g., yoga retreat, wildlife safari)?")
    # Dietary Restrictions/Preferences
    st.header("Dietary Restrictions/Preferences")
    dietary_restrictions = st.text_input("Do you have any dietary restrictions or preferences?")
    # Health and Safety
    st.header("Health and Safety")
    health_concerns = st.text_input("Are there any health concerns or vaccinations needed for your travel to India?")
    # Transportation Preferences
    st.header("Transportation Preferences")
    transportation_pref = st.text_input("What are your preferences regarding internal transportation (flights, trains, private car, etc.)?")
    # Language and Communication
    st.header("Language and Communication")
    language_requirements = st.text_input("Do you have any language preferences or requirements for guides or interpreters?")
    # Cultural Sensitivity and Adaptation
    st.header("Cultural Sensitivity and Adaptation")
    cultural_sensitivity = st.text_input("Are there any cultural aspects or local customs you would like to learn about or be particularly respectful of?")
    # Emergency Contact Information
    st.header("Emergency Contact Information")
    emergency_contact = st.text_input("Do you have any emergency contact information or requirements?")
    if st.button("Submit"):
        user_questionnaire_response = {
            "Trip Duration": days,
            "Travel Dates": [start_date, end_date],
            "Season Preferences": season_pref,
            "Interests": interests,
            "Specific Interests": specific_interests,
            "Travel Style": travel_style,
            "Accommodation Preferences": accommodation_pref,
            "Regions of Interest": regions,
            "Previous Visits": previous_visits,
            "Mobility Requirements": mobility_requirements,
            "Budget (in Rupees)": budget,
            "Travel Companions": travel_companions,
            "Children Information": children_info,
            "Special Events": special_events,
            "Dietary Restrictions": dietary_restrictions,
            "Health Concerns": health_concerns,
            "Transportation Preferences": transportation_pref,
            "Language Requirements": language_requirements,
            "Cultural Sensitivity": cultural_sensitivity,
            "Emergency Contact": emergency_contact
        }
        save_questionnaire(username, user_questionnaire_response)
        st.success("Questionnaire saved, we'll curate your travel plan and reach out to you.")


# Main function of the Streamlit app
def main():
    if not st.session_state['login_status']:
        login_page()
    else:
        user_questionnaire(st.session_state['username'])

if __name__ == "__main__":
    main()
