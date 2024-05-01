import unittest
from app.services.bedrock_service import *
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter


class MyTestCase(unittest.TestCase):
    def test_invoke_llm(self):
        result = invoke_llm("당신은 영어를 한국어로 번역하는 전문 번역가입니다. I love programming.")
        print(result)

    def test_summarize_using_stuff(self):
        result = summarize_using_stuff(filepath="./../../app/files/22-26_국제 신재생에너지 정책변화 및 시장 분석.pdf",
                                       question="", max_tokens=4096,
                                       temperature=0.9, top_k=250, top_p=1
                                       )
        print(result["output_text"])

if __name__ == '__main__':
    unittest.main()
