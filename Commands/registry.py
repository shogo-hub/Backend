from .Programs.CodeGeneration import CodeGeneration
from .Programs.Migrate import Migration

def registry():
    return [
        Migration,
        CodeGeneration,
    ]

