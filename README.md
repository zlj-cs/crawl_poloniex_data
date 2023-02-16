## 并行获取poloniex中货币的价格信息
#### 使用时根据需要修改config中的如下变量:

- start: 爬取记录的开始时间
- end: 爬取记录的结束时间
- proxies: 代理，用来访问外网
- save_dir: 保存中间文件的目录
- save_path: 保存最终文件的路径
- topN: 保存过去24小时交易量最多的topN个虚拟货币
- process_num: 开启的进程数

使用如下命令
```
python crawl_poloniex.py
python poloniex_to_db.py
```