"""
❖ 請用 Python 撰寫一個 cli scrape 工具,須包含以下功能
➢ 指定 block 區間 , 且上限為 100 block (ex. 21442021 - 21442120)

➢ 抓出每個 block 的 Transaction Details 資訊 (Transaction Hash, Status,
Block, Timestamp, Transaction Action, Sponsored, From, To, Value,
Transaction Fee, Gas Price)
➢ 工具需支援指抓取特定 Method and/or Amount (0 或 not 0) 的 filter
➢ 將 scrape 的資訊寫入 Postgres or JSON file Note:
■ 使用 .env file 為工具的環境變數
■ 如選用 Postgres , 請用 docker-compose 啟動 Postgres , 並在 .env 設定
Postgres 的連線資訊
■ 如使用 JSON file , 工具需支援透過 .env 決定 JSON file 的 root path
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
from lxml import etree
import re
class ETHerScanLib:

    def __init__(self):
        #https://etherscan.io/txs?block=21643501&p=1
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)


    def go_to_url(self,url):
        self.driver.get(url)
        self.url = url


    def get_pagesource(self):
        self.page_source = self.driver.page_source


    def click_element(self):
        pass







    def bs4_xpath_pagesource(self):
        soup = BeautifulSoup(self.page_source, "html.parser")
        return etree.HTML(str(soup))


    def get_block_transactions_topic(self,bs4_pagesource):
        topic_elements = bs4_pagesource.xpath(("//div[@class='table-responsive']\
                                    //thead[@id='ContentPlaceHolder1_theadAllTransactionTable']//th//span"))
        print(f"topic_elements count : {len(topic_elements)}")
        topic_list = []
        for ele in topic_elements:
            ele_text = ele.text.strip().strip("\n")
            print(ele_text)
            # if ele_text == "":
            #     ele_text = ele.xpath("/div/span")[0].text.strip().strip("\n")
            #     if ele_text :
            #         print("aa",ele_text)
            #         topic_list.append(ele_text)
            # else:
            #     topic_list.append(ele_text)

        print(topic_list)
        #Transaction Hash	Method  Block Date Time (UTC) From To  Amount	Txn Fee


    def get_total_block_transactions_detail_for_one_block(self, current_page, total_page):
        if current_page != 1:
            pass
        else:
            while current_page <= total_page:
                pass





    def get_block_transactions_detail_for_one_page(self,bs4_pagesource):
        record_list = bs4_pagesource.xpath("//tbody[@class='align-middle text-nowrap']//tr")
        print(len(record_list))
        detail_list = []
        for record in record_list:
           # print(len(record.xpath(".//td")))
            #print(record.xpath(".//td[12]")[0].text)
            transaction_hash = "".join(record.xpath(".//td[2]")[0].itertext()).strip().strip("\n")
            method = "".join(record.xpath(".//td[3]")[0].itertext()).strip().strip("\n")
            block = "".join(record.xpath(".//td[4]")[0].itertext()).strip().strip("\n")
            timestamp = "".join(record.xpath(".//td[7]")[0].itertext()).strip().strip("\n")
            from_ = "".join(record.xpath(".//td[8]")[0].itertext()).strip().strip("\n")
            to_ = "".join(record.xpath(".//td[10]")[0].itertext()).strip().strip("\n")
            amount = "".join(record.xpath(".//td[11]/span")[0].itertext()).strip().strip("\n")
            txn_fee = "".join(record.xpath(".//td[12]")[0].itertext()).strip().strip("\n")

            detail_list.append([transaction_hash,method,block,timestamp,from_,to_,amount,txn_fee])
            #text_value = record.xpath(".//td[8]")[0].text
        print(detail_list)

        #1 ,2,3 ,4 ,7,9,10,11


    def get_current_page_and_total_page_number(self, bs4_pagesource) -> int:
        page_text = bs4_pagesource.xpath("//span[@class='page-link text-nowrap']")[1].text
        pattern = r'Page\s+(\d+)\s+of\s+(\d+)'
        match = re.search(pattern, page_text)
        print(match.group(1), match.group(2))
        if match:
            return int(match.group(1)), int(match.group(2))
        return None

    def check_if_page_is_final_page(self):
        #Page 2 of 4
        pass

    def check_if_the_block_exist(self,bs4_pagesource):
        no_match_text = ""
        try:
            no_match_text = bs4_pagesource.xpath("//h3[@class='h5']")[0].text
        except :
            pass
        if not(no_match_text and "no matching" in no_match_text) :
            return True



        #if "There are no matching entries"


    def run(self,url):
        self.go_to_url(url)
        self.get_pagesource()
        pagesource = self.bs4_xpath_pagesource()
        if not self.check_if_the_block_exist(pagesource):
            print("The block doesn't exist")

        self.get_toal_page_number(bs4_pagesource=pagesource)
        #self.get_block_transactions_detail(pagesource)
        #self.driver.wait(10)
        #self.get_block_transactions_topic(pagesource)




#ETHerScanLib().run(url="https://etherscan.io/txs?block=21643501") #https://etherscan.io/txs?block=22643501&p=1


ETHerScanLib().run(url="https://etherscan.io/txs?block=21671673")
