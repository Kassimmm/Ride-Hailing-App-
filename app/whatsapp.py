from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os
import requests
import httpx
import random
import asyncio  # Add asyncio for event loop management

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Environment variables for mock endpoints
LOGIN_URL = os.getenv('LOGIN_URL', 'http://127.0.0.1:5000/login')
SIGNUP_URL = os.getenv('SIGNUP_URL', 'http://127.0.0.1:5000/signup')
EDIT_PROFILE_URL = os.getenv('EDIT_PROFILE_URL', 'http://127.0.0.1:5000/edit')


# In-memory session storage
user_sessions = {}

# Menu options
MENU = """
✨ *Main Menu* ✨
1️⃣ Edit Profile
2️⃣ Book a Ride 🚖
3️⃣ View Ride History 📜
4️⃣ Cancel a Ride ❌
"""

# Menu for ride options
RIDE_TYPES = {
    "1": "Economy",
    "2": "Premium",
    "3": "Luxury"
}

DRIVER_NAMES = ["John Doe", "Jane Smith", "Alex Carter"]
CAR_MODELS = ["Toyota Corolla", "Honda Civic", "Tesla Model 3"]
CAR_LICENSE_PLATES = ["ABC-123", "XYZ-789", "LMN-456"]

# Simulate random fare and ETA
def generate_random_fare_and_eta():
    fare = round(random.uniform(10.0, 50.0), 2)
    eta = random.randint(5, 15)
    return fare, eta



def login_user(phone_number):
    """Attempt to log in the user."""
    try:
        response = requests.post(LOGIN_URL, params={"phone_number": phone_number}, timeout=10.0)
        if response.status_code == 200:
            return {"success": True, "message": "🎉 Login successful!", "id": response.json().get("id")}
        elif response.status_code == 422:
            return {"success": False, "message": "❌ Login failed: Unprocessable Entity. Check input data."}
        else:
            return {"success": False, "message": f"❌ Login failed with unexpected status: {response.status_code}"}
    except requests.RequestException as e:
        return {"success": False, "message": f"❌ An error occurred during the login request: {e}"}

