import re
from openai import OpenAI
import os

client = OpenAI(
    # This is the default and can be omitted
    api_key=os.getenv("OPENAI_API_KEY"),
)

title = """Margaret Atwood
The Handmaid’s Tale"""

def splitFiles(path):
    # Open the file, look for all matches to "CHAPTER .*" and find corresponding line numbers
    with open(path, 'r') as file:
        lines = file.readlines()
        chapter_lines = [i for i, line in enumerate(lines) if "CHAPTER" in line]
        openai_filenames = {

        }

        # Go through each chapter, and go two lines before and see if it is a roman numeral using regex
        for i, chapter_line in enumerate(chapter_lines):
            pre_chap = lines[chapter_line - 2]
            match = re.match(r'^[IVXLCDM]+$', pre_chap.strip())
            # If match, change the line in array to 2 lines 
            if match:
                chapter_lines[i] = chapter_line - 2
        
        # split the file based on line numbers, append title to start, save to out/
        for i, chapter_line in enumerate(chapter_lines):
            if i == len(chapter_lines) - 1:
                chapter = lines[chapter_line:]
            else:
                chapter = lines[chapter_line:chapter_lines[i+1]]
            chapter.insert(0, title+"\n")
            with open(f"out/hmt-{i}.txt", 'w') as file:
                file.writelines(chapter)
            openai_file = client.files.create(
                file=open(f"out/hmt-{i}.txt", 'rb'),
                purpose="assistants",
            )
            openai_filenames[openai_file.id] = f"HMT Chapter {i}"

        print(openai_filenames)

splitFiles("hmt.txt")