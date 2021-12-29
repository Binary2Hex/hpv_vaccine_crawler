#!/usr/bin/env python3
import requests
from string import Template
import json
from bs4 import BeautifulSoup
import logging
import re
import argparse

DEBUG = False
FORMAT = '%(asctime)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger(__name__)

USER_ID = 9755014559
BUYER_PHONE = 13127850312
BUYER_NAME = "蔡依林"
BUYER_CITY = "上海"
BUYER_ADDRESS = "浦东新区海阳西路500弄1号1202室"

GOODS_LIST = {
    "xh_hpv9": {
        "description": "徐汇HPV9价疫苗(3针)",
        "goods_id": 588001328,
        "sku_id": 36540375,
        "price": 500000,
        "banner_id": "seach.42679387~search~1~8Kkv1mNB",
        "slg": "consumer-search,standardModify,d929e020-c75d-d856-666e-6016e6dfa154,711.545_844d557e016c417fa910c9d407681243",
        "reft": "1640338541722",
        "spm": "seach.42679387",
        "uuid": "d929e020-c75d-d856-666e-6016e6dfa154",
        "alg_id": "",
        "pv_id": "",
    },
    "heart_300": {
        "description": "日常急救及心肺复苏 自动体外除颤课程(300)",
        "goods_id": 619888485,
        "sku_id": 36729387,
        "price": 30000,
        "banner_id": "ag.42679387~goods.2~7~HK0qZUXJ",
        "slg": "allGoodList,recommendSearch,9755014559,585_d41bd2ce8c334c65a19da2e741dae28a",
        "reft": "1640664629040_1640664645601",
        "spm": "seach.42679387_uc.42679387_ag.42679387",
        "uuid": "d929e020-c75d-d856-666e-6016e6dfa154",
        "alg_id": "0.0.0.0.0.0.681.268.401.456.582_0252eff2e34e4b13aefeffce5c5a1983",
        "pv_id": "/wscshop/showcase/homepage~0406e367-db82-4ad1-90c4-d80b37f96169",
    },
    "heart_1200": {
        "description": "拯救心脏课程(1200)",
        "goods_id": 619888485,
        "sku_id": 36729388,
        "price": 120000,
        "banner_id": "ag.42679387~goods.2~7~HK0qZUXJ",
        "slg": "allGoodList,recommendSearch,9755014559,585_d41bd2ce8c334c65a19da2e741dae28a",
        "reft": "1640664629040_1640664645601",
        "spm": "seach.42679387_uc.42679387_ag.42679387",
        "alg_id": "0.0.0.0.0.0.681.268.401.456.582_0252eff2e34e4b13aefeffce5c5a1983",
        "uuid": "d929e020-c75d-d856-666e-6016e6dfa154",
        "pv_id": "/wscshop/showcase/homepage~0406e367-db82-4ad1-90c4-d80b37f96169"
    },
    "gongjing_1300": {
        "description": " 宫颈筛查套餐(基础套餐)",
        "goods_id": 493719241,
        "sku_id": 36361958,
        "price": 130000,
        "banner_id": "ol.42679387~recService.1~18~q422cyk5",
        "slg": "consumer-search,standardModify,d929e020-c75d-d856-666e-6016e6dfa154,711.545_844d557e016c417fa910c9d407681243",
        "reft": "1640338541722",
        "spm": "seach.42679387",
        "uuid": "d929e020-c75d-d856-666e-6016e6dfa154",
        "alg_id": "",
        "pv_id": "",
    }
}

