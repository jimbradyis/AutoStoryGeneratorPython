import uuid
from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class WorldBuilderEntry:
    """Represents a single entry in the World Builder."""
    category: str
    description: str
    keywords: List[str] = field(default_factory=list)

@dataclass
class Character:
    """Represents a single character in the story."""
    name: str
    description: str
    role: str

@dataclass
class Story:
    """Represents the entire story project, including all its components."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    prompt: str = ""
    main_character_desc: str = ""
    target_length: int = 5000
    world_guide: str = ""
    genre: str = ""
    tone: str = ""
    style: str = ""

    # Generated components
    world_builder: List[WorldBuilderEntry] = field(default_factory=list)
    story_outline: str = ""
    characters: List[Character] = field(default_factory=list)
