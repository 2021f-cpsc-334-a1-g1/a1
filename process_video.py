#!/usr/bin/python3

# Python library imports
import typing
import os
import time
import json
import argparse

# FFmpeg binary bindings
import ffmpeg

from pathlib import Path
ffprobe_loc = Path("./bin/ffmpeg/ffprobe.exe")
ffmpeg_loc = Path("./bin/ffmpeg/ffmpeg.exe")

# Argument parsing
parser = argparse.ArgumentParser(usage="Convert videos to fit collected data.\n")
parser.add_argument("display_config_json", help="collected screen data")
parser.add_argument("in_video", help="path of video to parse")
parser.add_argument("out_video", help="path of video to output")
parser.add_argument("--crf", help="crf for intermediate encoding (default: 30)", default=30, type=int)
parser.add_argument("--preset", help="profile for intermediate encoding (default: veryfast)", default="veryfast", type=str)
parser.add_argument("-p", "--padding", help="constant padding value (default: 0)", default=0, type=int) # TODO
parser.add_argument("-r", "--rotate", help="add clockwise rotation degree (only 90, 180, 270 accepted)", default=0, type=int) # TODO
parser.add_argument("-c", "--crop", help="crop for aspect ratio compensation", action="store_true") # TODO
parser.add_argument("-s", "--split", help="keep video split for each screen", action="store_true")
parser.add_argument("-n", "--noaction", help="do not encode", action="store_true") # TODO
parser.add_argument("-v", "--verbose", help="print all actions", action="store_true")
parser.add_argument("-q", "--quiet", help="hide all actions", action="store_true")
args = parser.parse_args()

# Script log levels
severities = ["INF", "INF", "WRN", "ERR"]
def log(message: str, severity: str) -> None:
    log_time = ""
    if args.verbose == True:
        log_time = f"{time.time():.8f} "

    if severity == 0 and args.quiet == False and args.verbose == True:
        print(f"{log_time}\x1b[0;36;40m{severities[severity]}: {message}\033[0;0m")
    elif severity == 1 and args.quiet == False:
        print(f"{log_time}\x1b[0;37;40m{severities[severity]}: {message}\033[0;0m")
    elif severity == 2 and args.quiet == False:
        print(f"{log_time}\x1b[0;33;40m{severities[severity]}: {message}\033[0;0m")
    elif severity == 3 and args.quiet == False:
        print(f"{log_time}\x1b[0;31;40m{severities[severity]}: {message}\033[0;0m")
        exit(1)

# Input validation
if not os.path.isfile(args.in_video):
    log(f"Invalid in_video: {args.in_video}. in_video may not exist.", 3)
if os.path.isfile(args.out_video):
    log(f"Invalid out_video: {args.out_video}. out_video already exists.", 3)
if args.rotate not in [0, 90, 180, 270]:
    log(f"Invalid rotation value: {args.rotate}. Only rotation values of 90, 180, or 270 are accepted.", 3)

logl = ""
if args.verbose is True:
    logl = "info"
else:
    logl = "quiet"

# Open screen config generated in previous script
log("Loading JSON screen config...", 0)
with open(args.display_config_json, "r") as read_file:
    config = json.load(read_file)
    log("JSON screen config loaded.", 1)

    # Probe in_video
    print(args.in_video)
    probe = ffmpeg.probe(args.in_video, cmd=ffprobe_loc)

    # Look for applicable in_video streams
    video_stream_indicies = []
    for idx,stream in enumerate(probe["streams"]):
        if stream["codec_type"] == "video":
            video_stream_indicies.append(idx)
    log(f"Video streams detected on: {video_stream_indicies}", 0)

    # Multiple video streams unsupported
    if len(video_stream_indicies) > 1:
        log("More than one video stream detected. Spatial audio may be encoded to video tracks.", 3)
    elif len(video_stream_indicies) < 1:
        log("No video streams detected.", 3)

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
    log(f"Output resolution: {total_width}x{total_height}", 1)

    # If not preprocessed to output resolution, preprocess
    if in_video_width != total_width or in_video_height != total_height:
        log("Preprocessing...", 1)
        if not args.noaction:
            upscale = ffmpeg.input(args.in_video).filter("scale", width=total_width, height=total_height).filter("setsar", "1", "1").output("part-x.mp4", crf=args.crf, preset=args.preset, loglevel=logl).run(cmd="./bin/ffmpeg/ffmpeg.exe")

    # Create crops based on screen config, collect as inputs for concat step
    hstack = []
    for idx,screen in enumerate(config["screens"]):
        log(f"Processing screen ({idx + 1}/{len(config['screens'])}): {json.dumps(screen)}", 1)
        if not args.noaction:
            log(f"Cropping... size: ({screen['size']['x']}, {screen['size']['y']}) origin: ({screen['origin']['x']}, {screen['origin']['y']})", 0)
            out = ffmpeg.input("part-x.mp4").filter("crop", f"{screen['size']['x']}", f"{screen['size']['y']}", f"{screen['origin']['x']}", f"{screen['origin']['y']}")

            log(f"Rotating {args.rotate} degrees...", 1)
            if args.rotate == 90:
                out = out.filter("transpose", 1)
            elif args.rotate == 180:
                out = out.filter("transpose", 2).filter("transpose", 2)
            elif args.rotate == 270:
                out = out.filter("transpose", 2)
            out.output(f"part-{idx}.mp4", loglevel=logl).run(cmd="./bin/ffmpeg/ffmpeg.exe")

            hstack.append(ffmpeg.input(f"part-{idx}.mp4"))

    # If not keeping split, concatenate videos horizontally
    # TODO: Rotation options from screen config
    if not args.split:
        log(f"Merging {len(config['screens'])} screens...", 1)
        if not args.noaction:
            out = ffmpeg.filter(hstack, "hstack", "6").output(args.out_video, crf=args.crf, preset=args.preset, loglevel=logl).run(cmd="./bin/ffmpeg/ffmpeg.exe")

        # Clean up individual crops
        if not args.noaction:
            for idx,screen in enumerate(config["screens"]):
                os.remove(f"part-{idx}.mp4")

    # Clean up resolution preprocessing
    if not args.noaction:
            os.remove("part-x.mp4")
