# RedditWithLLM

## 💡 Why I Built This

Recently I was looking for an easy way to ask ChatGPT questions about my Reddit account. I was interested in extracting the key info from my saved posts about a place and the food recommendations (that I saved across multiple posts in the past). Turns out that most other tools have a direct integration but not Reddit. I created this tool to help exactly with that.

## 🚀 What It Does

A secure application that connects your Reddit account to ChatGPT, allowing you to ask AI questions about your Reddit activity, posts, comments, saved content, and engagement patterns.

**RedditWithLLM** lets you:
1. **Securely connect** your Reddit account (runtime credentials only)
2. **Connect to ChatGPT** with your OpenAI API key
3. **Ask ChatGPT questions** about your Reddit account data
4. **Analyze your saved posts** with their comments and replies
5. **Extract recommendations** from saved discussions (like food places, travel tips, etc.)
6. **Get AI insights** about your posting patterns, community engagement, and content performance
7. **Receive personalized suggestions** for improving your Reddit experience

## ✨ Key Features

- **🔐 Secure Runtime Credentials**: No storage of Reddit auth or API keys on disk
- **📚 Enhanced Saved Posts Analysis**: Fetch your saved posts WITH their comments and replies
- **🍽️ Extract Recommendations**: Perfect for finding food places, travel tips, product reviews from saved discussions
- **📊 Comprehensive Reddit Analysis**: Posts, comments, karma, subreddit activity
- **🤖 ChatGPT Integration**: Ask natural language questions about your Reddit data
- **🔍 Deep Content Search**: Search through posts, comments, AND saved post discussions
- **💡 AI Insights**: Get patterns analysis and improvement suggestions
- **🎯 Interactive Interface**: User-friendly command-line experience
- **📈 Subreddit Comparisons**: Compare your activity across different communities
- **💬 Content Suggestions**: Get AI-powered content ideas for specific subreddits

## 🔒 Security Guarantee

**Your credentials are NEVER stored on disk**:
- Reddit credentials collected via secure runtime prompts
- ChatGPT API key entered securely (hidden input)
- All credentials stored only in memory during execution
- Automatic credential cleanup when application exits
- No config files, no persistence, no credential leakage

## Setup

### Prerequisites

1. **Reddit API Credentials** (Step-by-step guide):

   **Step 1: Go to Reddit App Preferences**
   - Visit [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps)
   - Log in to your Reddit account if not already logged in

   **Step 2: Create a New Application**
   - Click "Create App" or "Create Another App" button
   - Fill out the form:
     - **Name**: Choose any name (e.g., "RedditWithLLM")
     - **App type**: Select **"script"** (this is important!)
     - **Description**: Optional (e.g., "Personal Reddit data analysis")
     - **About URL**: Leave blank or add any URL
     - **Redirect URI**: Enter `http://localhost:8080` (required but not used)
   - Click "Create app"

   **Step 3: Extract Your Credentials**
   After creating the app, you'll see your app details. Note down these values:
   - **Client ID**: The string under your app name (looks like: `abcdef123456`)
   - **Client Secret**: The "secret" field (looks like: `xyz789secretstring`)
   - **Username**: Your Reddit username
   - **Password**: Your Reddit account password

   **⚠️ Important Notes:**
   - Keep these credentials secure and never share them
   - The app type MUST be "script" for this tool to work
   - You'll enter these credentials when you run the application (they're never stored)

2. **OpenAI API Key** (for ChatGPT):

   **Step 1: Get OpenAI API Key**
   - Visit [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Log in to your OpenAI account (create one if needed)
   - Click "Create new secret key"
   - Copy the API key (starts with `sk-`)
   - **Important**: You'll need billing set up on your OpenAI account

### Installation

```bash
# Clone the repository
git clone https://github.com/Ratnaditya-J/RedditWithLLM.git
cd RedditWithLLM

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### How It Works

**🔒 Secure Runtime Credential Collection:**
When you run the application, it will securely prompt you for:

1. **Reddit Credentials** (from the app you created above):
   - Client ID
   - Client Secret  
   - Username
   - Password (hidden input)

2. **OpenAI API Key** (from the setup above):
   - Your OpenAI API key (starts with `sk-`)
   - Hidden input for security

**✅ What Happens Next:**
- Application connects to Reddit API and fetches your data
- Your data is analyzed and summarized
- You can ask ChatGPT questions about your Reddit account
- All credentials are cleared from memory when you exit

**🔐 Security Promise:**
- No credentials are ever written to files
- No config files created or modified
- Everything stays in memory only
- Automatic cleanup on exit

## Usage

```bash
python main.py
```

## Security

- Never commit your `config.json` file
- Keep your API keys secure
- Use environment variables in production

## License

MIT License
