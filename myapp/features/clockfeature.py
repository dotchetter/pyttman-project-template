from datetime import datetime

from pyttman import Feature
from pyttman.core.communication.command import Command
from pyttman.core.communication.models.containers import Reply, Message
from pyttman.core.parsing import parsers
from pyttman.core.parsing.identifiers import DateTimeFormatIdentifier


class SetTimeFormat(Command):
    """
    This command allows users to set the format of 
    datetime strings. It uses the EntityParser API 
    with a DateTimeFormatIdentifier Identifier class 
    to do this efficiently and with very little code.
    """
    description = "Sets the format of datetime outputs"
    lead = ("set",)
    trail = ("datetime", "format",)
    example = "Set the datetime format to %m-%d-%y::%H:%M"

    class EntityParser(Command.EntityParser):
        datetime_format = parsers.ValueParser(identifier=DateTimeFormatIdentifier)

    def respond(self, message: Message) -> Reply:
        # Check the entities dict, populated by the EntityParser
        if datetime_format := self.entities.get("datetime_format"):

            # Accessing the Feature-scope Storage object
            self.feature.storage.put("datetime_format", datetime_format)
            return Reply(f"Set datetime format to: {datetime_format}")


class GetTime(Command):
    """
    This command returns a timestamp, with the 
    configured time format.
    """
    lead = ("what",)
    trail = ("time",)
    example = "What time is it?"

    def respond(self, message: Message) -> Reply:
        time_format = self.feature.storage.get("datetime_format")
        return Reply(f"The time is currently {datetime.now().strftime(time_format)}")


class ClockFeature(Feature):
    """
    A basic, simple feature which
    answers what time it is.
    """
    commands = (GetTime, SetTimeFormat)

    def configure(self):
        self.storage.put("datetime_format", "%y-%m-%d - %H:%M")