# BOOKKEY_PAYLOAD_TEMP = Template(
#     '{"goodsList":"[{\\\"goods_id\\\":$goods_id,\\\"num\\\":1,\\\"sku_id\\\":$sku_id,\\\"price\\\":$price,\\\"message_0\\\":\\\"$message_0\\\",\\\"message_1\\\":\\\"$message_1\\\",\\\"message_2\\\":\\\"$message_2\\\",\\\"message_3\\\":\\\"$message_3\\\",\\\"dcPs\\\":\\\"\\\",\\\"biz_trace_point_ext\\\":\\\"{\\\\\\\"atr_uuid\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"yzk_ex\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"page_type\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"tui_platform\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"tui_click\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"wecom_chat_id\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"wecom_uuid\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"from_source\\\\\\\":\\\\\\\"\\\\\\\",\\\\\\\"is_share\\\\\\\":\\\\\\\"1\\\\\\\",\\\\\\\"pv_id\\\\\\\":\\\\\\\"/wscshop/showcase/homepage~0406e367-db82-4ad1-90c4-d80b37f96169\\\\\\\",\\\\\\\"banner_id\\\\\\\":\\\\\\\"$banner_id\\\\\\\",\\\\\\\"slg\\\\\\\":\\\\\\\"$slg\\\\\\\",\\\\\\\"st\\\\\\\":\\\\\\\"js\\\\\\\",\\\\\\\"sv\\\\\\\":\\\\\\\"1.1.37\\\\\\\",\\\\\\\"yai\\\\\\\":\\\\\\\"wsc_c\\\\\\\",\\\\\\\"uuid\\\\\\\":\\\\\\\"d929e020-c75d-d856-666e-6016e6dfa154\\\\\\\",\\\\\\\"userId\\\\\\\":9755014559,\\\\\\\"platform\\\\\\\":\\\\\\\"web\\\\\\\",\\\\\\\"alg\\\\\\\":\\\\\\\"0\\\\\\\",\\\\\\\"reft\\\\\\\":\\\\\\\"$reft\\\\\\\",\\\\\\\"spm\\\\\\\":\\\\\\\"$spm\\\\\\\"}\\\",\\\"qr\\\":\\\"\\\",\\\"tpps\\\":\\\"\\\",\\\"fcode\\\":\\\"\\\",\\\"isSevenDayUnconditionalReturn\\\":false}]","common":"{\\\"kdt_id\\\":42679387,\\\"store_id\\\":0,\\\"store_name\\\":\\\"\\\",\\\"postage\\\":0,\\\"activity_alias\\\":\\\"\\\",\\\"activity_id\\\":0,\\\"activity_type\\\":0,\\\"use_wxpay\\\":0,\\\"from\\\":\\\"\\\",\\\"bosWorkFlow\\\":false}","extra":"{}"}')

GOODS_LIST_TEMP = {
    "goods_id": "",
    "num": 1,
    "sku_id": "",
    "price": 0,
    "message_0": "",
    "message_1": "",
    "message_2": "",
    "message_3": "",
    "dcPs": "",
    "biz_trace_point_ext": "",
    "qr": "",
    "tpps": "",
    "fcode": "",
    "isSevenDayUnconditionalReturn": False
}

biz_trace_point_ext = {
    "atr_uuid": "",
    "yzk_ex": "",
    "page_type": "",
    "tui_platform": "",
    "tui_click": "",
    "wecom_chat_id": "",
    "wecom_uuid": "",
    "from_source": "",
    "is_share": "1",
    "pv_id": "/wscshop/showcase/homepage~0406e367-db82-4ad1-90c4-d80b37f96169",
    "banner_id": "",
    "slg": "",
    "st": "js",
    "sv": "1.1.37",
    "yai": "wsc_c",
    "uuid": "d929e020-c75d-d856-666e-6016e6dfa154",
    "userId": 9755014559,
    "platform": "web",
    "alg": "0",
    "reft": "",
    "spm": ""
}

BOOKKEY_PAYLOAD_TEMP = {
    "goodsList": "",
    "common": "{\"kdt_id\":42679387,\"store_id\":0,\"store_name\":\"\",\"postage\":0,\"activity_alias\":\"\",\"activity_id\":0,\"activity_type\":0,\"use_wxpay\":0,\"from\":\"\",\"bosWorkFlow\":false}",
    "extra": "{}"
}

