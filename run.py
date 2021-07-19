import csv
import pandas as pd
import datetime
from selenium import webdriver
from config.config import configs
import time
import psycopg2
from apscheduler.schedulers.blocking import BlockingScheduler
from ftplib import FTP



sched = BlockingScheduler()
config = configs()

def ftp_file(ip,user,passwd):

    ftp_client = FTP(ip)
    ftp_client.login(user=user, passwd=passwd)
    ftp_client.cwd("/export/everyday")
    file_name = "EMA20_B30_" + datetime.date.today().strftime('%Y%m%d') + "_" + datetime.date.today().strftime('%Y%m%d') + ".csv"
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
    driver.get(config["login_user"]["ssi_web_link"])
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
    volume_stock.send_keys(int(volume) * 100)
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
def log(p_result):
    f = open("log.txt", "a")
    f.write(datetime.date.today().strftime("%Y%m%d:%M%S")+"  "+p_result+"\n")
    f.close()
def main():
    f_result = stock_data(path_string())
    driver = webdriver.Chrome()
    auto_login(driver)
    for index, row in f_result.iterrows():
        if index > 0:
           if int(row[4]) != 0:
               print(row[0], row[4])
               auto_trade(driver, row[0], row[4])
    driver.close()
def run_schedule(hour, minute):
    @sched.scheduled_job('cron', hour=hour, minute=minute)
    def run_schedule_def():
        main()
if __name__ == "__main__":
#    hour = "09"
#    minute = "09"
#    run_schedule(hour,minute)
#   sched.start()
    try:
        ftp_file(config["login_user"]["ftp_ip"],config["login_user"]["ftp_user"],config["login_user"]["ftp_password"])
        main()
        log("Done")
    except (Exception) as error:
        log(str(error))








