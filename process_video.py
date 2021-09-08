#!/usr/bin/python3

import typing
import time
import json
import argparse

import ffmpeg

parser = argparse.ArgumentParser(usage="Convert videos to fit collected data.\n")
parser.add_argument("screen_config_json", help="collected screen data")
parser.add_argument("in_video", help="path of video to parse")
parser.add_argument("out_video", help="path of video to output")
parser.add_argument("-c", "--crop", help="crop for aspect ratio compensation", action="store_true") #TODO
parser.add_argument("-p", "--padding", help="force constant padding value", action="store_true") #TODO
parser.add_argument("-n", "--noaction", help="do not encode", action="store_true") #TODO
parser.add_argument("-v", "--verbose", help="print all actions", action="store_true") #TODO
parser.add_argument("-q", "--quiet", help="hide all actions", action="store_true") #TODO
args = parser.parse_args()

severities = ["INF", "WRN", "ERR"]

def log(message: str, severity: str) -> None:
    log_time = ""
    if args.verbose == True:
        log_time = f"{time.time():.8f} "

    if severity == 0 and args.verbose == True and args.quiet == False:
        print(f"{log_time}\x1b[0;37;40m{severities[severity]}: {message}\033[0;0m")
    elif severity == 1 and args.quiet == False:
        print(f"{log_time}\x1b[0;33;40m{severities[severity]}: {message}\033[0;0m")
    elif severity == 2 and args.quiet == False:
        print(f"{log_time}\x1b[0;31;40m{severities[severity]}: {message}\033[0;0m")

#TODO: def divide():

with open(args.screen_config_json, "r") as read_file:
    config = json.load(read_file)
    probe = ffmpeg.probe(args.in_video)
    log(json.dumps(probe["streams"][0]), 0)

    video_stream_indicies = []
    for idx,stream in enumerate(probe["streams"]):
        if stream["codec_type"] == "video":
            video_stream_indicies.append(idx)

    log(f"Video streams detected: {video_stream_indicies}", 0)


    #in_video = ffmpeg.input(args.in_video).filter('crop')
    #in0 = ffmpeg.input(args.in_video).filter('crop', "iw", "ih/3", "0", "0").output("0.mp4").run()
    #in1 = ffmpeg.input(args.in_video).filter('crop', "iw", "ih/3", "0", "oh").output("1.mp4").run()
    #in2 = ffmpeg.input(args.in_video).filter('crop', "iw", "ih/3", "0", "oh*2").output("2.mp4").run()
    for screen in config["screens"]:
        log(json.dumps(screen), 1)


