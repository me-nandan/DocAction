What is DocAction?
DocAction is an AI-powered, image-based document assistant that analyzes document images, extracts important information, deadlines, and required actions, and generates a simple summary. The summary can then be sent directly to the user’s Telegram for easy access.

✨ Features

* 📷 Upload images
* 🤖 AI-powered image analysis
* 📝 Generate simple summaries
* 🔍 Extract important information
* 📅 Identify deadlines
* ✅ Identify required actions
* 📲 Send summaries directly to Telegram

🛠️ Technologies Used

* Python
* Streamlit
* Google Gemini AI
* Telegram Bot API

⚙️ How It Works

1. Upload a document image to DocAction.
2. Analyze the image using Google Gemini AI.
3. Extract important information, deadlines, and actions.
4. Generate a simple and clear summary.
5. Send the summary directly to the user’s Telegram.

🚀 Setup Instructions

  1. Clone the Repository
  
     git clone https://github.com/me-nandan/DocAction.git
     cd DocAction
  
  
  2. Create a Virtual Environment
  
     python -m venv venv
  
     Windows:
     venv\Scripts\activate
  
  
  3. Install Dependencies
  
     pip install -r requirements.txt
  
  
  4. Configure API Keys
  
     Create the following file:
  
     .streamlit/secrets.toml
  
     Add your API keys:
  
     GEMINI_API_KEY = "your-gemini-api-key"
     TELEGRAM_BOT_TOKEN = "your-telegram-bot-token"
  
     Replace the placeholder values with your actual API keys.
  
  
  5. Run the Application
  
     streamlit run app.py
  
     The application will open in your web browser.
  
  
  6. Connect Telegram
  
     1. Open @DocActionAIBot on Telegram.
     2. Press Start.
     3. Open @userinfobot on Telegram.
     4. Press Start and copy your Telegram Chat ID.
     5. Enter your name and Telegram Chat ID in DocAction.
     6. Upload a document and analyze it.
     7. Click "Send to Telegram" to receive the summary.
  
  ⚠️ Security
  
   Keep your API keys and other sensitive credentials private.
   Never upload API keys, passwords, or secret credentials to GitHub.

   Make sure sensitive configuration files are included in your .gitignore file.
