import datetime
import json
import time
import tzlocal
import dateutil.parser
import multiprocessing as mp
import requests
import sqlite3
from multiprocessing.managers import SyncManager
from queue import PriorityQueue


features = ["id", "created_at", "reblogs_count", "language", "content"]
TIME_ZONE = tzlocal.get_localzone()


class MyManager(SyncManager):
    pass


MyManager.register("PriorityQueue", PriorityQueue)


def Manager():
    m = MyManager()
    m.start()
    return m

def filter_toot(toot):
    output_toot = dict()

    for feature in features:
        if feature in toot:
            output_toot[feature] = toot[feature]
        else:
            return None
    return output_toot


def to_db_converter(instance):
    def to_db_columns(toot):
        id = int(toot['id'])
        created_at = dateutil.parser.parse(toot['created_at'])
        added_at = datetime.datetime.utcnow()
        content = toot['content']
        language = toot['language']
        reblogs_count = int(toot['reblogs_count'])
        return id, created_at, added_at, content, language, reblogs_count, instance
    return to_db_columns


class InstanceCrawler(object):
    def __init__(self, instance_address, start_time, crawl_interval=datetime.timedelta(hours=2)):
        self.start_time = start_time
        self.crawled_up_to_id = None
        self.crawled_from_id = None
        self.crawled_up_to_date = None
        self.crawled_all_preceding = False
        self.instance_active = True
        self.instance_address = instance_address
        self.crawl_interval = crawl_interval

    def crawl(self):
        if not self.crawled_all_preceding:
            if self.crawled_from_id is not None:
                self.crawl_backwards()
            else:
                self.crawl_forwards()
        else:
            if self.crawled_up_to_date is not None and self.crawled_up_to_date + self.crawl_interval > datetime.datetime.now(tz=TIME_ZONE):
                time_delta = (self.crawled_up_to_date + self.crawl_interval) - datetime.datetime.now(tz=TIME_ZONE)
                print("WAIT\t Waiting for %d seconds until next crawl."%(time_delta.total_seconds()))
                time.sleep(time_delta.total_seconds())
            self.crawl_forwards()

    def crawl_forwards(self):
        print("FORWARD_CRAWL_START\t Starting forward crawl on %s."%self.instance_address)
        try:
            if self.crawled_up_to_id is not None:
                r = requests.get("http://"+self.instance_address+"/api/v1/timelines/public", {'local': True, 'since_id': self.crawled_up_to_id, 'limit': 40}, timeout=(3, 27))
            else:
                r = requests.get("http://"+self.instance_address+"/api/v1/timelines/public", {'local': True, 'limit': 40}, timeout=(3, 27))
        except Exception:
            print("CONNECT_ERROR Instance %s is down."%self.instance_address)
            self.instance_active = False
            return
        try:
            content = json.loads(r.text)
        except json.JSONDecodeError as e:
            print("JSON_ERROR\t Instance: %s "%self.instance_address)
            self.instance_active = False
            return

        if not r.status_code == requests.codes.ok:
            print("ERROR Instance %s returned bad status code."%self.instance_address)
            self.instance_active = False
            return

        content = list(filter(lambda x: x is not None, map(filter_toot, content)))

        # TODO: Filter out all toots that are too old and don't set the flag correctly if we have all toots from start time
        self.crawled_up_to_date = datetime.datetime.now(tz=TIME_ZONE)
        if len(content) == 0:
            self.crawled_all_preceding = True
            print("ZEROLENGTH\t Crawl from instance %s returned zero-length array."%self.instance_address)
            return

        i = 0
        date = dateutil.parser.parse(content[i]["created_at"])
        while date is None or date > self.start_time:
            i += 1
            if i == len(content):
                break
            date = dateutil.parser.parse(content[i]["created_at"])

        self.crawled_all_preceding = len(content) != i
        print("Set crawled all preceding to ", self.crawled_all_preceding)
        if i != 0:
            content = content[:i]
        else:
            content = []
        if len(content) == 0:
            print("ZEROLENGTH_TIME\t Crawl from instance %s returned zero-length array after time filtering."%self.instance_address)
            return

        if self.crawled_from_id is None:
            self.crawled_from_id = content[-1]["id"]
        self.crawled_up_to_id = content[0]["id"]
        db = sqlite3.connect("data/toots.db")
        db.executemany("INSERT INTO raw_toots VALUES (?,?,?,?,?,?,?)", list(map(to_db_converter(self.instance_address), content)))
        db.commit()
        db.close()
        print("FORWARD_CRAWL_FINISH\t Finished forward crawl on %s, %d new toots acquired." % (self.instance_address, len(content)))

    def crawl_backwards(self):
        print("BACKWARD_CRAWL_START\t Starting backward crawl on %s."%self.instance_address)
        try:
            if self.crawled_from_id is not None:
                r = requests.get("http://"+self.instance_address+"/api/v1/timelines/public", {'local': True, 'max_id': self.crawled_from_id, 'limit': 40}, timeout=(3, 27))
            else:
                r = requests.get("http://"+self.instance_address+"/api/v1/timelines/public", {'local': True, 'limit': 40}, timeout=(3, 27))
        except Exception:
            print("CONNECT_ERROR Instance %s is down."%self.instance_address)
            self.instance_active = False
            return

        if not r.status_code == requests.codes.ok:
            print("ERROR Instance %s returned bad status code."%self.instance_address)
            self.instance_active = False
            return

        try:
            content = json.loads(r.text)
        except json.JSONDecodeError as e:
            print("JSON_ERROR\t Instance: %s "%self.instance_address)
            self.instance_active = False
            return

        # TODO: Language flag not found in some instances, plz fix...
        content = list(filter(lambda x: x is not None,map(filter_toot, content)))
        self.crawled_up_to_date = datetime.datetime.now(tz=TIME_ZONE)

        if len(content) == 0:
            print("ZEROLENGTH\t Crawl from instance %s returned zero-length array."%self.instance_address)
            self.crawled_all_preceding = True
            return

        i = 0
        date = dateutil.parser.parse(content[i]["created_at"])
        while date is None or date > self.start_time:
            i += 1
            if i == len(content):
                break
            date = dateutil.parser.parse(content[i]["created_at"])

        self.crawled_all_preceding = len(content) != i
        if i != 0:
            content = content[:i]
            self.crawled_from_id = content[i-1]["id"]
        else:
            content = []
        if len(content) == 0:
            print("ZEROLENGTH_TIME\t Crawl from instance %s returned zero-length array after time filtering."%self.instance_address)
            return

        if self.crawled_up_to_id is None:
            self.crawled_up_to_id = content[0]["id"]
        db = sqlite3.connect("data/toots.db")
        db.executemany("INSERT INTO raw_toots VALUES (?,?,?,?,?,?,?)", list(map(to_db_converter(self.instance_address), content)))
        db.commit()
        db.close()
        print("BACKWARD_CRAWL_FINISH\t Finished backward crawl on %s, %d new toots acquired." % (self.instance_address, len(content)))

    def __cmp__(self, other):
        if not self.crawled_all_preceding:
            return -1
        elif not other.crawled_all_preceding:
            return 1

        if self.crawled_up_to_date > other.crawled_up_to_date:
            return 1
        elif self.crawled_up_to_date == other.crawled_up_to_date:
            return 0
        else:
            return -1

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0





class Crawler(object):
    def __init__(self, max_parallel_crawls, instance_list, start_time, crawl_interval=datetime.timedelta(hours=2)):
        self.manager = Manager()
        self.queue = self.manager.PriorityQueue()
        self.max_parallel_crawls = max_parallel_crawls
        self.instance_list = instance_list
        self.start_time = start_time
        self.crawl_interval = crawl_interval

        for instance in instance_list:
            self.queue.put(InstanceCrawler(instance, start_time, crawl_interval=crawl_interval))

    def run(self):
        for i in range(self.max_parallel_crawls - 1):
            mp.Process(target=self.crawl).start()
        self.crawl()

    def crawl(self):
        while True:
            instance_crawler = self.queue.get()
            instance_crawler.crawl()
            if instance_crawler.instance_active:
                self.queue.put(instance_crawler)


if __name__ == "__main__":
    with open("instances.json", "r") as f:
        instances = json.load(f)
    instance_list = map(lambda i: i["name"], instances)
    #instance_list = ["mastodon.social", "mastodon.utwente.nl"]
    crawler = Crawler(50, instance_list, datetime.datetime.now(tz=TIME_ZONE) - datetime.timedelta(hours=2))
    crawler.run()