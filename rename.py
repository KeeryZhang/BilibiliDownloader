#!/usr/local/bin/python3
"""Find correct name from json file and rename the video file"""

import json
import os


def loadentry(entry_file):
    """Load entry data from json file"""
    entry = None
    with open(file=entry_file, mode="r", encoding="UTF-8") as f:
        entry = json.load(f)
    return entry

def remove_space(name:str):
    """Remove Starting or Ending space from file name"""
    if name.startswith(" "):
        name = name[1:]
    elif name.endswith(" "):
        name = name[:-1]
    else:
        return name
    name = remove_space(name)
    return name

def findname(entry):
    """Find and parsing name from entry"""
    page_data = entry.get("page_data")
    name = page_data.get("part")
    name = remove_space(name)
    return name

def findtitle(entry):
    """Find collection title"""
    title = entry.get("title")
    return title

def rename(video_file, new_name):
    """Rename video file to real name"""
    parent = os.path.dirname(video_file)
    new_path = os.path.join(parent, new_name)
    os.rename(video_file, new_path)
    return new_path

def rename_audio(audio_file):
    old_name = audio_file.split(".")[0]
    new_name = ".".join([old_name, "mp3"])
    os.rename(audio_file, new_name)
    return new_name

def rename_video(video_file):
    old_name = video_file.split(".")[0]
    new_name = ".".join([old_name, "mp4"])
    os.rename(video_file, new_name)
    return new_name

# Only for test
# def test_rename():
#     print("Test Start")
#     test_file = r"d:\zqy92\Downloads\test_file.123"
#     with open(test_file, "w", encoding="UTF-8") as f:
#         f.write("")
#     print("Test file created")
#     entry_file = r"d:\zqy92\Downloads\entry.json"
#     entry = loadentry(entry_file)
#     new_name = ".".join([findname(entry), "mp4"])
#     new_path = rename(test_file, new_name)
#     print("Test file renamed")
#     assert os.path.exists(new_path), "Cannot find new file {}".format(new_path)
#     print("Test Pass")
#     os.remove(new_path)
#     print("Test file removed")
#     print("Test Done")

# test_rename()
