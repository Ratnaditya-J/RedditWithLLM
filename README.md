# RedditWithLLM

A secure application that connects your Reddit account to ChatGPT, allowing you to ask AI questions about your Reddit activity, posts, comments, and engagement patterns.

## 🎯 What It Does

**RedditWithLLM** lets you:
1. **Securely connect** your Reddit account (runtime credentials only)
2. **Connect to ChatGPT** with your OpenAI API key
3. **Ask ChatGPT questions** about your Reddit account data
4. **Get AI insights** about your posting patterns, community engagement, and content performance
5. **Receive personalized suggestions** for improving your Reddit experience

## ✨ Key Features

- **🔐 Secure Runtime Credentials**: No storage of Reddit auth or API keys on disk
- **📊 Comprehensive Reddit Analysis**: Posts, comments, karma, subreddit activity
- **🤖 ChatGPT Integration**: Ask natural language questions about your Reddit data
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

1. **Reddit API Credentials**:
   - Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
   - Create a new application
   - Note down your `client_id`, `client_secret`, `username`, and `password`

2. **LLM API Key**:
   - Obtain an API key from your preferred LLM provider (OpenAI, Anthropic, etc.)

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd RedditWithLLM

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp config.example.json config.json
# Edit config.json with your credentials
```

### Configuration

The application requires two sets of credentials:

1. **Reddit Authentication**:
   - Client ID
   - Client Secret
   - Username
   - Password

2. **LLM API Key**:
   - API Key for your chosen LLM provider

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
