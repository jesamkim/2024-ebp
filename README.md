# 2024 AWS Enterprise Boost Program

## Amazon Bedrock & RAG sample codes
> <i> provided by Jesam Kim, Kichul Kim, Jisun Choi</i>


### Clone and use this notebooks
> Amazon SageMaker JupyterLab에서 File > New > Terminal을 클릭하여 "시스템 터미널"을 열어 다음과 같이 이 레포지토리를 복제(clone) 합니다.
<br>


```bash
cd SageMaker
git clone https://github.com/jesamkim/2024-ebp.git

```

---

## <i>[01_bedrock_fundamental.ipynb](./01_bedrock_fundamental.ipynb)</i>
* 기본 1 : 기본적인 형태로 Bedrock의 Claude 3 모델 클라이언트를 생성하고 호출하는 방법을 확인 합니다.
* 기본 2 (중요) : LangChain을 활용하여 Bedrock의 Claude 3 모델을 호출하는 방법을 확인 합니다.


## <i>[02_OpenSearch_setup.ipynb](./02_OpenSearch_setup.ipynb)</i>
* RAG를 위한 OpenSearch Cluster를 생성 합니다.


## <i>[03_RAG_OpenSearch.ipynb](./03_RAG_OpenSearch.ipynb)</i>
* 앞서 생성한 OpenSearch를 활용해 RAG를 구성 합니다.
* 시맨틱 검색, 어휘 검색, 하이브리드 검색 기법을 확인 합니다.


## <i>[04_web_crawling.ipynb](./04_web_crawling.ipynb)</i>
* beautifulsoup 라이브러리를 이용한 웹크롤링 샘플 코드 입니다.
* 샘플 코드에서는 google 검색에 대한 결과 페이지를 가져오는 내용 입니다.

---


## 템플릿
* 아래 ToDo_1, ToDo_2 노트북은 각각 웹크롤링 후 S3 업로드, RAG 구현 단계를 만드는 템플릿 노트북 입니다.
* 이 곳에 팔요한 코드를 채워서 템플릿의 Flow를 따라서 완성하는 것을 권장 드립니다.

### <i>[ToDo_1_Crawling-Summary-Tableau.ipynb](./ToDo_1_Crawling-Summary-Tableau.ipynb)</i>



### <i>[ToDo_2_RAG-QnA.ipynb](./ToDo_2_RAG-QnA.ipynb)</i>


<br><br>

[참조] 본 노트북의 소스 코드들은 [aws-ai-ml-workshop-kr](https://github.com/aws-samples/aws-ai-ml-workshop-kr)의 컨텐츠를 참조하였습니다.


