import os
import re

from oelint_adv.parser import get_items


class Stash():

    def __init__(self):
        self.__list = []

    def AddFile(self, _file, lineOffset=0, forcedLink=None):
        print("Parsing {}".format(_file))
        res = get_items(self, _file)
        if forcedLink:
            for item in [x for x in res if x.Origin == _file]:
                item.AddLink(forcedLink)
        # Match bbappends to bbs
        if _file.endswith(".bbappend"):
            bn_this = os.path.basename(_file).replace(
                ".bbappend", "").replace("%", ".*")
            for item in self.__list:
                if re.match(bn_this, os.path.basename(item.Origin).replace(".bb", "")):
                    item.AddLink(_file)
                    for r in res:
                        r.AddLink(item.Origin)
        self.__list += res
        return res

    def GetRecipes(self):
        return list(set([x.Origin for x in self.__list if x.Origin.endswith(".bb")]))

    def __is_linked_to(self, item, filename):
        return filename in item.Links or filename == item.Origin

    def __get_items_by_file(self, items, filename):
        if not filename:
            return items
        return [x for x in items if self.__is_linked_to(x, filename)]

    def __get_items_by_classifier(self, items, classifier):
        if not classifier:
            return items
        return [x for x in items if x.CLASSIFIER == classifier]

    def __get_items_by_attribute(self, items, attname, attvalue):
        if not attname:
            return items
        # v is a list
        res = [x for x in items if attname in x.GetAttributes().keys()]
        if attvalue:
            res = [x for x in res if (attname in x.GetAttributes(
            ).keys() and x.GetAttributes()[attname] == attvalue)]
        return res

    def GetItemsFor(self, filename=None, classifier=None, attribute=None, attributeValue=None):
        res = self.__list
        res = self.__get_items_by_file(res, filename)
        res = self.__get_items_by_classifier(res, classifier)
        res = self.__get_items_by_attribute(res, attribute, attributeValue)
        return list(set(res))
