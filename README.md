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




## 금주 내 시퀀스 다이어그램, 크롤링 샘플코드 부분도 공유 예정 입니다.


<br><br>

[참조] 본 노트북의 소스 코드들은 [aws-ai-ml-workshop-kr](https://github.com/aws-samples/aws-ai-ml-workshop-kr)의 컨텐츠를 참조하였습니다.


