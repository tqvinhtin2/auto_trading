import csv
import pandas as pd
import datetime
from selenium import webdriver
from sqlalchemy import null
from config.config import configs
import time
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
from ftplib import FTP



sched = BlockingScheduler()


config = configs()

#p_str_path="D:\\automatic_stocks-master\EMA20_B30_"
p_str_path="EMA20_B30_"
p_str_link="https://webtrading.ssi.com.vn/"
ip="45.124.84.24"
user="tvinh"
passwd="123456"

def ftp_file(ip,user,passwd):

    ftp_client = FTP(ip)
    ftp_client.login(user=user, passwd=passwd)
    ftp_client.cwd("/export/everyday")
    print("test\n", ftp_client.cwd("/export/everyday/"))
    file_name = "EMA20_B30_" + datetime.date.today().strftime('%Y%m%d') + "_" + datetime.date.today().strftime('%Y%m%d') + ".csv"
    print(file_name)
    file_stream = open(file_name, "wb")  # read file to send to byte
    ftp_client.retrbinary('RETR {}'.format(file_name),file_stream.write,1024)
    file_stream.close()
    print("Download OK")
    ftp_client.close

def path_string():
    now=datetime.date.today().strftime('%Y%m%d')
    return p_str_path+now+"_"+now+".csv"
def stock_data(p_str_path):
    data = []
    with open(p_str_path, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            data.append(row)
        data = pd.DataFrame(data)
    return data
def auto_login(driver):
    driver.get(p_str_link)
    user = driver.find_element_by_id("name")
    user.send_keys(config["login_user"]["Username"])
    password = driver.find_element_by_id("txtPassword")
    password.send_keys(config["login_user"]["Password"])
    driver.find_element_by_id("btnLogin").click()
    time.sleep(10)
def auto_trade(driver,symbol,volume):
    if int(volume) > 0:
        driver.find_element_by_id("btnOrderBuy").click()
    elif int(volume) < 0:
        driver.find_element_by_id("btnOrderSell").click()
    code_stock = driver.find_element_by_id("txtStockSymbol")
    code_stock.send_keys(symbol)
    volume_stock = driver.find_element_by_id("txtOrderUnits")
    volume_stock.send_keys(int(volume) * 100)  # sao ở đây ông lại chuyển là float,
    price_stock = driver.find_element_by_id("txtOrderPrice")
    price_stock.send_keys("MP")
    pin_stock = driver.find_element_by_id("txtSecureCode")
    pin_stock.send_keys(config["login_user"]["Pin_code"])
    time.sleep(5)
    driver.find_element_by_id("btnOrder").click()
    time.sleep(5)
    button = driver.find_element_by_id('popup_ok')
    button.click()
    time.sleep(2)
    # driver.find_element_by_id("btnOrderBuy
    if int(volume) > 0:
        driver.find_element_by_id("btnOrderBuy").click()
    elif int(volume) < 0:
        driver.find_element_by_id("btnOrderSell").click()

def main():
    f_result = stock_data(path_string())
    op = webdriver.ChromeOption()
    op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    op.add_argument("--headless")
    op.add_argument("--no-sandbox")
    op.add_argument("--disabe-dev-sh-usage")
    driver = webdriver.Chrome(excecutable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=op)
    try:
        auto_login(driver)
        print(f_result)
        for index, row in f_result.iterrows():
            if index > 0:
                if int(row[4]) != 0:
                    print(row[0], row[4])
                    auto_trade(driver, row[0], row[4])
        driver.close()
    except (Exception) as error:
        print(error)

def run_schedule(hour, minute):
    @sched.scheduled_job('cron', hour=hour, minute=minute)
    def run_schedule_def():
        main()

if __name__ == "__main__":

#    hour = "09"
#    minute = "09"
#    run_schedule(hour,minute)
#   sched.start()

   ftp_file(ip,user,passwd)
   main()








