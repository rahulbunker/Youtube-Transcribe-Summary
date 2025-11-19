# YouTube Transcript & Summarization App

## 📖 Project Storytelling

This project is a web application that extracts YouTube video transcripts and generates summaries using Google's Gemini LLM.  
It simplifies the process of understanding video content by converting long videos into concise summaries or detailed key points.

---

## 🎯 Objective
The main goals of this project are:
- Automatically fetch YouTube video transcripts in multiple languages.
- Summarize content into concise, detailed, or key-point summaries.
- Provide a fast, reliable API for transcript retrieval and summarization.

---

## 📂 Dataset & Input
- **Input**: YouTube video URL
- **Languages Supported**: English, Hindi (auto-translation when needed)
- **Output**: Full transcript and/or summary (concise, detailed, key points)

---

## 🔍 Key Functionalities
### 1. Transcript Extraction
- Extracts YouTube video ID from any valid URL format.  
- Fetches transcripts even in cases where multiple languages are available.  
- Handles exceptions like disabled transcripts or unavailable content.

### 2. Summarization with Gemini
- Uses **Google Gemini LLM** to generate:
  - **Concise summaries** (3-5 sentences)  
  - **Detailed bullet summaries**  
  - **Key points extraction**  
- Efficient handling of large transcripts by truncating excessive text to 10,000 characters.

### 3. Combined API
- Single endpoint to fetch transcript **and** summary simultaneously.  
- Returns structured JSON with success status, video ID, transcript, and summary.

---

## 📈 Key Insights & Features
- Provides **multi-language support** (English & Hindi).  
- Intelligent **error handling** for unavailable or blocked transcripts.  
- Supports multiple summary types for flexible usage.  
- Built as a **Flask web app** with REST API endpoints for easy integration.  

---

## 🧩 Business & Technical Insights
- **Efficiency**: Automates content summarization for educational, business, or research purposes.  
- **Scalability**: Can be extended to batch process multiple videos.  
- **Flexibility**: Users can choose summary type according to their needs.  

---

## ✅ Conclusion
This project transforms long-form video content into easily digestible summaries, saving time and improving content accessibility.

---

## 🚀 Next Steps
- Integrate **frontend dashboard** for live video URL input.  
- Add support for **more languages**.  
- Implement **user authentication** for personalized summarization history.  

---

## 🛠️ Tools & Libraries Used
- **Python**  
- **Flask**  
- **Google Gemini API**  
- **YouTube Transcript API**  
- **Regex**  
- **Dotenv for API Key Management**  

---

📌 This app provides an end-to-end solution for extracting, translating, and summarizing YouTube video content using state-of-the-art AI models.
