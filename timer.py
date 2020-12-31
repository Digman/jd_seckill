# -*- coding:utf-8 -*-
import time
import requests
import json

from datetime import datetime
from jd_logger import logger
from config import global_config


class Timer(object):
    def __init__(self, sleep_interval=0.5):
        self.buy_time = 0
        self.buy_time_ms = 0
        self.start_time = 0
        self.init_time()
        self.diff_time = self.local_jd_time_diff()
        self.sleep_interval = sleep_interval
        self.max_duration = int(global_config.getRaw('config', 'seckill_duration'))

    def init_time(self, t=None):
        # '2018-09-28 22:45:50'
        t = global_config.getRaw('config', 'buy_time') if not t else t
        self.buy_time = datetime.strptime(t, "%Y-%m-%d %H:%M:%S")
        self.buy_time_ms = int(time.mktime(self.buy_time.timetuple()) * 1000.0 + self.buy_time.microsecond / 1000) - 500

    def jd_time(self):
        """
        从京东服务器获取时间毫秒
        :return:
        """
        url = 'https://a.jd.com//ajax/queryServerData.html'
        ret = requests.get(url).text
        js = json.loads(ret)
        return int(js["serverTime"])

    def local_time(self):
        """
        获取本地毫秒时间
        :return:
        """
        return int(round(time.time() * 1000))

    def local_jd_time_diff(self):
        """
        计算本地与京东服务器时间差
        :return:
        """
        return self.local_time() - self.jd_time()

    def enabled(self):
        """
        根据抢购持续时间计算是否需要停止
        :return:
        """
        if self.max_duration == 0 or self.start_time == 0:
            return True

        duration = self.local_time() - self.start_time
        ret = self.max_duration > duration

        if not ret:
            logger.warning("已到达设置的抢购最大持续时间:%d毫秒，即将停止抢购", self.max_duration)

        return ret

    def start(self, title='抢购'):
        self.start_time = 0
        logger.info('正在等待到达设定{}时间:{}，检测本地时间与京东服务器时间误差为【{}】毫秒'.format(title, self.buy_time, self.diff_time))
        while True:
            # 本地时间减去与京东的时间差，能够将时间误差提升到0.1秒附近
            # 具体精度依赖获取京东服务器时间的网络时间损耗
            if self.local_time() - self.diff_time >= self.buy_time_ms:
                self.start_time = self.local_time()
                logger.info('时间到达，开始执行...')
                break
            else:
                time.sleep(self.sleep_interval)
