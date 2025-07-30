"""
Reddit API client for RedditWithLLM.
Handles secure connection to Reddit and data fetching.
"""

import praw
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class RedditUserData:
    """Container for Reddit user account data."""
    username: str
    account_created: datetime
    comment_karma: int
    link_karma: int
    total_karma: int
    is_gold: bool
    is_mod: bool
    recent_posts: List[Dict[str, Any]]
    recent_comments: List[Dict[str, Any]]
    saved_posts: List[Dict[str, Any]]
    subscribed_subreddits: List[str]
    most_active_subreddits: Dict[str, int]


class RedditClient:
    """Secure Reddit API client."""
    
    def __init__(self, client_id: str, client_secret: str, username: str, password: str, user_agent: str):
        """Initialize Reddit client with user credentials."""
        # Ensure proper user agent format
        if not user_agent or len(user_agent) < 10:
            user_agent = f"RedditWithLLM:v1.0 (by /u/{username})"
            
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            username=username,
            password=password,
            user_agent=user_agent
        )
        self.username = username
        
    def test_connection(self) -> bool:
        """Test Reddit API connection."""
        try:
            # Try to access user info
            user = self.reddit.user.me()
            return user is not None
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Reddit connection failed: {error_msg}")
            
            # Provide helpful debugging info
            if "401" in error_msg:
                print(f"🔍 Debug info: 401 Unauthorized - Check your Reddit app credentials:")
                print(f"   • Verify Client ID and Client Secret are correct")
                print(f"   • Ensure your Reddit app is set to 'script' type")
                print(f"   • Confirm username and password are correct")
                print(f"   • Make sure 2FA is disabled or use app password")
            elif "403" in error_msg:
                print(f"🔍 Debug info: 403 Forbidden - User agent or rate limiting issue")
            elif "429" in error_msg:
                print(f"🔍 Debug info: 429 Too Many Requests - Rate limited")
            
            return False
    
    def fetch_user_data(self, limit_posts: int = 25, limit_comments: int = 25, limit_saved: int = 50) -> RedditUserData:
        """
        Fetch comprehensive user data from Reddit.
        
        Args:
            limit_posts: Number of recent posts to fetch
            limit_comments: Number of recent comments to fetch
            limit_saved: Number of saved posts to fetch
            
        Returns:
            RedditUserData: Comprehensive user account data
        """
        try:
            # Get user object
            user = self.reddit.user.me()
            
            # Basic user info
            account_created = datetime.fromtimestamp(user.created_utc)
            
            # Fetch recent posts
            recent_posts = []
            for submission in user.submissions.new(limit=limit_posts):
                post_data = {
                    'title': submission.title,
                    'subreddit': str(submission.subreddit),
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'created_utc': submission.created_utc,
                    'selftext': submission.selftext[:500] if submission.selftext else '',  # Limit text length
                    'url': submission.url if not submission.is_self else None,
                    'upvote_ratio': submission.upvote_ratio
                }
                recent_posts.append(post_data)
            
            # Fetch recent comments
            recent_comments = []
            for comment in user.comments.new(limit=limit_comments):
                comment_data = {
                    'body': comment.body[:300] if comment.body else '',  # Limit comment length
                    'subreddit': str(comment.subreddit),
                    'score': comment.score,
                    'created_utc': comment.created_utc,
                    'parent_title': comment.submission.title if comment.submission else 'Unknown'
                }
                recent_comments.append(comment_data)
            
            # Fetch saved posts
            saved_posts = []
            try:
                print(f"🔍 Fetching saved posts (limit: {limit_saved})...")
                saved_count = 0
                for saved_item in user.saved(limit=limit_saved):
                    saved_count += 1
                    # Check if it's a submission (post) or comment
                    if hasattr(saved_item, 'title'):  # It's a submission
                        # Fetch top comments for this saved post
                        comments_data = []
                        try:
                            saved_item.comments.replace_more(limit=0)  # Remove "more comments" placeholders
                            for comment in saved_item.comments.list()[:10]:  # Get top 10 comments
                                if hasattr(comment, 'body') and comment.body != '[deleted]':
                                    comment_info = {
                                        'author': str(comment.author) if comment.author else '[deleted]',
                                        'body': comment.body[:300],  # Limit comment length
                                        'score': comment.score,
                                        'created_utc': comment.created_utc,
                                        'is_submitter': comment.is_submitter,
                                        'permalink': f"https://reddit.com{comment.permalink}"
                                    }
                                    comments_data.append(comment_info)
                        except Exception as e:
                            print(f"⚠️  Could not fetch comments for saved post '{saved_item.title[:50]}...': {e}")
                        
                        saved_data = {
                            'type': 'post',
                            'title': saved_item.title,
                            'subreddit': str(saved_item.subreddit),
                            'author': str(saved_item.author) if saved_item.author else '[deleted]',
                            'score': saved_item.score,
                            'num_comments': saved_item.num_comments,
                            'created_utc': saved_item.created_utc,
                            'selftext': saved_item.selftext[:500] if saved_item.selftext else '',
                            'url': saved_item.url if not saved_item.is_self else None,
                            'upvote_ratio': saved_item.upvote_ratio,
                            'permalink': f"https://reddit.com{saved_item.permalink}",
                            'comments': comments_data,
                            'comments_fetched': len(comments_data)
                        }
                    else:  # It's a comment
                        saved_data = {
                            'type': 'comment',
                            'body': saved_item.body[:300] if saved_item.body else '',
                            'subreddit': str(saved_item.subreddit),
                            'author': str(saved_item.author) if saved_item.author else '[deleted]',
                            'score': saved_item.score,
                            'created_utc': saved_item.created_utc,
                            'parent_title': saved_item.submission.title if saved_item.submission else 'Unknown',
                            'permalink': f"https://reddit.com{saved_item.permalink}"
                        }
                    saved_posts.append(saved_data)
                print(f"✅ Successfully fetched {len(saved_posts)} saved posts/comments")
            except Exception as e:
                print(f"⚠️  Could not fetch saved posts: {e}")
                print(f"⚠️  This might be due to Reddit API permissions or rate limiting")
                saved_posts = []
            
            # Get subscribed subreddits (limited for privacy)
            subscribed_subreddits = []
            try:
                for subreddit in user.subreddits(limit=50):
                    subscribed_subreddits.append(str(subreddit))
            except Exception:
                # Subreddit list might be private
                subscribed_subreddits = ["Private/Unavailable"]
            
            # Calculate most active subreddits from posts and comments
            subreddit_activity = {}
            for post in recent_posts:
                subreddit = post['subreddit']
                subreddit_activity[subreddit] = subreddit_activity.get(subreddit, 0) + 1
                
            for comment in recent_comments:
                subreddit = comment['subreddit']
                subreddit_activity[subreddit] = subreddit_activity.get(subreddit, 0) + 1
            
            # Sort by activity
            most_active = dict(sorted(subreddit_activity.items(), key=lambda x: x[1], reverse=True)[:10])
            
            return RedditUserData(
                username=str(user),
                account_created=account_created,
                comment_karma=user.comment_karma,
                link_karma=user.link_karma,
                total_karma=user.comment_karma + user.link_karma,
                is_gold=user.is_gold,
                is_mod=user.is_mod,
                recent_posts=recent_posts,
                recent_comments=recent_comments,
                saved_posts=saved_posts,
                subscribed_subreddits=subscribed_subreddits,
                most_active_subreddits=most_active
            )
            
        except Exception as e:
            raise Exception(f"Failed to fetch Reddit user data: {e}")
    
    def get_user_summary(self, user_data: RedditUserData) -> str:
        """
        Generate a text summary of user data for LLM processing.
        
        Args:
            user_data: Reddit user data
            
        Returns:
            str: Formatted summary for LLM
        """
        summary = f"""
Reddit Account Summary for {user_data.username}:

ACCOUNT OVERVIEW:
- Username: {user_data.username}
- Account created: {user_data.account_created.strftime('%Y-%m-%d')}
- Total karma: {user_data.total_karma:,} (Comment: {user_data.comment_karma:,}, Link: {user_data.link_karma:,})
- Reddit Gold: {'Yes' if user_data.is_gold else 'No'}
- Moderator: {'Yes' if user_data.is_mod else 'No'}

ACTIVITY SUMMARY:
- Recent posts: {len(user_data.recent_posts)}
- Recent comments: {len(user_data.recent_comments)}
- Saved posts/comments: {len(user_data.saved_posts)}
- Subscribed subreddits: {len(user_data.subscribed_subreddits)}

MOST ACTIVE SUBREDDITS:
{chr(10).join([f"- r/{sub}: {count} interactions" for sub, count in user_data.most_active_subreddits.items()])}

RECENT POSTS:
{chr(10).join([f"- [{post['subreddit']}] {post['title']} (Score: {post['score']}, Comments: {post['num_comments']})" for post in user_data.recent_posts[:5]])}

RECENT COMMENTS:
{chr(10).join([f"- [{comment['subreddit']}] {comment['body'][:100]}... (Score: {comment['score']})" for comment in user_data.recent_comments[:5]])}

SAVED POSTS/COMMENTS:
{chr(10).join([self._format_saved_item_for_summary(item) for item in user_data.saved_posts[:5]])}
"""
        return summary.strip()
    
    def _format_saved_item_for_summary(self, item: dict) -> str:
        """Format a saved item with its comments for the summary."""
        if item['type'] == 'post':
            base_info = f"- [{item['subreddit']}] {item['title'][:80]}{'...' if len(item['title']) > 80 else ''} (Score: {item['score']}, Comments: {item['num_comments']})"
            if item.get('comments') and len(item['comments']) > 0:
                comments_preview = f"\n    Top replies ({item['comments_fetched']} fetched):"
                for comment in item['comments'][:3]:  # Show top 3 comments
                    comment_preview = comment['body'][:60].replace('\n', ' ')
                    comments_preview += f"\n      • {comment['author']}: {comment_preview}{'...' if len(comment['body']) > 60 else ''} ({comment['score']} pts)"
                return base_info + comments_preview
            else:
                return base_info + "\n    (No comments fetched)"
        else:  # saved comment
            return f"- [{item['subreddit']}] {item.get('body', '')[:100]}{'...' if len(item.get('body', '')) > 100 else ''} (saved comment)"
    
    def search_user_content(self, user_data: RedditUserData, query: str) -> List[Dict[str, Any]]:
        """
        Search user's posts and comments for specific content.
        
        Args:
            user_data: Reddit user data
            query: Search query
            
        Returns:
            List of matching posts and comments
        """
        results = []
        query_lower = query.lower()
        
        # Search posts
        for post in user_data.recent_posts:
            if (query_lower in post['title'].lower() or 
                query_lower in post['selftext'].lower() or
                query_lower in post['subreddit'].lower()):
                results.append({
                    'type': 'post',
                    'content': post,
                    'match_reason': 'Title, content, or subreddit match'
                })
        
        # Search comments
        for comment in user_data.recent_comments:
            if (query_lower in comment['body'].lower() or
                query_lower in comment['subreddit'].lower()):
                results.append({
                    'type': 'comment',
                    'content': comment,
                    'match_reason': 'Comment text or subreddit match'
                })
        
        # Search saved posts and comments
        for saved_item in user_data.saved_posts:
            if saved_item['type'] == 'post':
                # Search in post title, content, and subreddit
                if (query_lower in saved_item['title'].lower() or 
                    query_lower in saved_item['selftext'].lower() or
                    query_lower in saved_item['subreddit'].lower()):
                    results.append({
                        'type': 'saved_post',
                        'content': saved_item,
                        'match_reason': 'Saved post title, content, or subreddit match'
                    })
                
                # Also search in the comments of saved posts
                if saved_item.get('comments'):
                    for comment in saved_item['comments']:
                        if query_lower in comment['body'].lower():
                            results.append({
                                'type': 'saved_post_comment',
                                'content': {
                                    'post_title': saved_item['title'],
                                    'post_subreddit': saved_item['subreddit'],
                                    'comment': comment
                                },
                                'match_reason': f'Comment in saved post "{saved_item["title"][:50]}..."'
                            })
                            break  # Only add one match per post to avoid duplicates
                            
            else:  # saved comment
                if (query_lower in saved_item['body'].lower() or
                    query_lower in saved_item['subreddit'].lower()):
                    results.append({
                        'type': 'saved_comment',
                        'content': saved_item,
                        'match_reason': 'Saved comment text or subreddit match'
                    })
        
        return results
