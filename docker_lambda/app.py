from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import pandas as pd
import warnings
import trafilatura
import boto3
#from langchain_aws import ChatBedrock
from langchain_community.chat_models import BedrockChat
from botocore.config import Config
from bs4 import BeautifulSoup


def get_driver():
    # Selenium 드라이버 옵션 설정
    options = webdriver.ChromeOptions()
    options.binary_location = './chrome-linux64/chrome' # 크롬 브라우저 경로 지정
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')

    # 크롬 드라이버 경로 설정
    service = Service("./chromedriver-linux64/chromedriver")
    crawling_driver = webdriver.Chrome(service=service, options=options)
    
    return crawling_driver
    

def main():
    from datetime import date
    # 오늘 날짜 가져오기 (YYYY-MM-DD)
    today = date.today().strftime('%Y-%m-%d')
    
    # 버킷 이름
    bucket_name = 'jesamkim-temp-20240409'
    
    # Bedrock 리전
    bedrock_region = 'us-west-2'
    
    
    # 크롬 드라이버 서비스 객체 생성
    service = Service("./chromedriver-linux64/chromedriver")

    # 크롬 드라이버 실행    
    driver = get_driver()
    print("chrome driver 실행 완료\n")
    
    warnings.filterwarnings('ignore')

    words = ['BESS project']  # 'solar PV project' #,'AUSTRALIA SOLAR FARM','AUSTRALIA BESS','SAUDI PV','SAUDI SOLAR FARM','SAUDI BESS','nuclear power plant']

    word_list = []
    title_list = []
    content_list = []
    link_list = []
    date_list = []

    url = 'https://www.google.com/search?q={}&newwindow=1&sca_esv=600662400&tbs=cdr:1,cd_min:1/1/2024,cd_max:4/16/2024&tbm=nws&ei=vGmvZaObBLPd1e8PirSVkAY&start={}&sa=N&ved=2ahUKEwij6Ye5_fKDAxWzbvUHHQpaBWI4KBDy0wN6BAgEEAQ&biw=1536&bih=735&dpr=1.25'
    # 날짜 설정

    for word in words:
        page = 1
        for i in range(0, 60, 10):  # 페이지 수
            # url {}에 순서대로 word,i 넣기
            new_url = url.format(word, i)

            # 크롬 드라이버에 url 주소 넣고 실행
            driver.get(new_url)

            # 페이지가 완전히 로딩되도록 3초동안 기다림
            time.sleep(3)

            print("*" * 10 + str(page) + "*" * 10)
            page = page + 1

            titles = driver.find_elements(By.CLASS_NAME, 'n0jPhd.ynAwRc')
            for title in titles:
                word_list.append(word)
                title_list.append(title.text.replace(",", ""))
                # print(title.text) # 기사 제목 확인

            contents = driver.find_elements(By.CLASS_NAME, 'GI74Re.nDgy9d')
            for content in contents:
                content_list.append(content.text.replace(",", ""))

            dates = driver.find_elements(By.CLASS_NAME, 'OSrXXb.rbYSKb.LfVVr')
            for date in dates:
                date_list.append(date.text.replace(",", ""))

            links = driver.find_elements(By.CLASS_NAME, 'WlydOe')
            for link in links:
                link_list.append(link.get_attribute('href'))

            if page == 32:  # 페이지 수정
                break

    # 링크내 기사 본문 갖고 오기
    def extract_content(link_list):
        content_full = []
        for link in link_list:
            try:
                downloaded = trafilatura.fetch_url(link)
                extracted = trafilatura.extract(downloaded)
                content_full.append(extracted)
            except:
                content_full.append(None)
        return content_full

    content_full = extract_content(link_list)

    data = {'WORD': word_list, 'TITLE': title_list, 'CONTENT': content_list, 'CONTENT_FULL': content_full,
            'LINK': link_list, 'DATE': date_list}
    df = pd.DataFrame(data)
    df.to_csv(f"{today}_origin.csv", encoding="utf-8-sig")  # 일별 파일명설정
    df.to_excel(f"{today}_origin.xlsx")

    driver.quit()

    config = Config(read_timeout=1000)

    def parsing_data(content):
        summary_list = []
        summary_kor_list = []
        country_list = []
        city_list = []
        soup = BeautifulSoup(content, 'html.parser')

        for i in range(0, len(content_full)):
            summary = soup.find(f'summary_{i}')
            # summary_kor = soup.find(f'summary_kor_{i}')
            city = soup.find(f'city_{i}')
            country = soup.find(f'country_{i}')
            if summary:
                summary_list.append(summary.text.strip())

                country_list.append(country.text.strip() if country is not None else 'NaN')
                city_list.append(city.text.strip() if city is not None else 'NaN')

                # summary_kor_list.append(summary.text.s trip())
                # country_list.append(country.text.strip())
                # city_list.append(city.text.strip())
        # print(summary_list)
        print(city_list)
        return summary_list, country_list, city_list

    def get_text_response(input_content):
        llm = BedrockChat(
            region_name=bedrock_region,
            model_id="anthropic.claude-3-haiku-20240307-v1:0",
            model_kwargs={
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,  # maximum : 4096
                "temperature": 0,
                "top_p": 0.01,
                "top_k": 0,
            },
            config=config
        )
        return llm.predict(input_content)

    response_content = []
    total_summary_list = []
    total_country_list = []
    total_city_list = []

    for start in range(0, 101, 10):
        end = start + 10
        content_prompt = ""
        for doc_i in range(start, end):
            if doc_i < len(content_full):
                content_prompt += f"""<content_{doc_i}>{content_full[doc_i]}</content_{doc_i}>"""

        prompt = f"""

        다음 <content></content> 태그 안에 있는 본문의 내용을 <instructions></instructions> 지침에 따라 자세한 요약 메모를 작성하세요:

        <content> 
        {content_prompt}
        </content> 

        <instructions>
          각 <content> 기사의 주요 내용을 3~5문장으로 영어로 요약하고 요약 내용을 list에 삽입해줘.  
          요약시 상세한 숫자를 기입해서 작성해줘.
          각 <content> 에서 해당 국가정보와 도시정보가 있으면 국가정보는 country에, 도시정보는 city에 각각 영어로 한개의 값만 list에 삽입해주고 해당 정보가 없으면 'null'으로 처리해줘.

          summary list 는 <summary_NUMBER> 태그 안에 넣어서 출력해줘
          country list 는 <country_NUMBER> 태그 안에 넣어서 출력해줘
          city list 는 <city_NUMBER> 태그 안에 넣어서 출력해줘
        </instructions>


        """

        response = get_text_response(input_content=prompt)
        response_content.append(response)

    for i, content in enumerate(response_content):
        # print(f"Response {i}:")
        # print(content)
        summary_list, country_list, city_list = parsing_data(content)
        total_summary_list.extend(summary_list)
        total_country_list.extend(country_list)
        total_city_list.extend(city_list)

    print(len(total_summary_list))
    
    

    data2 = {'SUMMARY': total_summary_list, 'COUNTRY': total_country_list, 'CITY': total_city_list}
    df2 = pd.DataFrame(data2)

    df0 = pd.concat([df, df2], axis=1)
    df0.to_csv(f"{today}_news_result.csv", encoding="utf-8-sig")

    df0.to_excel(f"{today}_news_result.xlsx")

    s3 = boto3.client('s3')
    

    # 오늘 날짜 디렉토리 경로
    prefix = today + '/'
    
    # S3 버킷에 디렉토리 생성
    try:
        s3.put_object(Bucket=bucket_name, Key=prefix)
        print(f"디렉토리 {prefix} 생성 완료")
    except Exception as e:
        print(e)

    # 로컬 폴더의 모든 xlsx 파일 업로드
    for filename in os.listdir(f'./'):
        if filename.endswith('.xlsx'):
            local_path = os.path.join(f'./', filename)
            s3_path = os.path.join(prefix, filename)
            try:
                s3.upload_file(local_path, bucket_name, s3_path)
                print(f"파일 {filename} 업로드 완료")
            except Exception as e:
                print(e)

if __name__ == "__main__":
    main()
