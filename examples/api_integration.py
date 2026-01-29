"""
MirrorDNA API Integration

Programmatically inject MESH BOOT into API calls.
"""

import os
from pathlib import Path
from openai import OpenAI


def load_mesh_boot(path: str = "~/.mirrordna/mesh_boot.md") -> str:
    """Load MESH BOOT from file."""
    boot_path = Path(path).expanduser()
    if boot_path.exists():
        return boot_path.read_text()
    raise FileNotFoundError(f"MESH BOOT not found at {boot_path}")


class MirrorDNAClient:
    """OpenAI client with MirrorDNA identity injection."""

    def __init__(self, mesh_boot_path: str = "~/.mirrordna/mesh_boot.md"):
        self.client = OpenAI()
        self.mesh_boot = load_mesh_boot(mesh_boot_path)

    def chat(self, message: str, model: str = "gpt-4") -> str:
        """Send message with MESH BOOT context."""
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": self.mesh_boot},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content

    def chat_with_history(self, messages: list, model: str = "gpt-4") -> str:
        """Send conversation with MESH BOOT prepended."""
        full_messages = [
            {"role": "system", "content": self.mesh_boot}
        ] + messages

        response = self.client.chat.completions.create(
            model=model,
            messages=full_messages
        )
        return response.choices[0].message.content


# Example usage
if __name__ == "__main__":
    client = MirrorDNAClient()

    # Single message
    response = client.chat("What's my communication style preference?")
    print(response)

    # With history
    history = [
        {"role": "user", "content": "Let's work on my Python project"},
        {"role": "assistant", "content": "Ready. What's the task?"},
        {"role": "user", "content": "Review this function for issues"}
    ]
    response = client.chat_with_history(history)
    print(response)
