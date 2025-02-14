from .Programs.CodeGeneration import CodeGeneration
from .Programs.Migrate import Migration

commands = {
    Migration.get_alias(): Migration,
    CodeGeneration.get_alias(): CodeGeneration,
}
