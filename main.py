import sys
from jd_spider_requests import JdSeckill
from jd_logger import logger


if __name__ == '__main__':
    try:
        a = """
功能列表：                                   
 +---+-----------------------+                                                                        
 | 1 | 预约商品              |
 +---+-----------------------+
 | 2 | 秒杀抢购商品          |
 +---+-----------------------+
 | 3 | 推送测试              |
 +---+-----------------------+
        """
        print(a)
        choice_function = input('请选择[1-3]: ')
        jd_seckill = JdSeckill()
        if choice_function == '1':
            jd_seckill.reserve()
        elif choice_function == '2':
            jd_seckill.seckill_by_proc_pool()
        elif choice_function == '3':
            jd_seckill.test_message()
        else:
            print('没有此功能')
            sys.exit(1)
    except KeyboardInterrupt:
        logger.warning('Keyboard Interrupt')
        sys.exit(0)
