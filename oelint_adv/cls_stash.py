import os
import re

from oelint_adv.parser import get_items


class Stash():

    def __init__(self):
        self.__list = []

    def AddFile(self, _file, lineOffset=0, forcedLink=None):
        print("Parsing {}".format(_file))
        res = get_items(self, _file, lineOffset=lineOffset)
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

    def GetLoneAppends(self):
        __linked_appends = []
        __appends = []
        for x in self.__list:
            if x.Origin.endswith(".bbappend"):
                __appends.append(x)
            else:
                __linked_appends += x.Links
        return list(set([x.Origin for x in __appends if x not in __linked_appends]))

    def __is_linked_to(self, item, filename, nolink=False):
        return (filename in item.Links and not nolink) or filename == item.Origin

    def __get_items_by_file(self, items, filename, nolink=False):
        if not filename:
            return items
        return [x for x in items if self.__is_linked_to(x, filename, nolink=nolink)]

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

    def GetLinksForFile(self, filename):
        if not filename:
            return []
        return [x.Origin for x in self.__get_items_by_file(self.__list, filename) if x.Origin != filename]

    def GetItemsFor(self, filename=None, classifier=None, attribute=None, attributeValue=None, nolink=False):
        res = self.__list
        res = self.__get_items_by_file(res, filename, nolink=nolink)
        res = self.__get_items_by_classifier(res, classifier)
        res = self.__get_items_by_attribute(res, attribute, attributeValue)
        return list(set(res))
