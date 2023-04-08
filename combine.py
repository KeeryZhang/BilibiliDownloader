#!/usr/local/bin/python3
"""Module to combine audio and video"""

import rename
import os

FFMPEG = r"D:\zqy92\Downloads\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"


class Episode:
    def __init__(self, src_path, dst_path, title=None) -> None:
        self.epi_path = src_path
        self.dst_root = dst_path
        self.entry = None
        self.audio = None
        self.video = None
        self.media_folder = None
        self.epi_name = None
        self.collection_title = title
        self.processing()

    def get_fullpath(self, file_name, parent=None):
        if not parent:
            parent = self.epi_path
        fullpath = os.path.join(parent, file_name)
        return fullpath

    def sorting(self):
        contents = os.listdir(self.epi_path)
        for content in contents:
            fullpath = self.get_fullpath(content)
            if os.path.isdir(fullpath):
                self.media_folder = fullpath
            elif content.startswith("entry"):
                self.entry = fullpath
        
        sub_contents = os.listdir(self.media_folder)
        for sub_content in sub_contents:
            fullpath = self.get_fullpath(sub_content, self.media_folder)
            if sub_content.startswith("audio"):
                self.audio = rename.rename_audio(fullpath)
            elif sub_content.startswith("video"):
                self.video = rename.rename_video(fullpath)
    
    def find_epi_name(self):
        entry = rename.loadentry(self.entry)
        self.epi_name = ".".join([rename.findname(entry), "mp4"])
    
    def find_collection_title(self):
        entry = rename.loadentry(self.entry)
        if not self.collection_title:
            self.collection_title = rename.findtitle(entry)
        self.collection_path = os.path.join(self.dst_root, self.collection_title)

    def processing(self):
        self.sorting()
        self.find_epi_name()
        self.find_collection_title()

    def av_combine(self):
        self.command = ""
        pre_params = "-hwaccel cuvid -c:v h264_cuvid"
        inputs = "-i {0} -i {1}".format(self.audio, self.video)
        post_params = "-c:v h264_nvenc"
        output = "\"{0}\{1}\"".format(self.collection_path, self.epi_name)
        self.command = " ".join([FFMPEG, pre_params, inputs, post_params, output])
        os.system(self.command)
        print("{} processed and saved".format(output))


class Combine:
    def __init__(self, src_path, dst_path, title=None):
        self.src_path = r"{}".format(src_path)
        self.dst_path = r"{}".format(dst_path)
        self.collection_title = title
        self.video_folders = []
        self.sorting()

    def get_fullpath(self, file_name, parent=None):
        if not parent:
            parent = self.src_path
        fullpath = os.path.join(parent, file_name)
        return fullpath

    def sorting(self):
        contents = os.listdir(self.src_path)
        for content in contents:
            fullpath = self.get_fullpath(content)
            sub_folder = Episode(fullpath, self.dst_path, self.collection_title)
            self.video_folders.append(sub_folder)

    def processing(self):
        if not self.collection_title:
            self.collection_title = self.video_folders[0].collection_title
        fullname = os.path.join(self.dst_path, self.collection_title)
        os.makedirs(fullname, exist_ok=True)
        
        for video_folder in self.video_folders:
            video_folder.av_combine()
