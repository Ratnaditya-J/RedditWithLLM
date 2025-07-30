"""
Interactive query interface for RedditWithLLM.
Provides user-friendly interface for asking ChatGPT about Reddit account data.
"""

from typing import Optional
from colorama import Fore, Style, init
from reddit_client import RedditClient, RedditUserData
from llm_client import LLMClient, LLMResponse

# Initialize colorama
init()


class QueryInterface:
    """Interactive interface for Reddit + ChatGPT queries."""
    
    def __init__(self, reddit_client: RedditClient, llm_client: LLMClient):
        """Initialize query interface with API clients."""
        self.reddit_client = reddit_client
        self.llm_client = llm_client
        self.reddit_data: Optional[RedditUserData] = None
        self.reddit_summary: Optional[str] = None
        
    def load_reddit_data(self) -> bool:
        """Load and cache Reddit user data."""
        try:
            print(f"{Fore.CYAN}📊 Fetching your Reddit account data...{Style.RESET_ALL}")
            
            # Fetch comprehensive Reddit data
            self.reddit_data = self.reddit_client.fetch_user_data()
            self.reddit_summary = self.reddit_client.get_user_summary(self.reddit_data)
            
            print(f"{Fore.GREEN}✅ Reddit data loaded successfully{Style.RESET_ALL}")
            print(f"{Fore.BLUE}📈 Account overview:{Style.RESET_ALL}")
            print(f"   • Username: {self.reddit_data.username}")
            print(f"   • Total karma: {self.reddit_data.total_karma:,}")
            print(f"   • Recent posts: {len(self.reddit_data.recent_posts)}")
            print(f"   • Recent comments: {len(self.reddit_data.recent_comments)}")
            print(f"   • Saved posts/comments: {len(self.reddit_data.saved_posts)}")
            print(f"   • Active subreddits: {len(self.reddit_data.most_active_subreddits)}")
            
            return True
            
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to load Reddit data: {e}{Style.RESET_ALL}")
            return False
    
    def show_quick_insights(self):
        """Show quick AI insights about the user's Reddit account."""
        if not self.reddit_data or not self.reddit_summary:
            print(f"{Fore.RED}❌ Reddit data not loaded{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}🤖 Getting AI insights about your Reddit account...{Style.RESET_ALL}")
        
        response = self.llm_client.analyze_reddit_patterns(self.reddit_summary)
        
        if response.success:
            print(f"\n{Fore.GREEN}💡 AI Insights:{Style.RESET_ALL}")
            print(f"{response.response_text}")
            print(f"\n{Fore.YELLOW}📊 Tokens used: {response.tokens_used}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Failed to get AI insights: {response.error_message}{Style.RESET_ALL}")
    
    def ask_custom_question(self, question: str) -> bool:
        """Ask a custom question about Reddit data."""
        if not self.reddit_data or not self.reddit_summary:
            print(f"{Fore.RED}❌ Reddit data not loaded{Style.RESET_ALL}")
            return False
            
        print(f"\n{Fore.CYAN}🤖 Asking ChatGPT: {question}{Style.RESET_ALL}")
        
        response = self.llm_client.query_about_reddit_data(self.reddit_summary, question)
        
        if response.success:
            print(f"\n{Fore.GREEN}💬 ChatGPT Response:{Style.RESET_ALL}")
            print(f"{response.response_text}")
            print(f"\n{Fore.YELLOW}📊 Tokens used: {response.tokens_used}{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}❌ Failed to get response: {response.error_message}{Style.RESET_ALL}")
            return False
    
    def show_improvement_suggestions(self):
        """Get AI suggestions for improving Reddit engagement."""
        if not self.reddit_data or not self.reddit_summary:
            print(f"{Fore.RED}❌ Reddit data not loaded{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}🚀 Getting improvement suggestions...{Style.RESET_ALL}")
        
        response = self.llm_client.suggest_improvements(self.reddit_summary)
        
        if response.success:
            print(f"\n{Fore.GREEN}🎯 Improvement Suggestions:{Style.RESET_ALL}")
            print(f"{response.response_text}")
            print(f"\n{Fore.YELLOW}📊 Tokens used: {response.tokens_used}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Failed to get suggestions: {response.error_message}{Style.RESET_ALL}")
    
    def compare_subreddits_interactive(self):
        """Interactive subreddit comparison."""
        if not self.reddit_data or not self.reddit_summary:
            print(f"{Fore.RED}❌ Reddit data not loaded{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}🔍 Subreddit Comparison{Style.RESET_ALL}")
        print(f"{Fore.BLUE}Your most active subreddits:{Style.RESET_ALL}")
        for i, (subreddit, count) in enumerate(list(self.reddit_data.most_active_subreddits.items())[:5], 1):
            print(f"   {i}. r/{subreddit} ({count} interactions)")
        
        subreddit1 = input(f"\n{Fore.CYAN}Enter first subreddit to compare: {Style.RESET_ALL}").strip()
        subreddit2 = input(f"{Fore.CYAN}Enter second subreddit to compare: {Style.RESET_ALL}").strip()
        
        if subreddit1 and subreddit2:
            print(f"\n{Fore.CYAN}🤖 Comparing r/{subreddit1} vs r/{subreddit2}...{Style.RESET_ALL}")
            
            response = self.llm_client.compare_subreddits(self.reddit_summary, subreddit1, subreddit2)
            
            if response.success:
                print(f"\n{Fore.GREEN}📊 Comparison Analysis:{Style.RESET_ALL}")
                print(f"{response.response_text}")
                print(f"\n{Fore.YELLOW}📊 Tokens used: {response.tokens_used}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Failed to compare subreddits: {response.error_message}{Style.RESET_ALL}")
    
    def get_content_suggestions_interactive(self):
        """Interactive content suggestions for a subreddit."""
        if not self.reddit_data or not self.reddit_summary:
            print(f"{Fore.RED}❌ Reddit data not loaded{Style.RESET_ALL}")
            return
            
        print(f"\n{Fore.CYAN}💡 Content Suggestions{Style.RESET_ALL}")
        subreddit = input(f"{Fore.CYAN}Enter subreddit for content suggestions: {Style.RESET_ALL}").strip()
        
        if subreddit:
            print(f"\n{Fore.CYAN}🤖 Getting content suggestions for r/{subreddit}...{Style.RESET_ALL}")
            
            response = self.llm_client.get_content_suggestions(self.reddit_summary, subreddit)
            
            if response.success:
                print(f"\n{Fore.GREEN}💡 Content Suggestions:{Style.RESET_ALL}")
                print(f"{response.response_text}")
                print(f"\n{Fore.YELLOW}📊 Tokens used: {response.tokens_used}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}❌ Failed to get suggestions: {response.error_message}{Style.RESET_ALL}")
    
    def show_menu(self):
        """Display interactive menu options."""
        print(f"\n{Fore.CYAN}🎯 What would you like to know about your Reddit account?{Style.RESET_ALL}")
        print(f"{Fore.BLUE}1.{Style.RESET_ALL} Ask a custom question")
        print(f"{Fore.BLUE}2.{Style.RESET_ALL} Get AI insights about my Reddit patterns")
        print(f"{Fore.BLUE}3.{Style.RESET_ALL} Get improvement suggestions")
        print(f"{Fore.BLUE}4.{Style.RESET_ALL} Compare two subreddits")
        print(f"{Fore.BLUE}5.{Style.RESET_ALL} Get content suggestions for a subreddit")
        print(f"{Fore.BLUE}6.{Style.RESET_ALL} Reload Reddit data")
        print(f"{Fore.BLUE}7.{Style.RESET_ALL} Exit")
    
    def run_interactive_session(self):
        """Run the main interactive query session."""
        print(f"\n{Fore.GREEN}🎉 Welcome to RedditWithLLM Interactive Mode!{Style.RESET_ALL}")
        print(f"{Fore.CYAN}You can now ask ChatGPT questions about your Reddit account.{Style.RESET_ALL}")
        
        # Load Reddit data first
        if not self.load_reddit_data():
            return
        
        while True:
            self.show_menu()
            
            try:
                choice = input(f"\n{Fore.CYAN}Enter your choice (1-7): {Style.RESET_ALL}").strip()
                
                if choice == "1":
                    question = input(f"\n{Fore.CYAN}Ask ChatGPT about your Reddit account: {Style.RESET_ALL}").strip()
                    if question:
                        self.ask_custom_question(question)
                    
                elif choice == "2":
                    self.show_quick_insights()
                    
                elif choice == "3":
                    self.show_improvement_suggestions()
                    
                elif choice == "4":
                    self.compare_subreddits_interactive()
                    
                elif choice == "5":
                    self.get_content_suggestions_interactive()
                    
                elif choice == "6":
                    self.load_reddit_data()
                    
                elif choice == "7":
                    print(f"\n{Fore.GREEN}👋 Thanks for using RedditWithLLM!{Style.RESET_ALL}")
                    break
                    
                else:
                    print(f"{Fore.YELLOW}⚠️  Please enter a number between 1-7{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n\n{Fore.GREEN}👋 Goodbye!{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Error: {e}{Style.RESET_ALL}")
