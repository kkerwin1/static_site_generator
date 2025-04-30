import os, shutil, sys

from blocknode import heading_regex, markdown_to_html_node

def extract_title(markdown):
    """
    Given the text of a single markdown file, extract the title
    from the H1 header.

    :param markdown: Markdown text to parse
    :type markdown: str, required

    :returns: Text containing title
    :rtype: str

    :raises SyntaxError: If no H1 tag is found in markdown text
    """

    line_list = markdown.split("\n")
    for line in line_list:
        _match = heading_regex.match(line)
        if _match:
            hashes = _match[1]
            text = _match[2]
            num_hashes = len(hashes)
            if num_hashes == 1:
                return text
    raise SyntaxError("Invalid Markdown Syntax: No H1 Markdown tag")

def copy_static_tree(src_path, dest_path):
    """
    Recursively copy a directory tree.

    :param src_path: Directory to copy from
    :type src_path: str, required

    :param dest_path: Directory to copy to
    :type dest_path: str, required
    """

    if os.path.exists(src_path):
        os.mkdir(dest_path)
        dir_list = os.listdir(src_path)
        for path_name in dir_list:
            _src_path = src_path + "/" + path_name
            _dest_path = dest_path + "/" + path_name
            if os.path.isfile(_src_path):
                _path = shutil.copy(_src_path, _dest_path)
            if os.path.isdir(_src_path):
                copy_static_tree(_src_path, _dest_path)

def create_child_dirs(dest_path):
    """
    Check if parent directories of dest_path exist. If not,
    create them.

    :param dest_path: Path to check/create
    :type dest_path: str, required
    """

    path_list = dest_path.split("/")
    # Pop off file name at end of path_list
    file_name = path_list.pop()
    _path = ""
    for dir_name in path_list:
        _path = _path + dir_name + "/"
        if not os.path.exists(_path):
            os.mkdir(_path)

def generate_page(src_path, template_path, dest_path, basepath):
    """
    Generate an HTML page, and place it at dest_path.

    :param src_path: Path to read the markdown file from
    :type src_path: str, required

    :param template_path: Path to read the template html file from
    :type template_path: str, required

    :param dest_path: Path to write resulting html file to
    :type dest_path: str, required
    """

    print(
        f"Generating page from {src_path} to {dest_path} using {template_path}"
    )
    create_child_dirs(dest_path)

    src_text = ""
    with open(src_path) as src_file:
        src_text = src_file.read()
    
    template_text = ""
    with open(template_path) as template_file:
        template_text = template_file.read()
    
    title = extract_title(src_text)
    src_html_node = markdown_to_html_node(src_text)
    src_html_text = src_html_node.to_html()

    content_text = template_text.replace("{{ Title }}", title)
    content_text = content_text.replace("{{ Content }}", src_html_text)
    content_text = content_text.replace('href=/"', f'href="{basepath}/')
    content_text = content_text.replace('src=/"', f'src="{basepath}/')


    with open(dest_path, "w") as dest_file:
        dest_file.write(content_text)

def generate_html_tree(src_tree_root, template_path, dest_tree_root, basepath):
    """
    Given the root of a tree of markdown file, iterate over all markdown files in the root, and generate html pages from them in the dest_tree_root.

    :param src_tree_root: Source directory to search for markdown files in
    :type src_tree_root: str, required

    :param template_path: Path to template.html
    :type template_path: str, required

    :param dest_tree_root: Destination directory to place converted html files
    :type dest_tree_root: str, required
    """

    dir_list = os.listdir(src_tree_root)
    for path_name in dir_list:
        _src_path = src_tree_root + "/" + path_name
        _dest_path = dest_tree_root + "/" + path_name
        if os.path.isfile(_src_path):
            # Change .md file type to .html file type
            _dest_path = _dest_path.replace(".md", ".html")
            generate_page(_src_path, template_path, _dest_path, basepath)
        if os.path.isdir(_src_path):
            generate_html_tree(_src_path, template_path, _dest_path, basepath)

def main():
    try:
        shutil.rmtree("docs")
    except FileNotFoundError:
        pass

    try:
        basepath = sys.argv[1]
    except IndexError:
        basepath = "/"

    copy_static_tree("static", "docs")
    generate_html_tree("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()