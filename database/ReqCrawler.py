"""
a crawler that crawls requirements information on UCI website
"""

from bs4 import BeautifulSoup
import requests
import re
import json
import io

# Make it work for Python 2+3 and with Unicode
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

__author__ = "Jenny Zeng"
__email__ = "jennyzengzzh@gmail.com"


class ReqCrawler:
    def __init__(self):
        pass

    def CrawlUrl(self, save_at="requirements/temp_COMPUTER SCIENCE.json",
                 url="http://catalogue.uci.edu/donaldbrenschoolofinformationandcomputersciences/departmentofcomputerscience/#majorstext"):
        self.json = {"requirements": [], "specs": []}
        self.curReq = None
        self.curSubReqList = None
        self.save_at = save_at
        soup = self._GetTableEles(url)
        self._CrawlSoupByTr(soup)

    def _GetTableEles(self, url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "lxml")
        soup = soup.find("table", class_=["sc_courselist"]).find_all_next("tr")
        return soup

    def _CrawlSoupByTr(self, soup):
        for tag in soup:
            self._ProcessTr(tag)
        with io.open(self.save_at, 'w', encoding='utf8') as outfile:
            data = json.dumps(self.json, sort_keys=False, indent=2,
                              separators=(',', ': '), ensure_ascii=False)

            outfile.write(to_unicode(data))
        self.json.clear()

    def _ProcessTr(self, tag):
        if not tag.td: return
        if tag.td.div:
            self._ProcessTrCourseWithComment(tag)
        elif tag.td.span:
            self._ProcessTrComment(tag)
        elif tag.td.a:
            self._ProcessTrCourse(tag)


    def _ProcessTrComment(self, tag):
        attrs = tag.td.span.attrs
        indicator = attrs.get('class')
        if indicator:
            if "courselistcomment" in indicator:
                comment = self._GetString(tag.td.span)
                # should have a _comment field in json
                if "areaheader" in indicator:
                    # is requirement header
                    if self.curReq: self.json["requirements"].append(self.curReq)
                    self.curReq = {"name": comment, "sub_reqs": []}
                    self.curSubReqList = None

                else:
                    # is subreq begins
                    self.curReq['sub_reqs'].append({"_comments": comment, "req_num": -1, "req_list": []})
                    self.curSubReqList = self.curReq['sub_reqs'][-1]['req_list']
                    # we are not able to get the req_num from crawler, so we should look at the
                    # comments and do that manually


    def _ProcessTrCourseWithComment(self, tag):
        self._IfOneSubReqCondition()

        string = self._GetString(tag.td.div)
        self.curSubReqList.append(string)

    def _ProcessTrCourse(self, tag):
        self._IfOneSubReqCondition()
        string = self._GetString(tag.td)

        self.curSubReqList.append(string)

    def _GetString(self, tag):
        return " ".join(i for i in tag._all_strings()).strip()

    def _IfOneSubReqCondition(self):
        # only has one subreq
        if self.curSubReqList == None:
            self.curReq["sub_reqs"].append({ "req_num": -1, "req_list": []})
            self.curSubReqList = self.curReq["sub_reqs"][-1]["req_list"]

if __name__ == '__main__':

    crawler = ReqCrawler()
    crawler.CrawlUrl()