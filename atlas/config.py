from pathlib import Path

import yaml
from pydantic import BaseModel, Field, ValidationError

CONFIG_PATH = Path("config/atlas.yaml")


class ModelConfig(BaseModel):
    name: str = "qwen3:8b"
    temperature: float = Field(0.3, ge=0.0, le=2.0)
    top_p: float = Field(0.9, ge=0.0, le=1.0)
    num_ctx: int = Field(4096, gt=0)


class PersonaConfig(BaseModel):
    name: str = "Atlas"
    system_prompt: str


class MemoryConfig(BaseModel):
    top_k: int = Field(3, gt=0)
    min_similarity: float = Field(0.7, ge=0.0, le=1.0)


class GuardrailsConfig(BaseModel):
    enabled: bool = True
    max_input_chars: int = Field(4000, gt=0)
    blocked_topics: list[str] = []
    enable_pii_masking: bool = True
    enable_injection_check: bool = True
    enable_blocked_topics: bool = True
    enable_length_check: bool = True


class AppConfig(BaseModel):
    model: ModelConfig = ModelConfig()
    persona: PersonaConfig = PersonaConfig(
        name="Atlas",
        system_prompt="Tu es Atlas, assistant IA interne d'ATLAS Consulting.",
    )
    memory: MemoryConfig = MemoryConfig()
    guardrails: GuardrailsConfig = GuardrailsConfig()


def load_config() -> AppConfig:
    if not CONFIG_PATH.exists():
        return AppConfig()
    try:
        raw = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
        return AppConfig(**raw)
    except ValidationError as e:
        raise SystemExit(f"Config invalide dans {CONFIG_PATH}:\n{e}")
    except yaml.YAMLError as e:
        raise SystemExit(f"YAML malformé dans {CONFIG_PATH}:\n{e}")


config = load_config()
