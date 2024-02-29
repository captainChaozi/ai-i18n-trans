
import os
import json
import re
from langchain_core.language_models.llms import LLM
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import PlaywrightURLLoader, UnstructuredURLLoader


LLM = ChatGoogleGenerativeAI(
    model='gemini-pro', google_api_key='你自己的apikey')


def url_content(url):

    try:
        loader = PlaywrightURLLoader(
            urls=[url])

        data = loader.load()

        url_content = data[0].page_content
        return url_content
    except Exception as e:
        print(e)
        url_content = ''
    try:
        loader = UnstructuredURLLoader(
            urls=[url])

        data = loader.load()

        url_content = data[0].page_content
        return url_content
    except Exception as e:
        print(e)
        url_content = ''
    return url_content


def take_tran(json_data, lng):

    prompt = PromptTemplate(
        input_variables=["msg"],
        template="""你是一个{lng}翻译专家，非常善于把网站内容翻译成{lng}，严格翻译内容，符合{lng}的表达习惯，翻译成地道的{lng}
        请按照语种简称翻译下面 json的数据,然后只返回翻译后的json数据，该数据用于我的i18n网站的多语言翻译，
     
        --- 
        json数据如下：
        ```json
        {json_data}
        ```
        要求：严格翻译内容，符合{lng}的表达习惯，翻译成地道的{lng}
        翻译后的json数据:
        """,

    )
    chain = prompt | LLM

    return chain.invoke({'json_data': json_data, 'lng': lng}).content

# 定义函数，该函数接收命令行输入的 path 参数 然后读取path


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, )
    args = parser.parse_args()
    path = args.path
    zh = path + '/zh'
    # 读取en文件夹下的所有文件
    files = os.listdir(zh)
    # 遍历文件夹
    lngs = {
        "en": "English",
        "tw": "繁體中文",
        "ko": "한국어",
        "ja": "日本語",
        "pt": "Português",
        "es": "Español",
        "de": "Deutsch",
        "fr": "Français",
        "vi": "Tiếng Việt",
    }

    for lng, lng_name in lngs.items():

        for file in files:
            # 获取文件路径
            file_path = zh + '/' + file
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            flag = True

            while flag:
                try:
                    json_str = take_tran(content, lng_name)
                    # 去掉第一行和最后一行
                    json_tmp = json_str.split('\n')
                    json_str = '\n'.join(json_tmp[1:-1])
                    print(json_str)
                    lng_path = path + lng
                    if not os.path.exists(lng_path):
                        os.makedirs(lng_path)
                    with open(lng_path + '/' + file, 'w', encoding='utf-8') as f:
                        data = json.loads(json_str)
                        json.dump(data, f, ensure_ascii=False)
                    flag = False
                except Exception as e:
                    print(e)

                    continue


if __name__ == "__main__":
    main()


# python tran_json.py --path=/home/chao/work/coder/base64-utils/i18n/locales/