async def signup_user(phone_number, name, emergency_contact):
    """Attempt to sign up the user asynchronously."""
    payload = {
        "name": name,
        "role": "user",  # Default role
        "phone_number": phone_number,
        "emergency_contact": emergency_contact,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(SIGNUP_URL, json=payload, timeout=10.0)
            if response.status_code == 200:
                return {"success": True, "message": "✅ Signup successful!"}
            else:
                return {"success": False, "message": f"❌ Signup failed with status: {response.status_code}"}
        except httpx.RequestError as e:
            return {"success": False, "message": f"❌ An error occurred during the signup request: {e}"}

def edit_user_profile(user_id, updated_details):
    """
    Edit the user's profile by first retrieving their user ID using the phone number.

    Args:
        phone_number (str): The phone number of the user.
        updated_details (dict): The updated profile details.

    Returns:
        dict: A dictionary containing the success status and message.
    """
    try:
        if not user_id:
            return {"success": False, "message": "❌ User ID not found for the provided phone number."}

        # Step 2: Update the user's profile using their ID
        edit_profile_url = f"http://127.0.0.1:5000/profile/{user_id}"  # Base URL for profile updates
        response = requests.put(edit_profile_url, json=updated_details, timeout=10.0)

        if response.status_code == 200:
            return {"success": True, "message": "✅ Profile updated successfully!"}
        else:
            return {"success": False, "message": f"❌ Update failed with status: {response.status_code}"}
    except requests.RequestException as e:
        return {"success": False, "message": f"❌ An error occurred during the update request: {e}"}



@app.route("/whatsapp", methods=['POST'])
def whatsapp_webhook():
    incoming_msg = request.values.get("Body", "").strip()
    user_phone = request.values.get("WaId", None)  # User's WhatsApp phone number
    response = MessagingResponse()

    # Initialize user session if not found
    if user_phone not in user_sessions:
        user_sessions[user_phone] = {"stage": "name_collection", "authenticated": False}
        response.message("👋 Hi there! Welcome to *Ride-Hailing App*! 🚗💨\nWhat's your *name*? 😊")
        return str(response)

    # Get user session data
    user_data = user_sessions[user_phone]
    stage = user_data["stage"]

    # Handle stages
    if stage == "name_collection":
        user_data["name"] = incoming_msg
        user_data["stage"] = "emergency_contact"
        response.message(f"Awesome, {user_data['name']}! 🌟\nPlease share an *emergency contact number*. 📞")
    elif stage == "emergency_contact":
        user_data["emergency_contact"] = incoming_msg
        user_data["stage"] = "phone_authentication"
        response.message("🔑 Authenticating your phone number... Please wait a moment! ⏳")

        # Attempt login
        login_result = login_user(user_phone)
        if login_result["success"]:
            user_data["id"] = login_result["id"]
            user_data["authenticated"] = True
            user_data["stage"] = "menu"
            response.message(f"{login_result['message']}\n{MENU}")
        else:
            response.message(f"{login_result['message']}\n⚠️ Trying to create your account... Please wait!")

            # Attempt signup asynchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            signup_result = loop.run_until_complete(
                signup_user(user_phone, user_data["name"], user_data["emergency_contact"])
            )
            if signup_result["success"]:
                user_data["authenticated"] = True
                user_data["stage"] = "menu"
                response.message(f"{signup_result['message']}\n{MENU}")
            else:
                response.message(f"{signup_result['message']}")

    elif stage == "menu":
        if not user_data["authenticated"]:
            response.message("🚫 You need to log in first. Please restart the conversation.")
        elif incoming_msg == "1":
            user_data["stage"] = "edit_profile_details"
            response.message("✏️ *Edit Profile*: Please send your updated details.")
        elif incoming_msg == "2":
            user_data["stage"] = "ride_start"
            response.message("🚗 Welcome to Ride Booking Service!\nShare your *current location* to begin. 📍")
        elif incoming_msg == "3":
            response.message("📜 *View Ride History*: We'll fetch your ride history shortly!")
        elif incoming_msg == "4":
            response.message("❌ *Cancel a Ride*: Please provide the ride ID to cancel.")
        else:
            response.message(f"❓ Invalid input. Please select an option from the menu below:\n{MENU}")

    elif stage == "edit_profile_details":
        # Parse updated details
        try:
            details = dict(item.strip().split(": ") for item in incoming_msg.split(", "))
            updated_details = {
                "name": details.get("Name"),
                "emergency_contact": details.get("Emergency Contact")
            }
            # Call the edit profile function
            edit_result = edit_user_profile(user_data["id"], updated_details)
            if edit_result["success"]:
                user_data["stage"] = "menu"
                response.message(f"{edit_result['message']}\n{MENU}")
            else:
                response.message(f"{edit_result['message']}\n⚠️ Please try again or contact support.")
        except Exception as e:
            response.message(f"❌ Invalid input format. Please send your details as:\n"
                         "`Name: [Your Name], Emergency Contact: [Your Emergency Contact]`")

    elif stage == "ride_start":
        # Save current location and ask for destination
        user_data["current_location"] = incoming_msg
        user_data["stage"] = "destination"
        response.message("📍 Got your current location!\nNow share your *destination* location. 🗺️")
    elif stage == "destination":
        # Save destination and prompt for ride type
        user_data["destination"] = incoming_msg
        user_data["stage"] = "ride_type"
        response.message(
            "🛻 Destination saved! Select a ride type:\n1️⃣ Economy\n2️⃣ Premium\n3️⃣ Luxury\n"
            "Reply with the corresponding number."
        )
    elif stage == "ride_type":
        # Save ride type and simulate driver matching
        ride_type = RIDE_TYPES.get(incoming_msg)
        if not ride_type:
            response.message("❌ Invalid selection. Please reply with 1, 2, or 3.")
        else:
            user_data["ride_type"] = ride_type
            driver = random.choice(DRIVER_NAMES)
            car = random.choice(CAR_MODELS)
            license_plate = random.choice(CAR_LICENSE_PLATES)
            fare, eta = generate_random_fare_and_eta()

            user_data.update({
                "driver": driver,
                "car": car,
                "license_plate": license_plate,
                "fare": fare,
                "eta": eta,
                "stage": "ride_confirm"
            })

            response.message(
                f"🎉 Your {ride_type} ride is matched!\n🚘 *Driver*: {driver}\n🚗 *Car*: {car} ({license_plate})\n"
                f"⏳ *ETA*: {eta} minutes\n💵 *Estimated Fare*: ${fare}\n\n"
                "Reply *CONFIRM* to book this ride or *CANCEL* to start over."
            )
    elif stage == "ride_confirm":
        if incoming_msg.lower() == "confirm":
            response.message(
                "✅ Your ride is confirmed!\n🚘 Driver is on the way.\n"
                "We'll keep you updated with the status."
            )
            user_data["stage"] = "ride_in_progress"
        elif incoming_msg.lower() == "cancel":
            user_data["stage"] = "ride_start"
            response.message("🚫 Ride canceled. Share your *current location* to start again.")
        else:
            response.message("❌ Invalid input. Reply *CONFIRM* to book or *CANCEL* to restart.")
    elif stage == "ride_in_progress":
        # Simulate ride status updates
        response.message(
            "🚗 Status Update: Your driver is almost there!\n"
            "We'll notify you once the driver arrives. Enjoy your ride!"
        )

    else:
        response.message("⚠️ Something went wrong. Please restart the conversation.")

    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=8000)
