"""
Runtime credential manager for RedditWithLLM application.
Handles secure in-memory credential collection and validation.
NEVER stores credentials to disk for security.
"""

import getpass
from typing import Optional
from dataclasses import dataclass


@dataclass
class RedditConfig:
    """Reddit API configuration."""
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = "RedditWithLLM/1.0"


@dataclass
class LLMConfig:
    """LLM API configuration."""
    provider: str
    api_key: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    temperature: float = 0.7


@dataclass
class AppConfig:
    """Application configuration."""
    debug: bool = True
    max_posts: int = 10
    default_subreddit: str = "AskReddit"


class RuntimeCredentialManager:
    """Manages runtime credential collection. NEVER stores credentials to disk."""
    
    def __init__(self):
        self.reddit_config: Optional[RedditConfig] = None
        self.llm_config: Optional[LLMConfig] = None
        self.app_config = AppConfig()  # Default app settings
        
    def collect_credentials(self) -> bool:
        """
        Collect credentials from user at runtime.
        SECURITY: Credentials are only stored in memory, never on disk.
        
        Returns:
            bool: True if credentials collected successfully, False otherwise.
        """
        try:
            print("🔐 RedditWithLLM requires credentials at runtime for security.")
            print("⚠️  Credentials are NEVER stored to disk.\n")
            
            # Collect Reddit credentials
            print("📱 Reddit API Credentials:")
            reddit_client_id = input("   Reddit Client ID: ").strip()
            reddit_client_secret = getpass.getpass("   Reddit Client Secret: ").strip()
            reddit_username = input("   Reddit Username: ").strip()
            reddit_password = getpass.getpass("   Reddit Password: ").strip()
            
            # Collect LLM credentials
            print("\n🤖 LLM API Configuration:")
            print("   Supported providers: openai, anthropic")
            llm_provider = input("   LLM Provider (openai): ").strip() or "openai"
            llm_api_key = getpass.getpass("   LLM API Key: ").strip()
            
            # Optional LLM settings
            llm_model = input("   LLM Model (gpt-3.5-turbo): ").strip() or "gpt-3.5-turbo"
            
            # Create configuration objects
            self.reddit_config = RedditConfig(
                client_id=reddit_client_id,
                client_secret=reddit_client_secret,
                username=reddit_username,
                password=reddit_password,
                user_agent="RedditWithLLM/1.0"
            )
            
            self.llm_config = LLMConfig(
                provider=llm_provider,
                api_key=llm_api_key,
                model=llm_model,
                max_tokens=1000,
                temperature=0.7
            )
            
            return self.validate_credentials()
            
        except KeyboardInterrupt:
            print("\n❌ Credential collection cancelled by user")
            return False
        except Exception as e:
            print(f"❌ Error collecting credentials: {e}")
            return False
    
    def validate_credentials(self) -> bool:
        """
        Validate that all required credentials are present and valid.
        
        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        errors = []
        
        # Validate Reddit configuration
        if not self.reddit_config.client_id:
            errors.append("Reddit client_id is required")
            
        if not self.reddit_config.client_secret:
            errors.append("Reddit client_secret is required")
            
        if not self.reddit_config.username:
            errors.append("Reddit username is required")
            
        if not self.reddit_config.password:
            errors.append("Reddit password is required")
        
        # Validate LLM configuration
        if not self.llm_config.api_key:
            errors.append("LLM API key is required")
            
        if self.llm_config.provider not in ["openai", "anthropic"]:
            errors.append(f"Unsupported LLM provider: {self.llm_config.provider}")
        
        if errors:
            print("❌ Credential validation failed:")
            for error in errors:
                print(f"   • {error}")
            return False
            
        print("✅ Credentials validated successfully")
        return True
    
    def get_reddit_config(self) -> RedditConfig:
        """Get Reddit configuration."""
        if not self.reddit_config:
            raise ValueError("Reddit credentials not collected")
        return self.reddit_config
    
    def get_llm_config(self) -> LLMConfig:
        """Get LLM configuration."""
        if not self.llm_config:
            raise ValueError("LLM credentials not collected")
        return self.llm_config
    
    def get_app_config(self) -> AppConfig:
        """Get app configuration."""
        return self.app_config
    
    def clear_credentials(self):
        """Securely clear credentials from memory."""
        if self.reddit_config:
            # Clear sensitive data
            self.reddit_config.client_secret = ""
            self.reddit_config.password = ""
            self.reddit_config = None
            
        if self.llm_config:
            # Clear API key
            self.llm_config.api_key = ""
            self.llm_config = None
            
        print("🔒 Credentials cleared from memory")


def main():
    """Test credential collection."""
    credential_manager = RuntimeCredentialManager()
    
    if credential_manager.collect_credentials():
        print("\n✅ Credentials collected successfully")
        print("🔒 Remember: credentials are only in memory, never stored to disk")
        print(f"Reddit user: {credential_manager.get_reddit_config().username}")
        print(f"LLM provider: {credential_manager.get_llm_config().provider}")
    else:
        print("\n❌ Failed to collect valid credentials")


if __name__ == "__main__":
    main()
