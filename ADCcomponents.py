import random


class ADC:
    def __init__(self, Vref, NumBit):
        self.NumBit = NumBit
        self.NumBinLevel = 2 ** NumBit
        self.Vref = Vref


class IdealADC(ADC):
    def __init__(self, Vref, NumBit):
        ADC.__init__(self, Vref, NumBit)
        self.Vtag = []
        for i in xrange(self.NumBinLevel):
            TagNom = i * Vref / self.NumBinLevel
            self.Vtag.append(TagNom)
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


class FlashADC:
    def __init__(self, Vref, SigmaVos, NumBit):
        ADC.__init__(self, Vref, NumBit)
        self.Vtag = []
        for i in xrange(self.NumBinLevel):
            Vos = random.gauss(0, SigmaVos)
            TagNom = i * Vref / self.NumBinLevel
            TagVal = TagNom + Vos
            self.Vtag.append(TagVal)
        self.Vtag.append(Vref)


class CDAC:
    def __init__(self, Cunit):
        return


class RDAC:
    def __init__(self, Runit):
        return


class SineGenerator:
    def __init__(self, Amp, Freq, Phase):
        self.Amp = Amp
        self.Freq = Freq
        self.Phase = Phase
    def Vgen(Time):
        #    def SineGen(self, NumPt, NumBit, FreqSin, PercntFS):
#        SineValues = []
#        for i in xrange()
#        return SineValues
