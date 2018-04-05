import os
import re
import expressions as expr


def parse_video_stub_type(path):
    # Check for stub type (dvd, bluray ..)
    filename, ext = os.path.splitext(path)
    if ext in expr.stub_extensions:
        stbext = os.path.splitext(filename)[1].strip('.')
        for token in iter(expr.video_stub_types):
            if token == stbext:
                return expr.video_stub_types[token]
    return None


def parse_video_extra_type(path):
    # Check for extra type (trailer or sample)
    filename, ext = os.path.split(path)
    for re_token in iter(expr.video_extra_types):
        if re.search(re_token, filename):
            return expr.video_extra_types[re_token]
    return None


def parse_video_3d_type(path):
    # Check if video is 3D
    filename, ext = os.path.split(path)
    for token in expr.video_3d_types:
        if filename.find(token):
            return expr.video_3d_types[token]
    return None


def is_video_file(path):
    return lower(os.path.splitext(path)[1]) in expr.video_extensions


def is_stub_file(path):
    return lower(os.path.splitext(path)[1]) in expr.stub_extensions


def parse_video(path):
    if not path:
        raise RuntimeError('Missing path')
    if os.path.isdir(path):
        return None
    filename, ext = os.path.splitext(path)
    stubtype = None
    if ext not in expr.video_extensions:
        stubtype = parse_video_stub_type(path)
    container = ext.strip('.')
    name, year = expr.clean_year(path)
    format3D = parse_video_stub_type(path)
    xtype = parse_video_extra_type(path)
    # Do a second pas to extract name and year after cleaning the path string
    if not name or not year:
        name, year = expr.clean_year(expr.clean_string(path))
    name = os.path.split(name)[1]
    return {
        'name'      : name,
        'container' : container,
        'year'      : year,
        'path'      : path,
        'stubtype'  : stubtype,
        'format3D'  : format3D,
        'xtype'     : xtype
    }

def parse_video_stack(files):
    # Directories are skiped
    filelist = [f for f in files if not os.path.isdir(f)
                  and (is_video_file(f) or is_stub_file(f))].sort()
    stack_result = None
    for fname in filelist:
        fidx = 1
        for rexpr in expr.video_file_stack_expr:
            match = re.search(rexpr, fname)
            match_next = re.search(rexpr, filelist[fidx])
            if not match or match_next:
                continue
            title = match.group(1)
            volume = match.group(2)
            ignore = match.group(3)
            title_next = match_next.group(1)
            volume_next = match_next.group(2)
            ignore_next = match_next.group(3)
            if title == title_next \
                    and volume != volume_next \
                    and ignore == ignore_next:
                if os.path.splitext(fname) == os.path.splitext(filelist[fidx]):
                    stack_files = []
                    if not stack_result:
                        stack_files.append(fname)
                        stack_result = {
                            'name' : title,
                            'files' : stack_files
                        }
                    stack_files.append(filelist[idx])
            else:
                continue





def parse_video_list(files):
    pass


