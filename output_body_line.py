from fire import Fire
import re
import glob
import os


def parse_body_line(file_path):
    """
    ファイルからjsを除いたbodyのみを抽出
    """
    with open(file_path) as f:
        extract_flag = False
        extract_js_flag = False
        for line in f.readlines():
            if re.search(r'\<body', line):
                extract_flag = True

            if extract_flag:
                if re.search(r'\<script', line):
                    extract_js_flag = True

                if not extract_js_flag:
                    yield line

                if re.search(r'\<\/script\>', line):
                    extract_js_flag = False

            if re.search(r'\<\/body\>', line):
                break


def format_line(line):
    """
    仕様に合わせた整形処理
    """

    convert_line = re.sub(r"<br.*?>", '@@@', line)
    convert_line = re.sub(r"<[^>]*?>", '', convert_line)
    convert_line = convert_line.strip()

    return convert_line


def output_body_line(path):
    """
    指定したフォルダにあるhtmlファイルのbodyのみを抽出し、整形し、出力する
    """

    file_list = glob.glob(path + '/**/*.html', recursive=True)
    for file in file_list:
        lines = [format_line(line) for line in parse_body_line(file)]
        lines = filter(lambda a: a != "", lines)
        name, ext = os.path.splitext(file)
        with open(name + '.txt', 'w', encoding='utf-8') as f:
            # １行目にルートフォルダからのパスを記載してほしい（※２行目は空きで）
            f.write(file.split('target/')[1] + '\n\n')
            f.write("\n".join(lines))

if __name__ == '__main__':
    Fire(output_body_line)