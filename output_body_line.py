from fire import Fire
import re


def parse_body_line(file_path):
    """
    ファイルからbodyのみを抽出
    """
    with open(file_path) as f:
        extract_flag = False
        for line in f.readlines():
            if re.search(r'\<body', line):
                extract_flag = True

            if extract_flag:
                yield line

            if re.search(r'\<\/body\>', line):
                break


def exclude_html_tag(line):
    """
    htmlタグを排除する
    """
    return re.sub('\<.*?\>', '', line)


def output_body_line(path):
    """
    指定したフォルダにあるhtmlファイルのbodyのみを抽出し、整形し、出力する
    """

    lines = [exclude_html_tag(line) for line in parse_body_line(path + '/wiki.html')]

if __name__ == '__main__':
    Fire(output_body_line)