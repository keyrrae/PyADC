import random


class FlashADC:
    def __init__(self, Vref, SigmaVos, NumBit):
        self.NumBit = NumBit
        self.NumBinLevel = 2 ** NumBit
        self.Vref = Vref
        self.Vtag = []
        for i in xrange(self.NumBinLevel):
            Vos = random.gauss(0, SigmaVos)
            TagNom = i * Vref / self.NumBinLevel
            TagVal = TagNom + Vos
            self.Vtag.append(TagVal)
        self.Vtag.append(Vref)

    def convert(self, Vin):
        if Vin > self.Vref:
            return self.NumBinLevel - 1
        elif Vin < 0.0:
            return 0
        else:
            for i in xrange(self.NumBinLevel):
                if Vin >= self.Vtag[i] and Vin < self.Vtag[i + 1]:
                    return i


class CDAC:
    def __init__(self, Cunit):
        return


class RDAC:
    def __init__(self, Runit):
        return
