import os


def read_input(input_file:str):
    target_file = ""
    start_and_end_timestapms = list()

    with open(input_file, 'r', encoding='utf-8') as file:
        isFirstLine = True

        for line in file:
            if len(line) == 0 or len(line) == 1:
                continue

            if isFirstLine:
                target_file = line.strip()
                isFirstLine = False

            else:
                start_and_end_timestapms.append(line.strip().split(';'))

    return target_file, start_and_end_timestapms


def convert_timestamp_to_seconds(timestamp:str):
    split = timestamp.split(':')
    hours = int(split[0])
    minutes = int(split[1])
    seconds = int(split[2])

    return hours * 3600 + minutes * 60 + seconds


def convert_seconds_to_timestamp(seconds:int):
    hours = seconds // 3600
    minutes = (seconds - 3600 * hours) // 60
    seconds = seconds - 3600 * hours - 60 * minutes

    return f'{hours}:{minutes}:{seconds}'


def get_time_diff(timestamp1, timestamp2):
    seconds1 = convert_timestamp_to_seconds(timestamp1)
    seconds2 = convert_timestamp_to_seconds(timestamp2)

    return seconds2 - seconds1


def convert_to_start_and_duration_timestamps(start_and_end_timestapms):
    start_and_duration_timestapms = list()

    for timestamp in start_and_end_timestapms:
        diff = get_time_diff(timestamp[0], timestamp[1])
        start_and_duration_timestapms.append((timestamp[0], convert_seconds_to_timestamp(diff)))

    return start_and_duration_timestapms


def get_filename_and_ending(file_path:str):
    last_dot_index = file_path.rfind(".")
    filename = file_path[:last_dot_index]
    ending = file_path[last_dot_index + 1:]
    print(ending)

    return filename, ending


def cut_video(input_file:str):
    target_file, start_and_end_timestapms = read_input(input_file)
    start_and_duration_timestamps = convert_to_start_and_duration_timestamps(start_and_end_timestapms)

    for i in range(len(start_and_duration_timestamps)):
        current = start_and_duration_timestamps[i]
        start = current[0]
        duration = current[1]


        filename, file_ending = get_filename_and_ending(target_file)

        # ffmpeg -ss 0:10:30 -i "13.mp4" -to 00:1:41 -c copy -avoid_negative_ts 1 "2_copy1.mp4"
        ffmpeg_command = f'ffmpeg -ss {start} -i "{target_file}" -to {duration} -c copy -avoid_negative_ts 1 "{filename}_copy{i}.{file_ending}"'
        print(ffmpeg_command)
        os.system(ffmpeg_command)

cut_video('input.txt')