SUB_ORDER_PAYLOAD_TEMP_1 = Template(
    '{"version":2,"source":{"bookKey":"$book_key","clientIp":"101.86.209.178","fromThirdApp":false,"isWeapp":false,"itemSources":[{"activityId":0,"activityType":0,"bizTracePointExt":"{\\\"yai\\\":\\\"wsc_c\\\",\\\"st\\\":\\\"js\\\",\\\"sv\\\":\\\"1.1.31\\\",\\\"atr_uuid\\\":\\\"\\\",\\\"page_type\\\":\\\"\\\",\\\"banner_id\\\":\\\"$banner_id\\\",\\\"yzk_ex\\\":\\\"\\\",\\\"tui_platform\\\":\\\"\\\",\\\"tui_click\\\":\\\"\\\",\\\"uuid\\\":\\\"d929e020-c75d-d856-666e-6016e6dfa154\\\",\\\"userId\\\":$user_id,\\\"platform\\\":\\\"web\\\",\\\"from_source\\\":\\\"\\\",\\\"spm\\\":\\\"$spm\\\",\\\"reft\\\":\\\"$reft\\\",\\\"wecom_uuid\\\":\\\"\\\",\\\"alg\\\":\"common_by_realtime.behavior_expand_offline.0:20211124,esmm_1013.1.classify,0.710.0.0.0.0.0.0.0.268.401.456.582_af65c2c24bf9494183464638f6eaf117\",\"wecom_chat_id\":\"\"}","cartCreateTime":0,"cartUpdateTime":0,"gdtId":"","goodsId":1298308789,"pageSource":"","skuId":37814747}],"kdtSessionId":"YZ923162603746385920YZhXmavQhm","needAppRedirect":false,"orderType":0,"platform":"mobile","salesman":"","userAgent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Mobile Safari/537.36","bizPlatform":""},"config":{"bosWorkFlow":false,"containsUnavailableItems":false,"fissionActivity":{"fissionTicketNum":0},"paymentExpiry":0,"receiveMsg":true,"usePoints":false,"useWxpay":false,"buyerMsg":"","disableStoredDiscount":true,"storedDiscountRechargeGuide":true,"yzGuaranteeInfo":{"displayTag":{"IS_YZ_SECURED":"0","FREIGHT_INSURANCE_FREE":"0","IS_FREIGHT_INSURANCE":"0"},"freightInsurance":false,"mainSupportContent":[],"securedItemSnapshotList":[],"hideYzGuarantee":false,"page":"order"}},"usePayAsset":{},"items":[{"activityId":0,"activityType":0,"deliverTime":0,"extensions":{"ticketCalendarEffectiveTime":"2021年12月24日 - 2022年03月23日","OUTER_ITEM_ID":"10000"},"fCode":"","goodsId":1298308789,"isSevenDayUnconditionalReturn":false,"itemFissionTicketsNum":0,"itemMessage":"[\"1111777\",\"ABC\"]","kdtId":42679387,"num":1,"pointsPrice":0,"price":39800,"skuId":37814747,"storeId":0,"umpSkuId":0}],"seller":{"kdtId":42679387,"storeId":0},"ump":{"activities":[{"activityId":0,"activityType":0,"externalPointId":0,"goodsId":1298308789,"kdtId":42679387,"pointsPrice":0,"skuId":37814747,"usePoints":false}],"coupon":{},"useCustomerCardInfo":{"specified":false},"costPoints":{"kdtId":42679387,"usePointDeduction":true}},"newCouponProcess":true,"unavailableItems":[],"asyncOrder":false,"delivery":{"hasFreightInsurance":false,"contacts":{"id":54386058,"recipients":"蔡依伶","tel":"13127850312"},"expressTypeChoice":0},"confirmTotalPrice":39800,"extensions":{"IS_OPTIMAL_SOLUTION":"true","IS_SELECT_PRESENT":"0","SELECTED_PRESENTS":"[]","BIZ_ORDER_ATTRIBUTE":"{\"RISK_GOODS_TAX_INFOS\":\"0\"}"},"behaviorOrderInfo":{"bizType":158,"token":""}}')

