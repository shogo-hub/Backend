from .Programs.CodeGeneration import CodeGeneration
from .Programs.Migrate import Migrate

commands = {
    Migrate.getAlias(): Migrate,
    CodeGeneration.getAlias(): CodeGeneration,
}
