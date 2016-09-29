from collections import OrderedDict 
from pprint import pprint 
import pickle, json

class JSON_Writer(object):
    """Dump non null extractions to output file"""

    def __init__(self):
        super(JSON_Writer, self).__init__()
        self.keys = ['url','name','brand','price','reduced_price','likes','color','measurements','size','fabric','washlook','item']

    def write(self, dumpname, filename):
        f = open(dumpname, "r")
        dump = pickle.load(f)
        f.close()

        newlist = []
        # i = 0
        for entry in dump:
            data = OrderedDict()
            for key in self.keys:
                if key in entry:
                    if key=="url":
                        data["URL"]=entry[key]
                    else:
                        data[key] = entry[key]
            # print i, len(data.keys())
            # i+=1
            newlist.append(json.dumps(data))

        # print newlist[0:100]
        w = open(filename, "w+")
        w.write("[")
        # out = json.dumps(newlist)
        w.write(",\n".join(newlist))
        w.write("\n"+"]")
        # w.write(out+'\n')
        w.close()