item_source = {
    "activityId": 0,
    "activityType": 0,
    "bizTracePointExt": "{\"yai\":\"wsc_c\",\"st\":\"js\",\"sv\":\"1.1.31\",\"atr_uuid\":\"\",\"page_type\":\"\",\"banner_id\":\"uc.42679387~recService.1~2~kLwOpEko\",\"yzk_ex\":\"\",\"tui_platform\":\"\",\"tui_click\":\"\",\"uuid\":\"d929e020-c75d-d856-666e-6016e6dfa154\",\"userId\":9755014559,\"platform\":\"web\",\"from_source\":\"\",\"spm\":\"f.78535840_f.78535840_uc.42679387\",\"reft\":\"1640328220383_1640328771438\",\"wecom_uuid\":\"\",\"alg\":\"common_by_realtime.behavior_expand_offline.0:20211124,esmm_1013.1.classify,0.710.0.0.0.0.0.0.0.268.401.456.582_af65c2c24bf9494183464638f6eaf117\",\"wecom_chat_id\":\"\"}",
    "cartCreateTime": 0,
    "cartUpdateTime": 0,
    "gdtId": "",
    "goodsId": "",
    "pageSource": "",
    "skuId": ""
}

sub_order_source = {
    "bookKey": "",
    "clientIp": "101.86.209.178",
    "fromThirdApp": False,
    "isWeapp": False,
    "itemSources": "item_source",
    "kdtSessionId": "",
    "needAppRedirect": False,
    "orderType": 0,
    "platform": "mobile",
    "salesman": "",
    "userAgent": "None",
    "bizPlatform": ""
}

sub_order_payload_items = {
    "activityId": 0,
    "activityType": 0,
    "deliverTime": 0,
    "extensions": {
        "ticketCalendarEffectiveTime": "2021年12月24日 - 2022年03月23日", "OUTER_ITEM_ID": "10000"
    },
    "fCode": "",
    "goodsId": "None",
    "isSevenDayUnconditionalReturn": False,
    "itemFissionTicketsNum": 0,
    "itemMessage": "",
    "kdtId": "None",
    "num": 1,
    "pointsPrice": 0,
    "price": "None",
    "skuId": "None",
    "storeId": 0,
    "umpSkuId": 0
}

ump_activities = {
    "activityId": 0,
    "activityType": 0,
    "externalPointId": 0,
    "goodsId": "",
    "kdtId": "",
    "pointsPrice": 0,
    "skuId": "",
    "usePoints": False
}

