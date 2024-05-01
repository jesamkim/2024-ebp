import unittest
import helpers.document_helper as doc_helper
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter


class MyTestCase(unittest.TestCase):
    def test_get_documents_by_parsing_excel(self):
        pass

    def test_get_file_list(self):
        result = doc_helper.get_file_list("./../../app/files")
        print(result)

    def test_get_merged_contents(self):
        result = doc_helper.get_merged_contents("./../../app/files/22-26_국제 신재생에너지 정책변화 및 시장 분석.pdf")
        print(result)

if __name__ == '__main__':
    unittest.main()
