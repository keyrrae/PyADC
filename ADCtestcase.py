import ADCcomponents

ADC1 = ADCcomponents.FlashADC(Vref = 3.0, 0.0, 3)

print ADC1.NumBit
print ADC1.NumBinLevel
print ADC1.Vref
print ADC1.Vtag
print ADC1.convert(2.8)
