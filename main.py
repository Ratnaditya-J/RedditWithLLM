"""
RedditWithLLM - Main application entry point.
Combines Reddit API integration with Large Language Model capabilities.
"""

import sys
import os
from colorama import init, Fore, Style

# Initialize colorama for cross-platform colored output
init()

from config_manager import RuntimeCredentialManager


def print_banner():
    """Print application banner."""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗
║                        RedditWithLLM                         ║
║              Reddit + AI Integration Platform                ║
╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def main():
    """Main application entry point."""
    print_banner()
    
    print(f"{Fore.CYAN}🔐 Collecting credentials securely...{Style.RESET_ALL}")
    
    # Initialize runtime credential manager
    credential_manager = RuntimeCredentialManager()
    
    # Collect and validate credentials at runtime
    if not credential_manager.collect_credentials():
        print(f"{Fore.RED}❌ Failed to collect valid credentials{Style.RESET_ALL}")
        return
    
    print(f"{Fore.GREEN}✅ Credentials validated successfully{Style.RESET_ALL}")
    
    # Get configurations
    reddit_config = credential_manager.get_reddit_config()
    llm_config = credential_manager.get_llm_config()
    app_config = credential_manager.get_app_config()
    
    print(f"{Fore.BLUE}📱 Reddit user: {reddit_config.username}{Style.RESET_ALL}")
    print(f"{Fore.BLUE}🤖 LLM provider: {llm_config.provider} ({llm_config.model}){Style.RESET_ALL}")
    
    try:
        # Initialize Reddit client
        print(f"\n{Fore.CYAN}📱 Connecting to Reddit API...{Style.RESET_ALL}")
        from reddit_client import RedditClient
        
        reddit_client = RedditClient(
            client_id=reddit_config.client_id,
            client_secret=reddit_config.client_secret,
            username=reddit_config.username,
            password=reddit_config.password,
            user_agent=reddit_config.user_agent
        )
        
        if not reddit_client.test_connection():
            print(f"{Fore.RED}❌ Failed to connect to Reddit API{Style.RESET_ALL}")
            return
            
        print(f"{Fore.GREEN}✅ Reddit API connected successfully{Style.RESET_ALL}")
        
        # Initialize ChatGPT client
        print(f"{Fore.CYAN}🤖 Connecting to ChatGPT API...{Style.RESET_ALL}")
        from llm_client import LLMClient
        
        llm_client = LLMClient(
            api_key=llm_config.api_key,
            model=llm_config.model,
            max_tokens=llm_config.max_tokens,
            temperature=llm_config.temperature
        )
        
        if not llm_client.test_connection():
            print(f"{Fore.RED}❌ Failed to connect to ChatGPT API{Style.RESET_ALL}")
            return
            
        print(f"{Fore.GREEN}✅ ChatGPT API connected successfully{Style.RESET_ALL}")
        
        # Launch interactive query interface
        print(f"\n{Fore.GREEN}🎉 All systems ready! Launching interactive mode...{Style.RESET_ALL}")
        from query_interface import QueryInterface
        
        query_interface = QueryInterface(reddit_client, llm_client)
        query_interface.run_interactive_session()
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Application interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Application error: {e}{Style.RESET_ALL}")
    finally:
        # Always clear credentials from memory when done
        print(f"\n{Fore.CYAN}🔒 Cleaning up...{Style.RESET_ALL}")
        credential_manager.clear_credentials()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Goodbye!{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}❌ Unexpected error: {e}{Style.RESET_ALL}")
        sys.exit(1)
