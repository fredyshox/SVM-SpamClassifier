import numpy as np
import re

class EmailProcessor():
    @staticmethod
    def process_email(contents):
        contents = EmailProcessor.replace_contents(contents)

    @staticmethod
    def replace_contents(contents):
        contents = "test_contents"
        has_header = True

        # If this is raw email, find email header and remove ( \n\n )
        if has_header:
            header = contents.find(chr(10) + chr(10))
            if not header == -1:
                contents = contents[header:len(contents)]

        # Lower case
        contents = contents.lower()
        # using regular expressions

        # HTML Headers
        # Replace strings that start with < and end with >
        contents = re.sub('<[^<>]+>', ' ', contents)

        # Numbers
        # Replace any one or more chars from 0-9
        contents = re.sub('[0-9]+', 'number', contents)

        # URLs
        # Replace any expressions starting with http:// or https:// and other characters except whitespace
        contents = re.sub('(http|https)://[^\s]*', 'httpaddr', contents)

        # Emails
        contents = re.sub('[^\s]+@[^\s]+', 'emailaddr', contents)

        # $ sign
        contents = re.sub('[$]+', 'dollar', contents)
        # TODO handle other currencies

        return contents