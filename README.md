# NewsletterStack

## Project Description
NewsletterStack is a powerful web application designed to help users create, manage, and distribute newsletters efficiently. The application allows users to customize templates, manage subscriber lists, and analyze engagement metrics, making it an essential tool for marketers, businesses, and content creators.

## Features
- **User Authentication**: Secure login and registration system.
- **Customizable Templates**: A range of templates to choose from for different types of newsletters.
- **Subscriber Management**: Easily add, remove, and manage subscriber lists.
- **Analytics Dashboard**: View engagement metrics and performance analytics of sent newsletters.
- **API Integration**: Connect with third-party services for added functionality.

## Tech Stack
- **Frontend**: React.js, Redux, Tailwind CSS
- **Backend**: Node.js, Express.js
- **Database**: MongoDB
- **Deployment**: Heroku
- **Testing**: Jest, Cypress

## Project Structure
```
NewsletterStack/
├── client/         # Frontend application
│   ├── src/        # Source files
│   ├── public/     # Public assets
│   └── ...
├── server/         # Backend application
│   ├── models/     # Database models
│   ├── routes/     # API routes
│   └── ...
└── README.md      # Project documentation
```

## API Endpoints
- `POST /api/auth/register`: User registration.
- `POST /api/auth/login`: User login.
- `GET /api/newsletters`: Retrieve all newsletters.
- `POST /api/newsletters`: Create a new newsletter.
- `GET /api/newsletters/:id`: Get a specific newsletter by ID.
- `DELETE /api/newsletters/:id`: Delete a newsletter by ID.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/JoanneKoshy/NewsletterStack.git
   ```
2. Navigate to the server directory and install dependencies:
   ```bash
   cd server
   npm install
   ```
3. Navigate to the client directory and install dependencies:
   ```bash
   cd client
   npm install
   ```
4. Start the server:
   ```bash
   cd server
   npm start
   ```
5. Start the client:
   ```bash
   cd client
   npm start
   ```

## Design Decisions
- Chose React for the frontend to create a responsive and dynamic user interface.
- Node.js and Express were selected for the backend to handle asynchronous operations and simplify API routing.
- MongoDB was picked for its flexibility in handling different data structures efficiently.

## Known Limitations
- The application currently does not support internationalization.
- Email verification for new users is not implemented yet.

## Planned Improvements
- Implement email verification and password recovery features.
- Introduce additional analytics features, like A/B testing and segmentation.
- Enhance UI with more customization options for newsletter templates.

---

This README serves as a guide for users and developers to understand and contribute to the NewsletterStack project.