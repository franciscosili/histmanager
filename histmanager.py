import ROOT

class HistManager:

    def __init__(self, path=None):
        self.data = dict()
        if path is not None:
            self.load(path)
        self.weight = None

    def set_weight(self, w):
        self.weight = w

    def add(self, name, xbins, xmin, xmax):
        self.data[name] = ROOT.TH1F(name, name, xbins, xmin, xmax)
        self.data[name].Sumw2()

    def add_2d(self, name, xbins, xmin, xmax, ybins, ymin, ymax):
        self.data[name] = ROOT.TH2F(name, name, xbins, xmin, xmax, ybins, ymin, ymax)
        self.data[name].Sumw2()

    def add_profile(self, name, xbins, xmin, xmax, ymin, ymax):
        self.data[name] = ROOT.TProfile(name, name, xbins, xmin, xmax, ymin, ymax)
        self.data[name].Sumw2()

    def fill(self, name, value, weight=None):
        if weight is not None:
            self.data[name].Fill(value, weight)
        elif self.weight is not None:
            self.data[name].Fill(value, self.weight)
        else:
            self.data[name].Fill(value)
    
    def set_content(self, name, ibin, value):
        self.data[name].SetBinContent(ibin, value)
    
    def add_content(self, name, ibin, weight=None):
        if weight is not None:
            self.data[name].AddBinContent(ibin, weight)
        elif self.weight is not None:
            self.data[name].AddBinContent(ibin, self.weight)
        else:
            self.data[name].AddBinContent(ibin)

    def fill_2d(self, name, value_x, value_y, weight=None):
        if weight is None:
            self.data[name].Fill(value_x, value_y)
        else:
            self.data[name].Fill(value_x, value_y, weight)

    def fill_profile(self, name, value_x, value_y, weight):
        self.data[name].Fill(value_x, value_y, weight)

    def save(self, path):
        f = ROOT.TFile(path, 'recreate')
        f.cd()
        for name, hist in sorted(self.data.items()):
            hist.Write(name)

    def load(self, path):
        f = ROOT.TFile.Open(path)
        for key in f.GetListOfKeys():
            name = key.GetName()
            self.data[name] = f.Get(name)
            try:
                self.data[name].SetDirectory(0)
            except:
                pass

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, item):
        self.data[key] = item

    def __iter__(self):
        return self.data.items()
    
    def keys(self):
        return self.data.keys()

    def items(self):
        return self.data.items()

    def values(self):
        return self.data.values()
