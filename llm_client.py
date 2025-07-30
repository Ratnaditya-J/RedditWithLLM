"""
LLM API client for RedditWithLLM.
Handles secure connection to ChatGPT/OpenAI and query processing.
"""

import openai
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json


@dataclass
class LLMResponse:
    """Container for LLM response data."""
    response_text: str
    tokens_used: int
    model_used: str
    success: bool
    error_message: Optional[str] = None


class LLMClient:
    """Secure LLM API client for ChatGPT integration."""
    
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo", max_tokens: int = 1000, temperature: float = 0.7):
        """Initialize LLM client with API credentials."""
        # Initialize OpenAI client (for openai>=1.0.0)
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        
    def test_connection(self) -> bool:
        """Test ChatGPT API connection."""
        try:
            # Simple test query using new OpenAI 1.0.0+ API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return response.choices[0].message.content is not None
        except Exception as e:
            print(f"❌ ChatGPT connection failed: {e}")
            return False
    
    def query_about_reddit_data(self, reddit_summary: str, user_question: str) -> LLMResponse:
        """
        Query ChatGPT about user's Reddit data.
        
        Args:
            reddit_summary: Formatted summary of user's Reddit data
            user_question: User's question about their Reddit account
            
        Returns:
            LLMResponse: ChatGPT's response with metadata
        """
        try:
            # Construct system prompt for Reddit analysis
            system_prompt = """You are a helpful assistant that analyzes Reddit account data. 
You have been provided with a user's Reddit account summary including their posts, comments, 
karma, active subreddits, and other account information. 

Please answer the user's questions about their Reddit account based on this data. 
Be specific, helpful, and provide insights when possible. If the data doesn't contain 
enough information to answer a question, say so clearly.

Keep responses conversational and engaging while being accurate to the provided data."""

            # Construct user message with Reddit data and question
            user_message = f"""Here is my Reddit account data:

{reddit_summary}

My question: {user_question}"""

            # Make API call to ChatGPT using new OpenAI 1.0.0+ API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            
            # Extract response data
            response_text = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            return LLMResponse(
                response_text=response_text,
                tokens_used=tokens_used,
                model_used=self.model,
                success=True
            )
            
        except Exception as e:
            return LLMResponse(
                response_text="",
                tokens_used=0,
                model_used=self.model,
                success=False,
                error_message=str(e)
            )
    
    def analyze_reddit_patterns(self, reddit_summary: str) -> LLMResponse:
        """
        Get ChatGPT analysis of user's Reddit patterns and insights.
        
        Args:
            reddit_summary: Formatted summary of user's Reddit data
            
        Returns:
            LLMResponse: ChatGPT's analysis with insights
        """
        analysis_prompt = """Based on this Reddit account data, please provide insights about:

1. **Posting Patterns**: What topics does this user typically post about?
2. **Community Engagement**: Which communities are they most active in and why?
3. **Content Style**: What's their commenting/posting style?
4. **Interests**: What are their main interests based on their activity?
5. **Engagement Quality**: How well do their posts and comments perform?

Please be specific and provide actionable insights where possible."""

        return self.query_about_reddit_data(reddit_summary, analysis_prompt)
    
    def suggest_improvements(self, reddit_summary: str) -> LLMResponse:
        """
        Get ChatGPT suggestions for improving Reddit engagement.
        
        Args:
            reddit_summary: Formatted summary of user's Reddit data
            
        Returns:
            LLMResponse: ChatGPT's suggestions for improvement
        """
        improvement_prompt = """Based on my Reddit activity data, please suggest ways I could:

1. **Improve Engagement**: How can I get better responses to my posts and comments?
2. **Discover Communities**: What new subreddits might I enjoy based on my interests?
3. **Content Strategy**: How can I create more valuable content?
4. **Community Participation**: How can I be a better community member?
5. **Growth Opportunities**: How can I grow my karma and positive impact?

Please provide specific, actionable advice based on my actual Reddit data."""

        return self.query_about_reddit_data(reddit_summary, improvement_prompt)
    
    def compare_subreddits(self, reddit_summary: str, subreddit1: str, subreddit2: str) -> LLMResponse:
        """
        Compare user's activity in two different subreddits.
        
        Args:
            reddit_summary: Formatted summary of user's Reddit data
            subreddit1: First subreddit to compare
            subreddit2: Second subreddit to compare
            
        Returns:
            LLMResponse: ChatGPT's comparison analysis
        """
        comparison_prompt = f"""Based on my Reddit activity data, please compare my participation in r/{subreddit1} vs r/{subreddit2}:

1. **Activity Level**: How active am I in each community?
2. **Content Type**: What kind of content do I post/comment in each?
3. **Engagement**: How well do my contributions perform in each?
4. **Community Fit**: Which community seems to be a better fit for me and why?
5. **Recommendations**: How can I improve my participation in each community?

If I haven't been active in one or both of these subreddits, please let me know and suggest similar communities I am active in."""

        return self.query_about_reddit_data(reddit_summary, comparison_prompt)
    
    def get_content_suggestions(self, reddit_summary: str, subreddit: str) -> LLMResponse:
        """
        Get content suggestions for a specific subreddit based on user's interests.
        
        Args:
            reddit_summary: Formatted summary of user's Reddit data
            subreddit: Target subreddit for content suggestions
            
        Returns:
            LLMResponse: ChatGPT's content suggestions
        """
        content_prompt = f"""Based on my Reddit activity and interests, please suggest content ideas for r/{subreddit}:

1. **Post Ideas**: What kind of posts would be valuable for this community and align with my interests?
2. **Discussion Topics**: What discussions could I start that would engage the community?
3. **Content Format**: What format (text, link, image, etc.) works best for my style and this subreddit?
4. **Timing**: Based on my activity patterns, when might be the best time to post?
5. **Engagement Strategy**: How can I encourage meaningful discussions?

Please base suggestions on my actual interests and past successful content."""

        return self.query_about_reddit_data(reddit_summary, content_prompt)
