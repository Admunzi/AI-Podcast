"""
Curiosities podcast main file

Autor: Daniel Ayala Cantador
"""

import typer
from rich import print
from rich.table import Table
import time
import openai_api
import os
import speech_polly

# Context of the podcast
context_text = open("context.txt", "r").read()
context = {"role": "system", "content": context_text}

GUESTS = ["Juan", "Manolo", "Lucía"]


def main():
    show_commands()
    messages = [context]

    themes = open("themes.txt", "r").read().splitlines()

    for theme in themes:
        response_content = generate_content(theme, messages)
        theme = theme.replace(" ", "_")
        generate_file_content(theme, response_content)
        generate_fragments_audio_content(theme, response_content)
        put_fragments_together(theme)

        # When the podcast is generated, clear the messages
        messages = [context]


def put_fragments_together(theme):
    """
    Put the fragments of the podcast together. In the folder audios there are the fragments of the podcast.
    Here we put the fragments together and generate the final podcast.
    """
    os.system(f"cat programs/{theme}/audios/* > programs/{theme}/podcast.mp3")


def generate_fragments_audio_content(theme, response_content):
    """
    Read each line of the podcast and check the name of the person who speaks.
    The syntax is:
        [Jose Luis]: Hello, how are you?
        [Juan]: I'm fine, and you?
        [Lucía]: I'm fine too, thanks.
        [Manolo]: I'm fine too, thanks.
    """
    lines = response_content.splitlines()
    os.makedirs(f"programs/{theme}/audios")

    # Default person is Jose Luis because sometimes the person is not specified when speaking multiple lines
    person = "Jose Luis"

    for line in lines:
        num_line = lines.index(line) + 1

        # use regex to find the name of the person who speaks
        if line.startswith("["):
            person = line.split("]")[0].replace("[", "")
            text = line.split("]: ")[1]
        else:
            text = line
        speech_polly.speech(person, text, theme, num_line)


def generate_content(theme, messages):
    # Generate the podcast header
    content = f"El tema del podcast será sobre '{theme}', genera la presentación del podcast, punto 1."
    response_content_final, messages = openai_api.generate_podcast(content, messages)

    # Generate the podcast content for each guest
    for guest in GUESTS:
        content = f"El invitado del podcast será {guest}, realiza el punto 2, 3, 4, 5. Al terminar de generar el " \
                  f"contenido del invitado, no lo hagas en tono de despedida"
        response_content, messages = openai_api.generate_podcast(content, messages)
        response_content_final += "\n" + response_content

    # Generate podcast footer
    content = f"Realiza el punto 6."
    response_content, messages = openai_api.generate_podcast(content, messages)
    response_content_final += "\n" + response_content

    return response_content_final


def show_commands():
    print("💬 [bold green]Curiosities podcast[/bold green]")
    table = Table("Command", "Description")
    table.add_row("exit", "Exit the application")
    table.add_row("new", "Create a new program")
    print(table)


def generate_file_content(theme, response_content):
    # Create folder for the programs
    os.makedirs(f"programs/{theme}")

    # Generate program file, the name of the file is current date and time
    with open(f"programs/{theme}/content.txt", "w") as file:
        file.write(response_content)
    print(f"📝 [bold green]Podcast generated[/bold green]: {theme}")


if __name__ == "__main__":
    typer.run(main)
