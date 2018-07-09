import json

import requests


def get_html(keyword, start):
    """获取网页源代码

    """
    url = "https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}"
    new_url = url.format(keyword, start)
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
    }
    try:
        response = requests.get(new_url, headers=headers)
        if response.status_code == 200:
            html = response.json()
            result = json.dumps(html, indent=4)
            return result
    except requests.ConnectionError:
        return None


def write_into_file(result):
    """写入文件

    """
    with open("result.json", "w", encoding="utf-8") as f:
        f.write(result)


def main():
    """主函数

    """
    # 可以修改的测试值 start=24
    keyword = "测试"
    start = 0
    result = get_html(keyword, start)
    write_into_file(result)


if __name__ == "__main__":
    print('*'*20, 'begin', '*'*20, '\n')
    print('author: Chris\n')
    print('*'*47)
    main()
    print('*'*21, 'end', '*'*21, '\n')