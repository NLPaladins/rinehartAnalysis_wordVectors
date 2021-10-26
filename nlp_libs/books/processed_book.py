import urllib.request
import re
from typing import *
from nlp_libs.fancy_logger.colorized_logger import ColorizedLogger

#logger = ColorizedLogger(logger_name='Process Book', color='cyan')

class ProcessedBook:
    title: str
    protagonists: Dict
    antagonist: Dict
    crime_weapon: Dict
    crime_objects: Dict

    def __init__(self, title: str, metadata: Dict):
        """
        raw holds the books as a single string.
        clean holds the books as a list of lowercase lines starting
        from the first chapter and ending with the last sentence.
        """
        self.title = title
        self.protagonists = metadata['protagonists']
        self.antagonist = metadata['antagonist']
        self.crime_weapon = metadata['crime']['crime_weapon']
        self.crime_objects = metadata['crime']['crime_objects']

        self.raw = self.read_book_from_proj_gut(metadata['url'])
        self.book_lines = self.get_book_lines_from_raw()
        self.clean_lines = self.clean_lines()
        self.clean = ' '.join(self.clean_lines).replace('  ', ' ')
        self.clean_lower = self.clean.lower()

    @staticmethod
    def read_book_from_proj_gut(book_url: str) -> str:
        req = urllib.request.Request(book_url)
        client = urllib.request.urlopen(req)
        page = client.read()
        return page.decode('utf-8')

    def get_book_lines_from_raw(self):
        raw = re.sub(r'\r\n', r'\n', self.raw)
        lines = re.findall(r'.*\n', raw)
        start = False
        text = []
        for i, line in enumerate(lines):
            # match chapters for book start and for 
            # removing chapter headers and titles
            if re.search(r'^ *((CHAPTER|Chapter) [A-Z]+\.?)\n$', line) or re.search(r'^ *[IVXLCDM]+\.?\n$', line):
                start = True
                chapter_start = True
                continue
            if start:
                if not chapter_start:
                    # check for book end
                    if re.search(r'project gutenberg', line, re.IGNORECASE):
                        break
                    else:
                        text.append(line)
                else:
                    # removing chapter titles if they are there
                    if re.search(r'^([A-Z] ?)+$', line):
                        chapter_start = False
                    if re.search(r'[a-z]+', line):
                        text.append(line)
                        chapter_start = False
        return text

    def clean_lines(self):
        clean_lines = []
        for line in self.book_lines:
            line = re.sub(r'([’‘])', '', line)
            if self.pass_clean_filter(line):
                clean_lines.append(line)
        return clean_lines

    @staticmethod
    def pass_clean_filter(line: str) -> bool:
        if re.search(r'^((\[illustration:)|(illustration:))', line, re.IGNORECASE):
            return False
        if re.search('^[\* ]*\n$', line):
            return False
        else:
            return True
