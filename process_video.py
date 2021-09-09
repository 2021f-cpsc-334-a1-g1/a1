#!/usr/bin/python3

# Python library imports
import typing
import os
import time
import json
import argparse

# FFmpeg binary bindings
import ffmpeg

# Argument parsing
parser = argparse.ArgumentParser(usage="Convert videos to fit collected data.\n")
parser.add_argument("screen_config_json", help="collected screen data")
parser.add_argument("in_video", help="path of video to parse")
parser.add_argument("out_video", help="path of video to output")
parser.add_argument("--crf", help="crf for intermediate encoding (default: 30)", default=30, type=int)
parser.add_argument("--preset", help="profile for intermediate encoding (default: veryfast)", default="veryfast", type=str)
parser.add_argument("-p", "--padding", help="constant padding value (default: 0)", default=0, type=int) # TODO
parser.add_argument("-c", "--crop", help="crop for aspect ratio compensation", action="store_true") # TODO
parser.add_argument("-s", "--split", help="keep video split for each screen", action="store_true")
parser.add_argument("-n", "--noaction", help="do not encode", action="store_true") # TODO
parser.add_argument("-v", "--verbose", help="print all actions", action="store_true")
parser.add_argument("-q", "--quiet", help="hide all actions", action="store_true")
args = parser.parse_args()

# FFmpeg log level setting
logl = ""
if args.verbose is True:
    logl = "info"
else:
    logl = "quiet"

# Script log levels
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
        exit(1)

# Open screen config generated in previous script
with open(args.screen_config_json, "r") as read_file:
    config = json.load(read_file)

    # Probe in_video
    probe = ffmpeg.probe(args.in_video)

    # Look for applicable in_video streams
    video_stream_indicies = []
    for idx,stream in enumerate(probe["streams"]):
        if stream["codec_type"] == "video":
            video_stream_indicies.append(idx)
    log(f"Video streams detected on: {video_stream_indicies}", 0)

    # Multiple video streams unsupported
    if len(video_stream_indicies) > 1:
        log("More than one video stream detected.\nSpatial audio may be encoded to video tracks.", 2)
    elif len(video_stream_indicies) < 1:
        log("No video streams detected.", 2)

    # Find in_video resolution
    in_video_width = probe["streams"][video_stream_indicies[0]]["width"]
    in_video_height = probe["streams"][video_stream_indicies[0]]["height"]
    log(f"Input resolution: {in_video_width}x{in_video_height}", 0)

    # Find out_video resolution
    total_width = 0
    total_height = config["screens"][0]["size"]["y"]
    for screen in config["screens"]:
        total_width += screen["size"]["x"]
        # TODO: Height, total_height += screen["size"]["y"]
    log(f"Output resolution: {total_width}x{total_height}", 0)

    # If not preprocessed to output resolution, preprocess
    if in_video_width != total_width or in_video_height != total_height:
        upscale = ffmpeg.input(args.in_video).filter("scale", width=total_width, height=total_height).filter("setsar", "1", "1").output("part-x.mp4", crf=args.crf, preset=args.preset, loglevel=logl).run()

    # Create crops based on screen config, collect as inputs for concat step
    hstack = []
    for idx,screen in enumerate(config["screens"]):
        log(f"Processing screen: {json.dumps(screen)}", 0)
        out = ffmpeg.input("part-x.mp4").filter('crop', f"{screen['size']['x']}", f"{screen['size']['y']}", f"{screen['origin']['x']}", f"{screen['origin']['y']}").output(f"part-{idx}.mp4", loglevel=logl).run()
        hstack.append(ffmpeg.input(f"part-{idx}.mp4"))

    # If not keeping split, concatenate videos horizontally
    # TODO: Rotation options from screen config
    if not args.split:
        out = ffmpeg.filter(hstack, "hstack", "3").output(args.out_video, crf=args.crf, preset=args.preset, loglevel=logl).run()

        # Clean up individual crops
        for idx,screen in enumerate(config["screens"]):
            os.remove(f"part-{idx}.mp4")

    # Clean up resolution preprocessing
    os.remove("part-x.mp4")
