import time
import datetime
from poloniex import Poloniex
import pandas as pd
import os
from log_tool import log
from multiprocessing import Pool
import json
def parse_time(time_string):
    return time.mktime(datetime.datetime.strptime(time_string, "%Y/%m/%d").timetuple())

def unixToDatetime(unix_time):
    date_time = datetime.datetime.fromtimestamp(unix_time) # Unix Time
    return date_time

def get_chart_until_success(polo, coin_pair, start, period, end):
    is_connect_success = False
    chart = {}
    while not is_connect_success:
        try:
            chart = polo.returnChartData(coin_pair, period=period, start=start, end=end)
            is_connect_success = True
        except Exception as e:
            print(e)
    return chart

def crawl_test(proxies, 
               start, 
               end, 
               period=300, 
               coin_pair='USDT_BTC',
               save_dir=None):
    polo = Poloniex(proxies=proxies)
    save_path = os.path.join(save_dir, "{}.pkl".format(coin_pair))
    if os.path.exists(save_path):
        log.info("{} is already downloaded".format(coin_pair))
        return 
    log.info("start crawling coin_pair {}".format(coin_pair))
    log.info("start {}, end {}".format(start, end))
    res = []
    st_time = time.time()
    while start < end:
        ret = get_chart_until_success(polo, coin_pair, start, period, end)
        try:
            t = ret[0]['date']
        except:
            log.warning(ret)
            break
        log.debug("crwaling start_time: {}, end_time: {}".format(ret[0]['date'], ret[-1]['date']))
        end = int(t[:-3])
        # 如果开始时间大于等于结束时间，或者该货币的交易记录不存在了
        if end <= start or ret[0]['date'] == ret[-1]['date']:
            break
        res += ret
    log.info('{} is downloaded, time_cost: {}'.format(coin_pair, time.time() - st_time))
    if save_dir:
        pd.to_pickle(res, os.path.join(save_dir, "{}.pkl".format(coin_pair)))


def crawl_coin_list(polo: Poloniex, topN=30):
    dic = polo.return24hVolume()
    btc_coin_pair = []
    for coin_pair in list(dic.keys()):
        if coin_pair.startswith("BTC_"):
            btc_coin_pair.append((coin_pair, float(dic[coin_pair]['BTC'])))
        elif coin_pair.endswith("_BTC"):
            btc_coin_pair.append(("_".join(coin_pair.split('_')[::-1]), float(dic[coin_pair]['BTC'])))
    btc_coin_pair.sort(key= lambda x:x[1])
    return btc_coin_pair[:topN]

if __name__ == "__main__":
    with open("config.json") as file:
        config = json.load(file)
    # 设置代理, 用于访问外网
    proxies = config['proxies']
    # 创建实例
    polo = Poloniex(proxies=proxies)
    # 需要爬取的开始和结束时间
    end = parse_time(config['end'])
    start = parse_time(config['start'])
    save_dir = config['save_dir']
    topN = config['topN']
    process_num = config['process_num']
    btc_coin_pairs = crawl_coin_list(polo, topN=topN)
    with Pool(process_num) as p:
        res = p.starmap_async(crawl_test, [(proxies, start, end, 300, coin_pair, save_dir, ) for coin_pair, _ in btc_coin_pairs]).get()
        log.info('Waiting for all subprocesses done...')
    log.info('All subprocesses done.')

    # p.close()# 必须在join前使用close
    # p.join()# 等待p中进程全部完成