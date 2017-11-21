import pycraft_minetest as pcmt
import pycraft_minetest.blocklist as blocklist

class PycraftMaterialsLibrary():

    matlibrary = {}

    def __init__(self):
        self.matlibrary = self.buildDictWithBlockNamesValues()

    def getBlockName(self, id):
        l = self.matlibrary.values()
        if id in l:
            i = l.index(id)
            return self.matlibrary.keys()[i]
        else:
            return "what is the name of block number {}?".format(id)

    def getBlockId(self, name):
        if name in self.matlibrary:
            return self.matlibrary[name]
        else:
            return pcmt.gold # default block if name is unknown

    def testNameInPcmt(self, name, id):
        for r in dir(pcmt):
            try:
                pcmtid = getattr(pcmt, r)
                if (pcmtid == id) and ((r == name) or (r+'_BLOCK'.lower() == name)): # _block removed from name
                    return r
            except:
                pass
        return None

    def buildDictWithBlockNamesValues(self):
        blockNames = dir(blocklist)  # get all variables in blocklist.py
        blockDict = {}
        bn = None
        for bn in blockNames:
            try:
                val = getattr(blocklist, bn)  # try to get the value of the symbol
                if isinstance(val, blocklist.Block):
                    bnpcmt = bn.lower()
                    bnpcmt_renamed = self.testNameInPcmt(bnpcmt, val.id)
                    if bnpcmt_renamed is not None:
                        blockDict[bnpcmt_renamed] = val.id
                        #print(bnpcmt,val.id)
                #bv = pcmt.getblock(bn.lower())
                #w[bn] = bv
            except:
                pass
        return blockDict

if __name__ == "__main__":
    w = PycraftMaterialsLibrary()
    print (w.matlibrary)
    print(w.getBlockName(w.matlibrary['fire']))
    print(w.getBlockName(89))
