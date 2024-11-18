# 🚖 Ride-Hailing-App- 

Welcome to the backend service for the Ride-Hailing App, a platform that enables users to book rides, manage profiles, view ride history, and more. Built using **FastAPI**, this service provides RESTful APIs to support client-side applications.  

## 🚀 Features  
- User authentication (login and signup).  
- Profile management (edit user details).  
- Ride booking and cancellation.  
- Ride history management.  
- API documentation powered by FastAPI's built-in Swagger and ReDoc.  

## 🛠️ Tech Stack  
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)  
- **Database**: PostgreSQL  
- **Hosting**: [Railway](https://railway.app/)  
- **HTTP Clients**: `httpx`, `requests`  
- **Environment Management**: Python `venv`  

## 📖 API Endpoints  

### Authentication  
- **Login**: `/login` [POST]  
  Authenticate users using their phone number.  
- **Signup**: `/signup` [POST]  
  Register new users with their details.  

### User Profile  
- **Edit Profile**: `/profile/{user_id}` [PUT]  
  Update user details like name and emergency contact.  

### Ride Management  
- **Book a Ride**: `/rides/book` [POST]  
  Book a ride by specifying pickup and destination details.  
- **Cancel a Ride**: `/rides/cancel/{ride_id}` [DELETE]  
  Cancel a booked ride using its ID.  

### Ride History  
- **Get Ride History**: `/rides/history` [GET]  
  Fetch the user's ride history.  

## 🔧 Installation  

1. **Clone the repository**:  
   ```bash  
   git clone https://github.com/your-username/ride-hailing-app-backend.git  
   cd ride-hailing-app-backend

2. **Create a virtual environment**:
  ```bash
  python -m venv venv  
  source venv/bin/activate
  On Windows: venv\Scripts\activate

3. Set up the environment variables:
   ```bash
 DATABASE_URL=your_postgresql_database_url
 LOGIN_URL=http://127.0.0.1:5000/login  
 SIGNUP_URL=http://127.0.0.1:5000/signup  
 SECRET_KEY=your_secret_key  


4. Run the application:
```bash
  uvicorn main:app --host 0.0.0.0 --port 8000 --reload

5. Access the API documentation:
  Open your browser and navigate to
  
  Swagger UI: http://127.0.0.1:8000/docs
  ReDoc: http://127.0.0.1:8000/redoc

## 🌐 Deployment on Railway

6. Create a Railway Project:

- Log in to Railway and create a new project.
Connect the repository:

- Link your GitHub repository to the Railway project.
Add environment variables:

- In the Railway dashboard, go to the "Variables" section and add the required environment variables (DATABASE_URL, SECRET_KEY, etc.).
Deploy the application:

- Railway automatically detects the main.py file and deploys the FastAPI app.
Access the hosted application:

- Railway will provide a public URL for your app. Use it to access your APIs.

## 🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
- Create a new branch: git checkout -b feature/your-feature-name.
- Commit your changes: git commit -m 'Add some feature'.
- Push to the branch: git push origin feature/your-feature-name.
- Open a pull request.


## 🙌 Acknowledgments
Thanks to the creators of FastAPI for such an excellent framework.
Special thanks to Railway for simplifying deployment processes.
