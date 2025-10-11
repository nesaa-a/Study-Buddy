# Study Buddy Frontend Setup Guide

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Start Development Server
```bash
npm run dev
```

### 3. Open Browser
Navigate to `http://localhost:3000`

## 🔧 Prerequisites

- **Node.js** (v16 or higher)
- **npm** or **yarn**
- **Backend running** on `http://localhost:5050`

## 📋 Features Implemented

### ✅ Authentication System
- **Login/Register** with JWT tokens
- **Protected routes** with automatic redirects
- **Token refresh** mechanism
- **User profile** management

### ✅ Document Management
- **File upload** with drag & drop
- **Supported formats**: PDF, DOCX, TXT
- **File validation** and size limits
- **Document list** with metadata

### ✅ AI Features
- **Document summarization** with multiple lengths
- **Quiz generation** from document content
- **AI chat** interface (mock responses)
- **Copy to clipboard** functionality

### ✅ User Interface
- **Responsive design** for all devices
- **Modern UI** with TailwindCSS
- **Smooth animations** and transitions
- **Loading states** and error handling

### ✅ Navigation & Layout
- **Tabbed dashboard** with multiple views
- **Responsive navbar** with mobile menu
- **Protected routes** and authentication
- **User profile** dropdown

## 🎨 Design Features

- **Color Scheme**: Primary blue, secondary green, neutral grays
- **Typography**: Clean, readable fonts with proper hierarchy
- **Icons**: Lucide React icons throughout
- **Animations**: Framer Motion for smooth transitions
- **Responsive**: Mobile-first design approach

## 🔐 Security Features

- **JWT Authentication** with access/refresh tokens
- **Automatic token refresh** on expiration
- **Protected routes** with authentication checks
- **Secure API calls** with proper headers
- **Input validation** and sanitization

## 📱 Mobile Support

- **Responsive breakpoints** for all screen sizes
- **Touch-friendly** interface elements
- **Mobile navigation** with hamburger menu
- **Optimized layouts** for small screens

## 🚀 Production Ready

The frontend is production-ready with:
- **Optimized builds** with Vite
- **Code splitting** for better performance
- **Error boundaries** for graceful error handling
- **Loading states** for better UX
- **SEO-friendly** structure

## 🔄 API Integration

The frontend integrates with your backend API:
- **Authentication endpoints** (`/api/auth/*`)
- **Document endpoints** (`/api/documents/*`)
- **Quiz endpoints** (`/api/quiz/*`)
- **User endpoints** (`/api/users/*`)

## 🎯 Next Steps

1. **Start the backend** server on port 5050
2. **Run the frontend** with `npm run dev`
3. **Register a new account** or login
4. **Upload a document** to test the features
5. **Generate summaries** and quizzes
6. **Chat with AI** (mock responses for now)

## 🐛 Troubleshooting

### Common Issues:

1. **CORS Errors**: Ensure backend has CORS enabled
2. **API Connection**: Check if backend is running on port 5050
3. **JWT Errors**: Verify JWT_SECRET_KEY is set in backend
4. **File Upload**: Check file size and format restrictions

### Debug Mode:
- Open browser DevTools
- Check Console for errors
- Verify Network requests
- Check Local Storage for tokens

## 📞 Support

If you encounter issues:
1. Check the browser console
2. Verify backend connectivity
3. Ensure all dependencies are installed
4. Check the README.md for detailed instructions

---

**Your Study Buddy frontend is ready to go! 🎓✨**
