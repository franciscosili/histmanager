import ROOT
from array import array
import os

class HistManager:
    #===============================================================================================
    def __init__(self, path=None, hists_dict=None):
        self.path = path
        self.data = dict()
        if path is not None:
            self.load(path)
        if hists_dict is not None:
            self.dict_to_hm(hists_dict)
        self.weight = None
    #===============================================================================================

    #===============================================================================================
    def set_weight(self, w):
        self.weight = w
    #===============================================================================================

    #===============================================================================================
    def add(self, name, nxbins, xmin=None, xmax=None, bins=None):
        if not bins: self.data[name] = ROOT.TH1F(name, name, nxbins, xmin, xmax)
        else:        self.data[name] = ROOT.TH1F(name, name, nxbins, array('d', bins))
        self.data[name].Sumw2()
    #===============================================================================================

    #===============================================================================================
    def add_2d(self, name, nxbins, xmin=None, xmax=None, nybins=None, ymin=None, ymax=None, binsx=None, binsy=None):
        if not binsx and not binsy:
            self.data[name] = ROOT.TH2F(name, name, nxbins, xmin, xmax, nybins, ymin, ymax)
        elif not binsx and binsy:
            self.data[name] = ROOT.TH2F(name, name, nxbins, xmin, xmax, nybins, array('d', binsy))
        elif binsx and not binsy:
            self.data[name] = ROOT.TH2F(name, name, nxbins, array('d', binsx), nybins, ymin, ymax)
        elif binsx and binsy:
            self.data[name] = ROOT.TH2F(name, name, nxbins, array('d', binsx), nybins, array('d', binsy))
        self.data[name].Sumw2()
    #===============================================================================================
    
    # #===============================================================================================
    # def add_graph(self, ):
    #     pass
    # #===============================================================================================

    #===============================================================================================
    def add_profile(self, name, xbins, xmin, xmax, ymin, ymax):
        self.data[name] = ROOT.TProfile(name, name, xbins, xmin, xmax, ymin, ymax)
        self.data[name].Sumw2()
    #===============================================================================================

    #===============================================================================================
    def fill(self, name, value, weight=None):
        if weight is not None:
            self.data[name].Fill(value, weight)
        elif self.weight is not None:
            self.data[name].Fill(value, self.weight)
        else:
            self.data[name].Fill(value)
    #===============================================================================================
    
    #===============================================================================================
    def fill_2d(self, name, valuex, valuey, weight=None):
        if weight is not None:
            self.data[name].Fill(valuex, valuey, weight)
        elif self.weight is not None:
            self.data[name].Fill(valuex, valuey, self.weight)
        else:
            self.data[name].Fill(valuex, valuey)
    #===============================================================================================
    
    #===============================================================================================
    def set_content(self, name, ibin, value):
        self.data[name].SetBinContent(ibin, value)
    #===============================================================================================
    
    #===============================================================================================
    def set_error(self, name, ibin, error):
        self.data[name].SetBinError(ibin, error)
    #===============================================================================================
    
    #===============================================================================================
    def set_content_2d(self, name, ibin, jbin, value):
        self.data[name].SetBinContent(ibin, jbin, value)
    #===============================================================================================
    
    #===============================================================================================
    def set_error_2d(self, name, ibin, jbin, error):
        self.data[name].SetBinError(ibin, jbin, error)
    #===============================================================================================
    
    #===============================================================================================
    def add_content(self, name, ibin, weight=None):
        if weight is not None:
            self.data[name].AddBinContent(ibin, weight)
        elif self.weight is not None:
            self.data[name].AddBinContent(ibin, self.weight)
        else:
            self.data[name].AddBinContent(ibin)
    #===============================================================================================

    #===============================================================================================
    def fill_profile(self, name, value_x, value_y, weight=None):
        if weight is not None:
            self.data[name].Fill(value_x, value_y, weight)
        elif self.weight is not None:
            self.data[name].Fill(value_x, value_y, self.weight)
        else:
            self.data[name].Fill(value_x, value_y)
    #===============================================================================================

    #===============================================================================================
    def save(self, path):
        self.path = path
        if not os.path.exists(self.path): os.makedirs(self.path)
        f = ROOT.TFile(path, 'recreate')
        f.cd()
        for name, hist in sorted(self.data.items()):
            hist.Write(name)
    #===============================================================================================

    #===============================================================================================
    def loop_keys(self, f, keys, folder=None):
        for key in keys:
            name = key.GetName()
            obj  = f.Get(name)
            if obj.ClassName() != 'TDirectoryFile':
                self.data[name] = f.Get(name)
                try:
                    self.data[name].SetDirectory(0)
                except:
                    pass
            else:
                if folder:
                    if folder == obj.GetName():
                        self.loop_keys(obj, obj.GetListOfKeys())
    #===============================================================================================
    
    #===============================================================================================
    def load(self, path, folder=None):
        f = ROOT.TFile.Open(path)
        self.loop_keys(f, f.GetListOfKeys(), folder)
        return
    #===============================================================================================

    #===============================================================================================
    def dict_to_hm(self, hists_dict):
        for k, h in hists_dict.items():
            self.data[k] = h
        return
    #===============================================================================================

    #===============================================================================================
    def __getitem__(self, key):
        return self.data[key]
    #===============================================================================================

    #===============================================================================================
    def __setitem__(self, key, item):
        self.data[key] = item
    #===============================================================================================

    #===============================================================================================
    def __iter__(self):
        return self.data.items()
    #===============================================================================================
    
    #===============================================================================================
    def keys(self):
        return self.data.keys()
    #===============================================================================================

    #===============================================================================================
    def items(self):
        return self.data.items()
    #===============================================================================================

    #===============================================================================================
    def values(self):
        return self.data.values()
    #===============================================================================================
