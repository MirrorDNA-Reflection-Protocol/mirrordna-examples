"""
MirrorDNA + LangChain Integration

Inject MESH BOOT into LangChain conversations for persistent identity.
"""

from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


def load_mesh_boot(path: str = "~/.mirrordna/mesh_boot.md") -> str:
    """Load MESH BOOT from file."""
    boot_path = Path(path).expanduser()
    if boot_path.exists():
        return boot_path.read_text()
    raise FileNotFoundError(f"MESH BOOT not found at {boot_path}")


def create_mirrordna_chain(model: str = "gpt-4"):
    """Create a LangChain with MirrorDNA identity."""
    mesh_boot = load_mesh_boot()

    llm = ChatOpenAI(model=model)

    # Inject MESH BOOT as system message
    def invoke_with_identity(user_message: str):
        messages = [
            SystemMessage(content=mesh_boot),
            HumanMessage(content=user_message)
        ]
        return llm.invoke(messages)

    return invoke_with_identity


# Example usage
if __name__ == "__main__":
    chain = create_mirrordna_chain()

    response = chain("What do you know about me from my MESH BOOT?")
    print(response.content)
