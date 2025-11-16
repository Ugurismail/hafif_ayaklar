"""
Agora.io RTC Token Generator
Bu modül Agora.io için RTC token oluşturur.

Agora.io setup için:
1. https://console.agora.io/ adresinden hesap oluşturun
2. Yeni bir proje oluşturun
3. App ID ve App Certificate'i alın
4. .env dosyasına ekleyin:
   AGORA_APP_ID=your_app_id_here
   AGORA_APP_CERTIFICATE=your_app_certificate_here
"""

import os
import time
from typing import Literal

# Agora token generation için agora_token_builder paketi gerekli
# pip install agora_token_builder

try:
    from agora_token_builder import RtcTokenBuilder
    from agora_token_builder.RtcTokenBuilder import Role_Publisher, Role_Subscriber
    AGORA_AVAILABLE = True
except ImportError:
    AGORA_AVAILABLE = False
    print("WARNING: agora_token_builder package not installed. Run: pip install agora_token_builder")


def generate_agora_token(
    channel_name: str,
    uid: int,
    role: Literal['broadcaster', 'audience'] = 'audience',
    expiration_time_in_seconds: int = 3600
) -> str:
    """
    Generate an Agora RTC token for a user to join a channel.

    Args:
        channel_name: The name of the channel
        uid: User ID (should be unique)
        role: 'broadcaster' for DJ, 'audience' for listeners
        expiration_time_in_seconds: Token validity duration (default: 1 hour)

    Returns:
        Generated token string

    Raises:
        ValueError: If AGORA_APP_ID or AGORA_APP_CERTIFICATE is not set
        ImportError: If agora-token package is not installed
    """
    if not AGORA_AVAILABLE:
        raise ImportError(
            "agora_token_builder package is required. Install it with: pip install agora_token_builder"
        )

    app_id = os.environ.get('AGORA_APP_ID')
    app_certificate = os.environ.get('AGORA_APP_CERTIFICATE')

    if not app_id or not app_certificate:
        raise ValueError(
            "AGORA_APP_ID and AGORA_APP_CERTIFICATE must be set in environment variables. "
            "Get them from https://console.agora.io/"
        )

    # Current timestamp
    current_timestamp = int(time.time())

    # Privilege expire timestamp (current time + expiration duration)
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds

    # Determine role
    agora_role = Role_Publisher if role == 'broadcaster' else Role_Subscriber

    # Build token
    token = RtcTokenBuilder.buildTokenWithUid(
        app_id,
        app_certificate,
        channel_name,
        uid,
        agora_role,
        privilege_expired_ts
    )

    return token


def generate_dj_token(channel_name: str, uid: int) -> str:
    """
    Generate token for DJ (broadcaster role) with 6 hour expiration.
    """
    return generate_agora_token(
        channel_name=channel_name,
        uid=uid,
        role='broadcaster',
        expiration_time_in_seconds=6 * 3600  # 6 hours
    )


def generate_listener_token(channel_name: str, uid: int) -> str:
    """
    Generate token for listener (audience role) with 3 hour expiration.
    """
    return generate_agora_token(
        channel_name=channel_name,
        uid=uid,
        role='audience',
        expiration_time_in_seconds=3 * 3600  # 3 hours
    )


def is_agora_configured() -> bool:
    """
    Check if Agora is properly configured.
    """
    return (
        AGORA_AVAILABLE and
        bool(os.environ.get('AGORA_APP_ID')) and
        bool(os.environ.get('AGORA_APP_CERTIFICATE'))
    )
