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
import logging

from file_lib import *


class ETHerScanLib:

    def __init__(self):

        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        service = Service(ChromeDriverManager(driver_version="133.0.6943.142").install(
        ))
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def go_to_url(self, url):
        # https://etherscan.io/txs?block=21643501&p=1
        print(f"Go TO {url}")
        self.driver.get(url)

    def modify_url(self, url, block, page):
        # self.source_url = url
        url = f"{url}?block={block}&p={page}"
        return url

    def get_pagesource(self):
        self.page_source = self.driver.page_source

    def click_element(self):
        pass

    def bs4_xpath_pagesource(self):
        soup = BeautifulSoup(self.page_source, "html.parser")
        return etree.HTML(str(soup))

    def get_block_transactions_topic(self, bs4_pagesource):
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
        # Transaction Hash	Method  Block Date Time (UTC) From To  Amount	Txn Fee

    def get_total_block_transactions_detail_for_one_block(self, current_page, total_page):
        if current_page != 1:
            pass
        else:
            while current_page <= total_page:
                pass

    def amount_filter(self, amount_string: str, filter_mode):

        if not filter_mode:
            return amount_string
        elif filter_mode == "zero":
            if float(amount_string) == 0.0:
                return amount_string
        elif filter_mode == "nonzero":
            if float(amount_string) >= 0.0:
                return amount_string
        return None

    def method_filter(self, method_text, method_filter_strings):
        if not method_filter_strings:
            return method_text
        else:
            for s in method_filter_strings:
                if s == method_text:
                    return method_text
        return None

    def get_block_transactions_detail_for_one_page(self, bs4_pagesource,
                                                   method_filter_strings="",
                                                   amount_filter_mod="zero"):
        """
        method_filter_strings:
        - "" return all
        - "your_key_words" only reutrn the matching texts

        amount_filter:
        - "zero" only return zero value
        - "nonzero" only return  not zero value
        - "" return all

        """
        record_list = bs4_pagesource.xpath(
            "//tbody[@class='align-middle text-nowrap']//tr")
        print(len(record_list))
        detail_list = []
        for record in record_list:
           # print(len(record.xpath(".//td")))
            # print(record.xpath(".//td[12]")[0].text)
            transaction_hash = "".join(record.xpath(
                ".//td[2]")[0].itertext()).strip().strip("\n")
            # method = "".join(record.xpath(
            #     ".//td[3]")[0].itertext()).strip().strip("\n")

            method = record.xpath(".//td[3]/span/@data-title")[0]
            block = "".join(record.xpath(
                ".//td[4]")[0].itertext()).strip().strip("\n")
            timestamp = "".join(record.xpath(
                ".//td[7]")[0].itertext()).strip().strip("\n")
            # /address/0x0ada3111b866ff1ad0477f0c5d2e8ed35a36eb5b
            from_ = record.xpath(
                ".//td[8]//a/@href")[0].replace("/address/", "")
            to_ = record.xpath(
                ".//td[10]//a/@href")[0].replace("/address/", "")

            amount = "".join(record.xpath(
                ".//td[11]/span")[0].itertext()).strip().strip("\n")
            txn_fee = "".join(record.xpath(
                ".//td[12]")[0].itertext()).strip().strip("\n")

            method = self.method_filter(method, method_filter_strings)

            match = re.search(r"([\d.]+)", amount)
            if match:
                number = match.group(1)
                amount = self.amount_filter(number, amount_filter_mod)

            if method and amount != None:
                detail_list.append(
                    [transaction_hash, method, block, timestamp, from_, to_, amount, txn_fee])

        return detail_list

        # 1 ,2,3 ,4 ,7,9,10,11

    def get_current_page_and_total_page_number(self, bs4_pagesource) -> tuple:
        page_text = bs4_pagesource.xpath(
            "//span[@class='page-link text-nowrap']")[1].text
        pattern = r'Page\s+(\d+)\s+of\s+(\d+)'
        match = re.search(pattern, page_text)
        print(match.group(1), match.group(2))
        if match:
            return int(match.group(1)), int(match.group(2))
        return None

    def check_if_the_block_exist(self, bs4_pagesource):
        no_match_text = ""
        try:
            no_match_text = bs4_pagesource.xpath("//h3[@class='h5']")[0].text
        except:
            pass
        if not (no_match_text and "no matching" in no_match_text):
            return True

    def get_current_page_from_current_url(self, url):
        match = re.search(r"p=(\d+)", url)
        if match:
            p_value = match.group(1)
            print(f"p vlaue:{p_value}")
            return p_value
        else:
            print(f"Not find p value, url:{url}")
            raise ValueError

    def block_range_checker(self, block_range):
        # block_range = "21442021 - 21442120"

        block_start, block_end = block_range.replace(" ", "").split("-")
        if int(block_end) - int(block_start) > 100:
            raise ValueError(
                f"block range:{block_range} should be in range 100")
        return block_start, block_end

    def run_with_same_block(self, url, block, method_filter_strings="",
                            amount_filter_mod=""):
        self.source_url = url

        url = self.modify_url(url, block, page=1)
        self.go_to_url(url)
        self.get_pagesource()
        pagesource = self.bs4_xpath_pagesource()
        # #Test if block exist
        # https://etherscan.io/txs?block=21643501&p=1
        if not self.check_if_the_block_exist(pagesource):
            print("The block doesn't exist")
            return False
        page_nums = self.get_current_page_and_total_page_number(pagesource)
        total_page_number = page_nums[1]

        count_current_page = 1
        # Run every page from same block
        while count_current_page < total_page_number:
            count_current_page += 1
            page_nums = self.get_current_page_and_total_page_number(pagesource)
            if page_nums:
                total_page_number = page_nums[1]

                url = self.modify_url(
                    self.source_url, block, page=count_current_page)
                self.go_to_url(url)
                print(f"count_current_page:{count_current_page},\
                      total_page_number:{total_page_number}")
                pagesource = self.bs4_xpath_pagesource()
                data = self.get_block_transactions_detail_for_one_page(pagesource,
                                                                       method_filter_strings,
                                                                       amount_filter_mod)
                write_json_file(filepath=f"{block}.json", data=data, mode='a')
        return True

    def run(self, url, block, method_filter_strings="",
            amount_filter_mod=""):
        summary = {}
        block_start, block_end = self.block_range_checker(block_range)

        for block in range(int(block_start), int(block_end)+1):
            if self.run_with_same_block(url, block, method_filter_strings,
                                        amount_filter_mod):
                summary[f"{block}"] = True
            else:
                summary[f"{block}"] = False

        time.sleep(30)


if __name__ == "__main__":
    pass
    # ETHerScanLib().run(url="https://etherscan.io/txs?block=21643501") #https://etherscan.io/txs?block=22643501&p=1
    # ETHerScanLib().run(url="https://etherscan.io/txs", block=21671673)
