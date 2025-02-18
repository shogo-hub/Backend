from .Programs.CodeGeneration import CodeGeneration
from .Programs.Migrate import Migration

commands = {
    Migration.getAlias(): Migration,
    CodeGeneration.getAlias(): CodeGeneration,
}
