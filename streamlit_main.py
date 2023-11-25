import streamlit as st
import os, re
from datetime import date, datetime
from pathlib import Path
from utility import *

Path('./users').mkdir(parents=True, exist_ok=True)

# Initialize session state
if 'login_status' not in st.session_state:
    st.session_state['login_status'] = False
if 'username' not in st.session_state:
    st.session_state['username'] = ''

def save_user_info(username, email, password):
    users_folder = "./users"
    if not os.path.exists(users_folder):
        os.makedirs(users_folder)

    with open(f"{users_folder}/{username}.txt", "w") as file:
        file.write(f"Username: {username}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Password: {password}\n")  # In a real app, you should hash passwords before saving

def user_exists(username, email=None):
    if os.path.exists(f"./users/{username}.txt"):
        return True
    if email:
        for file in os.listdir('./users'):
            with open(f'./users/{file}', 'r') as f:
                for line in f:
                    if line.startswith('Email:') and line.strip().endswith(email):
                        return True
    return False

def validate_email(email):
    # Define the pattern for valid emails
    pattern = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
    
    # Check if the email matches the pattern
    if re.match(pattern, email):
        # Further check for allowed domains (if necessary)
        allowed_domains = ['gmail.com', 'doormail.com', 'outlook.com']
        domain = email.split('@')[-1]
        if domain in allowed_domains:
            return True, 'Valid email format and domain.'
        else:
            return False, "Invalid email domain."
    else:
        return False, "Invalid email format."


def signup_page():
    st.title("Travel Plan Creator - Signup")
    new_username = st.text_input("Username")
    email = st.text_input("Email - (Allowed domains: gmail.com, doormail.com and outlook.com)")
    new_password = st.text_input("Password - (Password must be at least 8 characters long)", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Signup"):
        if new_username and email and new_password and confirm_password:
            email_validity, message = validate_email(email)
            if user_exists(new_username):
                st.error("User already exists for this username.")
            elif not email_validity:
                st.error(message)
            elif user_exists(new_username, email):
                st.error("User already exists for this email.")
            elif len(new_password) < 8:
                st.error("Password must be at least 8 characters long.")
            elif new_password == confirm_password:
                save_user_info(new_username, email, new_password)
                st.success("Signup successful. Please login.")
            else:
                st.error("Passwords do not match.")
        else:
            st.error("Please fill in all the fields.")


def get_user_info(username):
    user_file = f"./users/{username}.txt"
    if os.path.exists(user_file):
        with open(user_file, "r") as file:
            user_data = {}
            for line in file:
                key, value = line.strip().split(": ")
                user_data[key] = value
            return user_data
    return None


# Function to display login page
def login_page():
    st.title("Travel Plan Creator - Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_data = get_user_info(username)
        if user_data and user_data.get("Password") == password:
            st.session_state['login_status'] = True
            st.session_state['username'] = username
            st.session_state['user_email'] = user_data.get('Email')
            st.experimental_rerun()
        else:
            st.error("Invalid username or password.")


# Function to save questionnaire data
def save_questionnaire(username, responses):
    folder_path = f"./user_questionnaire_data/{username}"
    Path(folder_path).mkdir(parents=True, exist_ok=True)    
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a new file with the timestamp in its name
    file_name = f"{folder_path}/{username}_questionaire_data_{timestamp}.txt"
    data_for_email_body = ''
    with open(file_name, "w") as file:
        for question, answer in responses.items():
            file.write(f"{question}: {answer}\n")
            data_for_email_body += f"{question}: {answer}\n"
    email_subject = f"Travel Plan Creator - {username}'s Questionnaire Response"
    email_body = f"Hey {username},\n\nThank you for submitting your questionnaire response. We'll curate your travel plan and reach out to you on your registered email shortly.\n\n Attaching a copy of your response., \n\n {data_for_email_body}\n\nRegards,\nTravel Plan Creator Team"
    send_email(st.session_state['user_email'], email_subject, email_body)

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
        st.success("Response saved. We'll curate your travel plan and reach out to you on your registered email shortly. We have sent a copy of your response to your registered email.")


# Main function of the Streamlit app
def main():
    st.sidebar.title("Travel Plan Creator")
    if not st.session_state.get('login_status', False):
        choice = st.sidebar.selectbox("Choose Action", ["Signup", "Login"])
        if choice == "Login":
            login_page()
        elif choice == "Signup":
            signup_page()
    else:
        # Display the user questionnaire if logged in
        user_questionnaire(st.session_state['username'])

if __name__ == "__main__":
    main()
