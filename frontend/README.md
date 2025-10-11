# Study Buddy Frontend

A modern React frontend for the Study Buddy AI-powered learning platform.

## 🚀 Features

- **🔐 Authentication**: Secure login/register with JWT tokens
- **📤 Document Upload**: Drag & drop file upload (PDF, DOCX, TXT)
- **🤖 AI Summarization**: Automatic document summaries with different lengths
- **🧠 Quiz Generator**: AI-powered quiz creation from document content
- **💬 AI Chat**: Interactive chat with AI about your documents
- **📊 Dashboard**: Comprehensive overview of your learning progress
- **📱 Responsive Design**: Works perfectly on desktop and mobile

## 🛠️ Tech Stack

- **React 18** - Modern React with hooks
- **Vite** - Fast build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **React Hot Toast** - Beautiful notifications
- **Lucide React** - Beautiful icons
- **Framer Motion** - Smooth animations

## 📦 Installation

1. **Install dependencies:**
   ```bash
   cd frontend
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

## 🔧 Configuration

The frontend is configured to proxy API requests to the backend running on `http://localhost:5050`. Make sure your backend is running before starting the frontend.

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── auth/           # Authentication components
│   │   ├── chat/           # AI chat components
│   │   ├── dashboard/      # Dashboard components
│   │   ├── documents/      # Document management
│   │   ├── layout/         # Layout components (Navbar, etc.)
│   │   ├── quiz/           # Quiz components
│   │   └── ai/             # AI features (summaries)
│   ├── contexts/           # React contexts (Auth)
│   ├── services/           # API services
│   ├── App.jsx            # Main app component
│   ├── main.jsx           # App entry point
│   └── index.css          # Global styles
├── public/                # Static assets
├── package.json           # Dependencies
├── vite.config.js         # Vite configuration
├── tailwind.config.js     # TailwindCSS configuration
└── README.md             # This file
```

## 🎨 Design System

### Colors
- **Primary**: Blue tones for main actions
- **Secondary**: Green tones for success states
- **Gray**: Neutral colors for text and backgrounds

### Components
- **Cards**: Consistent card design with shadows
- **Buttons**: Primary, secondary, and success variants
- **Forms**: Styled input fields with focus states
- **Navigation**: Responsive navbar with mobile menu

## 🔐 Authentication Flow

1. **Login/Register**: Users authenticate with email/password
2. **JWT Tokens**: Access and refresh tokens stored securely
3. **Protected Routes**: Automatic redirect to login if not authenticated
4. **Token Refresh**: Automatic token renewal when expired

## 📤 Document Upload

- **Supported Formats**: PDF, DOCX, TXT
- **File Size Limit**: 10MB
- **Drag & Drop**: Intuitive file upload interface
- **Progress Tracking**: Real-time upload status

## 🤖 AI Features

### Summarization
- **Multiple Lengths**: Short, medium, long summaries
- **Copy to Clipboard**: Easy sharing of summaries
- **Statistics**: Word count, reading time, etc.

### Quiz Generation
- **Question Types**: Multiple choice and open-ended
- **Progress Tracking**: Step-by-step quiz navigation
- **Results**: Score calculation and performance feedback

### AI Chat
- **Document Context**: Chat about specific documents
- **Suggested Questions**: Pre-built conversation starters
- **Real-time**: Smooth chat interface with typing indicators

## 📱 Responsive Design

The app is fully responsive and works on:
- **Desktop**: Full-featured experience
- **Tablet**: Optimized layout for medium screens
- **Mobile**: Touch-friendly interface with mobile menu

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

### Preview Production Build
```bash
npm run preview
```

### Deploy to Vercel/Netlify
The app can be easily deployed to modern hosting platforms:
- **Vercel**: Connect your GitHub repo
- **Netlify**: Drag & drop the `dist` folder
- **AWS S3**: Upload the built files

## 🔧 Development

### Available Scripts
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Code Style
- **ESLint**: Configured for React best practices
- **Prettier**: Automatic code formatting
- **TailwindCSS**: Utility-first styling approach

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues:
1. Check the browser console for errors
2. Ensure the backend is running on port 5050
3. Verify your JWT tokens are valid
4. Check network connectivity

---

**Happy Learning with Study Buddy! 🎓✨**
