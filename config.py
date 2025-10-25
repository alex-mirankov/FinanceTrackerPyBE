"""
Configuration module for Finance Tracker API.

This module provides centralized configuration management for the Finance Tracker
application using Pydantic Settings. It handles environment variable loading,
type validation, and provides a single source of truth for all application
configuration.

The configuration system:
- Loads settings from environment variables and .env file
- Provides type validation and default values
- Uses LRU caching for performance optimization
- Supports different environments (development, production, testing)
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings configuration using Pydantic BaseSettings.

    This class defines all configuration parameters for the Finance Tracker
    application. Settings are automatically loaded from environment variables
    and the .env file, with type validation and default value support.

    Configuration Categories:
    - Frontend Integration: CORS origins and frontend URL
    - Database Configuration: Connection parameters and SSL settings
    - Google OAuth2: Authentication provider configuration
    - JWT Security: Token generation and validation settings
    - Application URLs: API endpoints and redirect URLs

    Attributes:
        fe_origins (str): Allowed CORS origins for frontend integration
        host (str): Application host address
        fe_url (str): Frontend application URL for redirects
        db_username (str): Database username for connection
        db_password (str): Database password for connection
        db_name (str): Database name to connect to
        db_host (str): Database host address
        db_ssl_mode (str): SSL mode for database connections
        client_id (str): Google OAuth2 client ID
        client_secret (str): Google OAuth2 client secret
        redirect_url (str): OAuth2 redirect URL after authentication
        project_id (str): Google Cloud project ID
        auth_uri (str): Google OAuth2 authorization URI
        token_uri (str): Google OAuth2 token exchange URI
        auth_provider (str): Authentication provider identifier
        google_user_info_url (str): Google user information API endpoint
        jwt_secret (str): Secret key for JWT token signing
        jwt_algo (str): Algorithm used for JWT token signing
    """

    fe_origins: str
    host: str
    fe_url: str
    db_username: str
    db_password: str
    db_name: str
    db_host: str
    db_ssl_mode: str
    client_id: str
    client_secret: str
    redirect_url: str
    project_id: str
    auth_uri: str
    token_uri: str
    auth_provider: str
    google_user_info_url: str
    jwt_secret: str
    jwt_algo: str
    model_config = SettingsConfigDict(env_file=".env")


@lru_cache
def get_settings():
    """
    Get application settings with LRU caching.

    This function provides a cached instance of the Settings class to ensure
    optimal performance when accessing configuration values throughout the
    application. The LRU cache prevents repeated parsing of environment
    variables and .env file.

    Returns:
        Settings: Cached instance of application settings
    """
    return Settings()
