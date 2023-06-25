import os
import hashlib
import base64
import time


def random_string(num_bytes, output_len=None):
    b = os.urandom(num_bytes)
    h = hashlib.sha256(b).digest()[:16]
    s = base64.b32encode(h).lower().replace(b"=", b"").decode("utf-8")
    if not output_len:
        return s
    return s[:output_len]


def human_readable_filesize(b):
    thresh = 1024.0
    if b < thresh:
        return "{:.1f} B".format(b)
    units = ("KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB")
    u = 0
    b /= thresh
    while b >= thresh:
        b /= thresh
        u += 1
    return "{:.1f} {}".format(b, units[u])


def format_seconds(seconds):
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)

    human_readable = []
    if days:
        human_readable.append("{:.0f}d".format(days))
    if hours:
        human_readable.append("{:.0f}h".format(hours))
    if minutes:
        human_readable.append("{:.0f}m".format(minutes))
    if seconds or not human_readable:
        human_readable.append("{:.0f}s".format(seconds))
    return "".join(human_readable)


def estimated_time_remaining(bytes_downloaded, total_bytes, started):
    now = time.time()
    time_elapsed = now - started
    download_rate = bytes_downloaded / time_elapsed
    remaining_bytes = total_bytes - bytes_downloaded
    eta = remaining_bytes / download_rate
    return format_seconds(eta)