SUB_ORDER_PAYLOAD_TEMP = {
    "version": 2,
    "source": "sub_order_source",
    "config": {
        "bosWorkFlow": False,
        "containsUnavailableItems": False,
        "fissionActivity": {
            "fissionTicketNum": 0
        },
        "paymentExpiry": 0,
        "receiveMsg": True,
        "usePoints": False,
        "useWxpay": False,
        "buyerMsg": "",
        "disableStoredDiscount": True,
        "storedDiscountRechargeGuide": True,
        "yzGuaranteeInfo": {
            "displayTag": {
                "IS_YZ_SECURED": "0",
                "FREIGHT_INSURANCE_FREE": "0",
                "IS_FREIGHT_INSURANCE": "0"
            },
            "freightInsurance": False,
            "mainSupportContent": [],
            "securedItemSnapshotList": [],
            "hideYzGuarantee": False,
            "page": "order"
        }
    },
    "usePayAsset": {},
    "items": [
        {
            "activityId": 0,
            "activityType": 0,
            "deliverTime": 0,
            "extensions": {
                "ticketCalendarEffectiveTime": "2021年12月24日 - 2022年03月23日", "OUTER_ITEM_ID": "10000"
            },
            "fCode": "",
            "goodsId": "None",
            "isSevenDayUnconditionalReturn": False,
            "itemFissionTicketsNum": 0,
            "itemMessage": "[\"1111777\",\"ABC\"]",
            "kdtId": "None",
            "num": 1,
            "pointsPrice": 0,
            "price": "None",
            "skuId": "None",
            "storeId": 0,
            "umpSkuId": 0
        }
    ],
    "seller": {
        "kdtId": "None",
        "storeId": 0
    },
    "ump": {
        "activities": "",
        "coupon": {},
        "useCustomerCardInfo": {
            "specified": False
        },
        "costPoints": {
            "kdtId": "None",
            "usePointDeduction": True
        }
    },
    "newCouponProcess": True,
    "unavailableItems": [],
    "asyncOrder": False,
    "delivery": {
        "hasFreightInsurance": False,
        "contacts": {
            "id": 54386058,
            "recipients": "蔡依伶",
            "tel": "13127850312",
            "groupHeader": False
        },
        "expressTypeChoice": 0
    },
    "confirmTotalPrice": "None",
    "extensions": {
        "IS_OPTIMAL_SOLUTION": "true",
        "IS_SELECT_PRESENT": "0",
        "SELECTED_PRESENTS": "[]",
        "BIZ_ORDER_ATTRIBUTE": "{\"RISK_GOODS_TAX_INFOS\":\"0\"}"
    },
    "behaviorOrderInfo": {
        "bizType": 158,
        "token": ""
    }
}


class HPVCrawler:
    def __init__(self, item_type):
        logger.info('Init Crawler')
        if DEBUG:
            logger.debug('In Debug mode')

        self.goods = GOODS_LIST[item_type]
        logger.info('Item type is ' + item_type + ", " + self.goods["description"])

        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                          'Chrome/96.0.4664.110 Safari/537.36 '
        # self.origin = 'https://shop42871555.m.youzan.com'
        self.kdt_id = 42679387
        # self.referer = 'https://shop42871555.m.youzan.com/wscgoods/detail/3f1njhruf76x7?banner_id=seach.42679387~search~1~8Kkv1mNB&words=hpv&alg=0&slg=consumer-search,standardModify,d929e020-c75d-d856-666e-6016e6dfa154,711.545_844d557e016c417fa910c9d407681243&reft=1640338541722&spm=seach.42679387'

        # self.referer = 'https://shop42871555.m.youzan.com/wscgoods/detail/3f1njhruf76x7?banner_id={banner_id}&words=hpv&alg=0&slg={slg}&reft={reft}&spm={spm}'.format(
        #     banner_id=self.banner_id, slg=self.slg, reft=self.reft, spm=self.spm)

        self.cookie = '_kdt_id_=42679387; KDTSESSIONID=YZ923162603746385920YZhXmavQhm; nobody_sign=YZ923162603746385920YZhXmavQhm; yz_log_uuid=d929e020-c75d-d856-666e-6016e6dfa154; yz_log_ftime=1640140716573; _canwebp=1; loc_dfp=be277df7a13669b2a2e87573618d4552; dfp=c117922171d88bef4ce95d0471d9253e; captcha_sid=YZ923949120421675008YZFpMSJQdQ; trace_sdk_context_banner_id=ag.42679387~goods.2~7~HK0qZUXJ; trace_sdk_context_slg=allGoodList,recommendSearch,9755014559,585_d41bd2ce8c334c65a19da2e741dae28a; open_token={"accessToken":"848acac2ef95ce91e9b67654549363","expires":604799,"scope":"item trade user utility shop item_category user_advanced trade_virtual pay_qrcode coupon present_advanced reviews courier notice_center","expiresRemind":604799}; Hm_lvt_679ede9eb28bacfc763976b10973577b=1640675008,1640675104,1640676273,1640761791; Hm_lpvt_679ede9eb28bacfc763976b10973577b=1640761791; yz_log_seqb=1640761809345; yz_log_seqn=7'

        self.book_key = None
        self.buy_url = None
        self.action_id = None
        self.session_id = None

    def get_book_key(self):
        logger.info('Getting bookId')
        url = "https://shop42871555.youzan.com/wsctrade/order/goodsBook.json?kdt_id={}".format(self.kdt_id)
        origin = 'https://shop42871555.m.youzan.com'

        # Referer should be useless
        # referer = 'https://shop42871555.m.youzan.com/wscgoods/detail/3f1njhruf76x7?banner_id={banner_id}&words=hpv&alg=0&slg={slg}&reft={reft}&spm={spm}'.format(
        #     banner_id=self.banner_id, slg=self.slg, reft=self.reft, spm=self.spm)

        biz_trace_point_ext["banner_id"] = self.goods["banner_id"]
        biz_trace_point_ext["slg"] = self.goods["slg"]
        biz_trace_point_ext["reft"] = self.goods["reft"]
        biz_trace_point_ext["spm"] = self.goods["spm"]

        GOODS_LIST_TEMP["goods_id"] = self.goods["goods_id"]
        GOODS_LIST_TEMP["sku_id"] = self.goods["sku_id"]
        GOODS_LIST_TEMP["price"] = self.goods["price"]
        GOODS_LIST_TEMP["message_0"] = BUYER_PHONE
        GOODS_LIST_TEMP["message_1"] = BUYER_NAME
        GOODS_LIST_TEMP["message_2"] = BUYER_CITY
        GOODS_LIST_TEMP["message_3"] = BUYER_ADDRESS
        GOODS_LIST_TEMP["biz_trace_point_ext"] = json.dumps(biz_trace_point_ext)

        goods_list = json.dumps([GOODS_LIST_TEMP])
        BOOKKEY_PAYLOAD_TEMP["goodsList"] = goods_list
        payload = json.dumps(BOOKKEY_PAYLOAD_TEMP, ensure_ascii=False)

        headers = {
            "Connection": "keep-alive",
            "User-Agent": self.user_agent,
            "Origin": origin,
            # "Referer": self.referer,
            "Cookie": self.cookie,
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*"
        }

        if DEBUG:
            # print(payload)
            res_text = '{"code":0,"msg":"ok","data":{"bookKey":"c48028be-0543-4459-863c-9980c97feaf2","buyUrl":"https://cashier.youzan.com/pay/wsctrade_buy?book_key=c48028be-0543-4459-863c-9980c97feaf2","url":"/wxpay/new_order"}}'
            res_json = json.loads(res_text)
        else:
            # res = requests.post(url, headers=headers, json=json.loads(payload.encode('utf-8')))
            res = requests.post(url, headers=headers, json=json.loads(payload))
            res_json = json.loads(res.text)

        if res_json["code"] == 0:
            self.book_key = res_json["data"]["bookKey"]
            self.buy_url = res_json["data"]["buyUrl"]
            logger.info('Received Data')
            logger.info('book_key: ' + self.book_key)
            logger.info('buy_url: ' + self.buy_url)
        else:
            logger.error('Failed to get bookId. Exit!')
            exit(1)

    def gen_order(self):
        logging.info('Generating order')
        url = 'https://cashier.youzan.com/pay/wsctrade_buy?kdt_id={kdt_id}&book_key={book_key}&bookKey={book_key}'.format(
            kdt_id=self.kdt_id, book_key=self.book_key)
        headers = {
            "Connection": "keep-alive",
            "User-Agent": self.user_agent,
            # "Referer": self.referer,
            "Cookie": self.cookie,
            "Accpet": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }

        if DEBUG:
            with open('/Users/suhan/Workspace/jolin/hpv_crawler/debug/check_order.html', 'r') as f:
                soup = BeautifulSoup(f.read(), "html.parser")
        else:
            res = requests.get(url, headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")

        if soup.title.contents[0].strip() == '确认订单':
            logger.info('Checking order')
            scripts = soup.findAll('script')
            for script in scripts:
                script_content = script.contents[0].strip()
                result = re.search(r'\{"actionId":"([\w-]+)".*"sessionId":"(\w+)"', script_content)
                if result:
                    self.action_id = result.group(1)
                    self.session_id = result.group(2)
                    break;
            logger.info('Get action_id: ' + self.action_id)
            logger.info('Get session_id: ' + self.session_id)
        else:
            logger.error('Failed to check order')
            exit(1)

    def submit_order(self):
        logger.info('Submitting Order')
        url = 'https://cashier.youzan.com/pay/wsctrade/order/buy/v2/bill-fast.json?kdt_id={}'.format(self.kdt_id)

        item_source["bizTracePointExt"] = json.dumps(biz_trace_point_ext)
        item_source["goodsId"] = self.goods["goods_id"]
        item_source["skuId"] = self.goods["sku_id"]

        sub_order_source["bookKey"] = self.book_key
        sub_order_source["itemSources"] = [item_source]
        sub_order_source["kdtSessionId"] = self.session_id
        sub_order_source["userAgent"] = self.user_agent
        SUB_ORDER_PAYLOAD_TEMP["source"] = sub_order_source

        sub_order_payload_items["goodsId"] = self.goods["goods_id"]
        sub_order_payload_items["itemMessage"] = "[\"{phone}\",\"{name}\",\"{city}\",\"{address}\"]".format(
            phone=BUYER_PHONE, name=BUYER_NAME, city=BUYER_CITY, address=BUYER_ADDRESS)
        sub_order_payload_items["kdtId"] = self.kdt_id
        sub_order_payload_items["price"] = self.goods["price"]
        sub_order_payload_items["skuId"] = self.goods["sku_id"]
        SUB_ORDER_PAYLOAD_TEMP["items"] = [sub_order_payload_items]

        SUB_ORDER_PAYLOAD_TEMP["seller"]["kdtId"] = self.kdt_id

        ump_activities["goodsId"] = self.goods["goods_id"]
        ump_activities["kdtId"] = self.kdt_id
        ump_activities["skuId"] = self.goods["sku_id"]
        SUB_ORDER_PAYLOAD_TEMP["ump"]["activities"] = [ump_activities]
        SUB_ORDER_PAYLOAD_TEMP["ump"]["costPoints"]["kdtId"] = self.kdt_id
        SUB_ORDER_PAYLOAD_TEMP["confirmTotalPrice"] = self.goods["price"]

        headers = {
            "Connection": "keep-alive",
            "User-Agent": self.user_agent,
            "x-yz-action-id": self.action_id,
            "Origin": "https://cashier.youzan.com",
            "Cookie": self.cookie,
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*"
        }

        res = requests.post(url, headers=headers, json=SUB_ORDER_PAYLOAD_TEMP)
        res_json = json.loads(res.text)
        if res_json['code'] != 0:
            logger.error('Failed to submit order')
            logger.error(res_json["msg"])
        else:
            logger.info('Congratulations. Submit order successfully!')

        logger.info('Save log to sub_order.log')
        with open('log/sub_order.log', 'w') as f:
            f.write(res.text)

        # if DEBUG:
        #     payload = json.dumps(SUB_ORDER_PAYLOAD_TEMP)
        #     logger.debug(payload)


def parse_args():
    parser = argparse.ArgumentParser(description='Parse options for crawler')
    parser.add_argument("type", choices=["xh_hpv9", "heart_300", "heart_1200", "gongjing_1300"],
                        help="Crawler type to order different items")
    parser.add_argument("--debug", dest='debug', action='store_true')
    args = parser.parse_args()
    return args


def crawler():
    global DEBUG
    args = parse_args()
    if args.debug:
        DEBUG = True

    hpv_crawler = HPVCrawler(args.type)
    hpv_crawler.get_book_key()
    hpv_crawler.gen_order()
    hpv_crawler.submit_order()


def main():
    crawler()


if __name__ == "__main__":
    main()
