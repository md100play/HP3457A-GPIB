import serial  # pySerial
import time

class hp(object):
    def readline(self):
        result = bytearray()
        c = 0
        while c != b'\r':
            c = self.ser.read()
            result += c
        return result.decode()

    def __init__(self, com):
        self.unit = "dcv"
        self.gotPlc = False
        self.plc = 10
        self.digits = '7.5'
        self.ser = serial.Serial(com, 460800, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                                 bytesize=serial.EIGHTBITS, timeout=3)
        self.ser.write(b'++rst\r\n')
        time.sleep(2)
        self.ser.write(b'++addr 22\r\n')
        self.ser.write(b'++eoi 0\r\n')
        self.ser.write(b'++eos 0\r\n')
        self.ser.write(b'++read_tmo_ms 5000\r\n')
        self.ser.write(b'END ALWAYS\r\n')
        self.ser.write(b'ID?\r\n')
        if "HP3457" not in self.readline():
            print("check connections and settings")
        self.ser.write(b'DCV\r\n')
        self.ser.write(b'TRIG SYN\r\n')

    def get_offset(self, unit, value):
        digit = self.get_digits()
        plc = str(self.get_plc())
        if float(plc) >= 1:
            plc = "1"
        elif float(plc) == float(.1):
            plc = ".1"
        elif float(plc) == float(.005):
            plc = ".005"
        elif float(plc) == float(.0005):
            plc = ".0005"
        if float(digit) > 6.5:
            digit = '6.5'
        # DC Volts Spec
        dcv_res = {'30mv': {'6.5': 10e-9, '5.5': 100e-9, '4.5': 1e-6, '3.5': 10e-6},
                  '300mv': {'6.5': 100e-9, '5.5': 1e-6, '4.5': 10e-6, '3.5': 100e-6},
                  '3v': {'6.5': 1e-6, '5.5': 10e-6, '4.5': 100e-6, '3.5': 1e-3},
                  '30v': {'6.5': 10e-6, '5.5': 100e-6, '4.5': 1e-3, '3.5': 10e-3},
                  '300v': {'6.5': 100e-6, '5.5': 1e-3, '4.5': 10e-3, '3.5': 100e-3}
                  }
        dcv_acc = {'30mv': {'100': {'acc': .0045, 'counts': 365}, '10': {'acc': .0045, 'counts': 385},
                           '1': {'acc': .0045, 'counts': 500}, '.1': {'acc': .0045, 'counts': 70},
                           '.005': {'acc': .0045, 'counts': 19}, '.0005': {'acc': .0045, 'counts': 6}},
                  '300mv': {'100': {'acc': .0035, 'counts': 39}, '10': {'acc': .0035, 'counts': 40},
                            '1': {'acc': .0035, 'counts': 50}, '.1': {'acc': .0035, 'counts': 9},
                            '.005': {'acc': .0035, 'counts': 4}, '.0005': {'acc': .0035, 'counts': 4}},
                  '3v': {'100': {'acc': .0025, 'counts': 6}, '10': {'acc': .0025, 'counts': 7},
                         '1': {'acc': .0025, 'counts': 7}, '.1': {'acc': .0025, 'counts': 4},
                         '.005': {'acc': .0025, 'counts': 4}, '.0005': {'acc': .0025, 'counts': 4}},
                  '30v': {'100': {'acc': .0040, 'counts': 19}, '10': {'acc': .0040, 'counts': 20},
                          '1': {'acc': .0040, 'counts': 30}, '.1': {'acc': .0040, 'counts': 7},
                          '.005': {'acc': .0040, 'counts': 4}, '.0005': {'acc': .0040, 'counts': 4}},
                  '300v': {'100': {'acc': .0055, 'counts': 6}, '10': {'acc': .0055, 'counts': 7},
                           '1': {'acc': .0055, 'counts': 7}, '.1': {'acc': .0055, 'counts': 4},
                           '.005': {'acc': .0055, 'counts': 4}, '.0005': {'acc': .0055, 'counts': 4}}
                  }

        # DC Current Spec
        dci_res = {'300ua': {'6.5': 100e-12, '5.5': 1e-9, '4.5': 10e-9, '3.5': 100e-9},
                  '3ma': {'6.5': 1e-9, '5.5': 10e-9, '4.5': 100e-9, '3.5': 1e-6},
                  '30ma': {'6.5': 10e-9, '5.5': 100e-9, '4.5': 1e-6, '3.5': 10e-6},
                  '300ma': {'6.5': 100e-9, '5.5': 1e-6, '4.5': 10e-6, '3.5': 100e-6},
                  '1a': {'6.5': 1e-6, '5.5': 10e-6, '4.5': 100e-6, '3.5': 1e-3}
                  }
        dci_acc = {'300ua': {'100': {'acc': .04, 'counts': 104}, '10': {'acc': .04, 'counts': 104},
                            '1': {'acc': .04, 'counts': 115}, '.1': {'acc': .04, 'counts': 14},
                            '.005': {'acc': .04, 'counts': 5}, '.0005': {'acc': .04, 'counts': 4}},
                  '3ma': {'100': {'acc': .04, 'counts': 104}, '10': {'acc': .04, 'counts': 104},
                          '1': {'acc': .04, 'counts': 115}, '.1': {'acc': .04, 'counts': 14},
                          '.005': {'acc': .04, 'counts': 5}, '.0005': {'acc': .04, 'counts': 4}},
                  '30ma': {'100': {'acc': .04, 'counts': 104}, '10': {'acc': .04, 'counts': 104},
                           '1': {'acc': .04, 'counts': 115}, '.1': {'acc': .04, 'counts': 14},
                           '.005': {'acc': .04, 'counts': 5}, '.0005': {'acc': .04, 'counts': 4}},
                  '300ma': {'100': {'acc': .08, 'counts': 204}, '10': {'acc': .08, 'counts': 204},
                            '1': {'acc': .08, 'counts': 215}, '.1': {'acc': .08, 'counts': 24},
                            '.005': {'acc': .08, 'counts': 6}, '.0005': {'acc': .08, 'counts': 4}},
                  '1a': {'100': {'acc': .08, 'counts': 604}, '10': {'acc': .08, 'counts': 604},
                         '1': {'acc': .08, 'counts': 615}, '.1': {'acc': .08, 'counts': 64},
                         '.005': {'acc': .08, 'counts': 10}, '.0005': {'acc': .08, 'counts': 5}}
                  }

        # 2-wire and 4-wire ohms
        ohms_res = {'30': {'6.5': 10e-6, '5.5': 100e-6, '4.5': 1e-3, '3.5': 10e-3},
                   '300': {'6.5': 100e-6, '5.5': 1e-3, '4.5': 10e-3, '3.5': 100e-3},
                   '3k': {'6.5': 1e-3, '5.5': 10e-3, '4.5': 100e-3, '3.5': 1},
                   '30k': {'6.5': 10e-3, '5.5': 100e-3, '4.5': 1, '3.5': 10},
                   '300k': {'6.5': 100e-3, '5.5': 1, '4.5': 10, '3.5': 100},
                   '3m': {'6.5': 1, '5.5': 10, '4.5': 100, '3.5': 1e3},
                   '30m': {'6.5': 10, '5.5': 100, '4.5': 1e3, '3.5': 10e3},
                   '300m': {'6.5': 100, '5.5': 1e3, '4.5': 10e3, '3.5': 100e3},
                   '3g': {'6.5': 1e3, '5.5': 10e3, '4.5': 100e3, '3.5': 1e6}
                   }
        ohms4_acc = {'30': {'100': {'acc': .0075, 'counts': 315}, '10': {'acc': .0075, 'counts': 335},
                           '1': {'acc': .0075, 'counts': 450}, '.1': {'acc': .0075, 'counts': 65},
                           '.0075': {'acc': .0075, 'counts': 18}, '.0005': {'acc': .0075, 'counts': 6}},
                    '300': {'100': {'acc': .0055, 'counts': 34}, '10': {'acc': .0055, 'counts': 35},
                            '1': {'acc': .0055, 'counts': 45}, '.1': {'acc': .0055, 'counts': 8},
                            '.0055': {'acc': .0055, 'counts': 4}, '.0005': {'acc': .0055, 'counts': 4}},
                    '3k': {'100': {'acc': .005, 'counts': 6}, '10': {'acc': .005, 'counts': 7},
                           '1': {'acc': .005, 'counts': 7}, '.1': {'acc': .005, 'counts': 4},
                           '.005': {'acc': .005, 'counts': 4}, '.0005': {'acc': .005, 'counts': 4}},
                    '30k': {'100': {'acc': .005, 'counts': 6}, '10': {'acc': .005, 'counts': 7},
                            '1': {'acc': .005, 'counts': 7}, '.1': {'acc': .005, 'counts': 4},
                            '.005': {'acc': .005, 'counts': 4}, '.0005': {'acc': .005, 'counts': 4}},
                    '300k': {'100': {'acc': .005, 'counts': 7}, '10': {'acc': .005, 'counts': 8},
                             '1': {'acc': .005, 'counts': 9}, '.1': {'acc': .005, 'counts': 4},
                             '.005': {'acc': .005, 'counts': 4}, '.0005': {'acc': .005, 'counts': 4}},
                    '3m': {'100': {'acc': .0065, 'counts': 12}, '10': {'acc': .0065, 'counts': 14},
                           '1': {'acc': .0065, 'counts': 16}, '.1': {'acc': .0065, 'counts': 7},
                           '.0065': {'acc': .0065, 'counts': 5}, '.0005': {'acc': .0065, 'counts': 5}},
                    '30m': {'100': {'acc': .04, 'counts': 80}, '10': {'acc': .04, 'counts': 83},
                            '1': {'acc': .04, 'counts': 93}, '.1': {'acc': .04, 'counts': 14},
                            '.04': {'acc': .04, 'counts': 6}, '.0005': {'acc': .04, 'counts': 5}}
                    }
        ohms2_acc = {'30': {'100': {'acc': .0075, 'counts': 20315}, '10': {'acc': .0075, 'counts': 20335},
                           '1': {'acc': .0075, 'counts': 20450}, '.1': {'acc': .0075, 'counts': 20065},
                           '.0075': {'acc': .0075, 'counts': 20018}, '.0005': {'acc': .0075, 'counts': 20006}},
                    '300': {'100': {'acc': .0055, 'counts': 2034}, '10': {'acc': .0055, 'counts': 2035},
                            '1': {'acc': .0055, 'counts': 2045}, '.1': {'acc': .0055, 'counts': 2008},
                            '.0055': {'acc': .0055, 'counts': 2004}, '.0005': {'acc': .0055, 'counts': 2004}},
                    '3k': {'100': {'acc': .005, 'counts': 206}, '10': {'acc': .005, 'counts': 207},
                           '1': {'acc': .005, 'counts': 207}, '.1': {'acc': .005, 'counts': 204},
                           '.005': {'acc': .005, 'counts': 204}, '.0005': {'acc': .005, 'counts': 204}},
                    '30k': {'100': {'acc': .005, 'counts': 26}, '10': {'acc': .005, 'counts': 27},
                            '1': {'acc': .005, 'counts': 27}, '.1': {'acc': .005, 'counts': 24},
                            '.005': {'acc': .005, 'counts': 24}, '.0005': {'acc': .005, 'counts': 24}},
                    '300k': {'100': {'acc': .005, 'counts': 9}, '10': {'acc': .005, 'counts': 10},
                             '1': {'acc': .005, 'counts': 11}, '.1': {'acc': .005, 'counts': 6},
                             '.005': {'acc': .005, 'counts': 6}, '.0005': {'acc': .005, 'counts': 6}},
                    '3m': {'100': {'acc': .0065, 'counts': 12}, '10': {'acc': .0065, 'counts': 14},
                           '1': {'acc': .0065, 'counts': 16}, '.1': {'acc': .0065, 'counts': 7},
                           '.0065': {'acc': .0065, 'counts': 5}, '.0005': {'acc': .0065, 'counts': 5}},
                    '30m': {'100': {'acc': .04, 'counts': 80}, '10': {'acc': .04, 'counts': 83},
                            '1': {'acc': .04, 'counts': 93}, '.1': {'acc': .04, 'counts': 14},
                            '.04': {'acc': .04, 'counts': 6}, '.0005': {'acc': .04, 'counts': 5}},
                    '300m': {'100': {'acc': 1.6, 'counts': 1000}, '10': {'acc': 1.6, 'counts': 1000},
                             '1': {'acc': 1.6, 'counts': 1000}, '.1': {'acc': 1.6, 'counts': 100},
                             '1.6': {'acc': 1.6, 'counts': 10}, '.0005': {'acc': 1.6, 'counts': 1}},
                    '3g': {'100': {'acc': 16, 'counts': 1000}, '10': {'acc': 16, 'counts': 1000},
                           '1': {'acc': 16, 'counts': 1000}, '.1': {'acc': 16, 'counts': 100},
                           '16': {'acc': 16, 'counts': 10}, '.0005': {'acc': 16, 'counts': 1}}
                    }

        # AC Voltage Spec 		90 day spec
        acv_res = {'30mv': {'6.5': 10e-9, '5.5': 100e-9, '4.5': 1e-6, '3.5': 10e-6},
                  '300mv': {'6.5': 100e-9, '5.5': 1e-6, '4.5': 10e-6, '3.5': 100e-6},
                  '3v': {'6.5': 1e-6, '5.5': 10e-6, '4.5': 100e-6, '3.5': 1e-3},
                  '30v': {'6.5': 10e-6, '5.5': 100e-6, '4.5': 1e-3, '3.5': 10e-3},
                  '300v': {'6.5': 100e-6, '5.5': 1e-3, '4.5': 10e-3, '3.5': 100e-3}
                  }
        acv_lo_acc = {
            '20': {'1': {'acc': .62, 'counts': 1120}, '.1': {'acc': .62, 'counts': 116},
                   '.005': {'acc': .62, 'counts': 16},
                   '.0005': {'acc': .62, 'counts': 6}},
            '45': {'1': {'acc': .21, 'counts': 1120}, '.1': {'acc': .21, 'counts': 116},
                   '.005': {'acc': .21, 'counts': 16},
                   '.0005': {'acc': .21, 'counts': 6}},
            '100': {'1': {'acc': .13, 'counts': 1120}, '.1': {'acc': .13, 'counts': 116},
                    '.005': {'acc': .13, 'counts': 16}, '.0005': {'acc': .13, 'counts': 6}},
            '400': {'1': {'acc': .14, 'counts': 1120}, '.1': {'acc': .14, 'counts': 550},
                    '.005': {'acc': .14, 'counts': 59}, '.0005': {'acc': .14, 'counts': 10}},
            '20000': {'1': {'acc': .66, 'counts': 2100}, '.1': {'acc': .66, 'counts': 224},
                      '.005': {'acc': .66, 'counts': 27}, '.0005': {'acc': .66, 'counts': 7}},
            '100000': {'1': {'acc': 3.16, 'counts': 9700}, '.1': {'acc': 3.16, 'counts': 974},
                       '.005': {'acc': 3.16, 'counts': 102}, '.0005': {'acc': 3.16, 'counts': 14}},
            '300000': {'1': {'acc': 10.16, 'counts': 66400}, '.1': {'acc': 10.16, 'counts': 6640},
                       '.005': {'acc': 10.16, 'counts': 668}, '.0005': {'acc': 10.16, 'counts': 71}}
        }
        acv_hi_acc = {
            '20': {'1': {'acc': .62, 'counts': 1120}, '.1': {'acc': .62, 'counts': 116},
                   '.005': {'acc': .62, 'counts': 16},
                   '.0005': {'acc': .62, 'counts': 6}},
            '45': {'1': {'acc': .27, 'counts': 1120}, '.1': {'acc': .27, 'counts': 116},
                   '.005': {'acc': .27, 'counts': 16},
                   '.0005': {'acc': .27, 'counts': 6}},
            '100': {'1': {'acc': .19, 'counts': 1120}, '.1': {'acc': .19, 'counts': 116},
                    '.005': {'acc': .19, 'counts': 16}, '.0005': {'acc': .19, 'counts': 6}},
            '400': {'1': {'acc': .2, 'counts': 1120}, '.1': {'acc': .2, 'counts': 550},
                    '.005': {'acc': .2, 'counts': 59},
                    '.0005': {'acc': .2, 'counts': 10}},
            '20000': {'1': {'acc': 1.06, 'counts': 3700}, '.1': {'acc': 1.06, 'counts': 374},
                      '.005': {'acc': 1.06, 'counts': 42}, '.0005': {'acc': 1.06, 'counts': 8}}
        }

        # AC DC coupled Voltage Spec		90 day spec
        acdcv_lo_acc = {'20': {'1': {'acc': 1.36, 'counts': 3600}, '.1': {'acc': 1.36, 'counts': 364},
                             '.005': {'acc': 1.36, 'counts': 41}, '.0005': {'acc': 1.36, 'counts': 8}},
                      '45': {'1': {'acc': .17, 'counts': 3600}, '.1': {'acc': .17, 'counts': 364},
                             '.005': {'acc': .17, 'counts': 41}, '.0005': {'acc': .17, 'counts': 8}},
                      '100': {'1': {'acc': .17, 'counts': 3600}, '.1': {'acc': .17, 'counts': 364},
                              '.005': {'acc': .17, 'counts': 41}, '.0005': {'acc': .17, 'counts': 8}},
                      '400': {'1': {'acc': .44, 'counts': 3600}, '.1': {'acc': .44, 'counts': 2810},
                              '.005': {'acc': .44, 'counts': 285}, '.0005': {'acc': .44, 'counts': 33}},
                      '20000': {'1': {'acc': .66, 'counts': 4620}, '.1': {'acc': .66, 'counts': 466},
                                '.005': {'acc': .66, 'counts': 51}, '.0005': {'acc': .66, 'counts': 9}},
                      '100000': {'1': {'acc': 3.16, 'counts': 11400}, '.1': {'acc': 3.16, 'counts': 1144},
                                 '.005': {'acc': 3.16, 'counts': 119}, '.0005': {'acc': 3.16, 'counts': 16}},
                      '300000': {'1': {'acc': 10.16, 'counts': 69600}, '.1': {'acc': 10.16, 'counts': 6960},
                                 '.005': {'acc': 10.16, 'counts': 701}, '.0005': {'acc': 10.16, 'counts': 74}}
                      }
        acdcv_hi_acc = {'20': {'1': {'acc': 1.36, 'counts': 3600}, '.1': {'acc': 1.36, 'counts': 364},
                             '.005': {'acc': 1.36, 'counts': 41}, '.0005': {'acc': 1.36, 'counts': 8}},
                      '45': {'1': {'acc': .23, 'counts': 3600}, '.1': {'acc': .23, 'counts': 364},
                             '.005': {'acc': .23, 'counts': 41}, '.0005': {'acc': .23, 'counts': 8}},
                      '100': {'1': {'acc': .23, 'counts': 3600}, '.1': {'acc': .23, 'counts': 364},
                              '.005': {'acc': .23, 'counts': 41}, '.0005': {'acc': .23, 'counts': 8}},
                      '400': {'1': {'acc': .5, 'counts': 3600}, '.1': {'acc': .5, 'counts': 2810},
                              '.005': {'acc': .5, 'counts': 285}, '.0005': {'acc': .5, 'counts': 33}},
                      '20000': {'1': {'acc': 1.16, 'counts': 6420}, '.1': {'acc': 1.16, 'counts': 650},
                                '.005': {'acc': 1.16, 'counts': 69}, '.0005': {'acc': 1.16, 'counts': 11}}
                      }

        # AC Current Spec	90 day spec
        aci_res = {'30ma': {'6.5': 10e-9, '5.5': 100e-9, '4.5': 1e-6, '3.5': 10e-6},
                  '300ma': {'6.5': 100e-9, '5.5': 1e-6, '4.5': 10e-6, '3.5': 100e-6},
                  '1a': {'6.5': 1e-6, '5.5': 10e-6, '4.5': 100e-6, '3.5': 1e-3}}
        aci_lo_acc = {
            '20': {'1': {'acc': .85, 'counts': 2800}, '.1': {'acc': .85, 'counts': 290},
                   '.005': {'acc': .85, 'counts': 32},
                   '.0005': {'acc': .85, 'counts': 7}},
            '45': {'1': {'acc': .3, 'counts': 2800}, '.1': {'acc': .3, 'counts': 290},
                   '.005': {'acc': .3, 'counts': 32},
                   '.0005': {'acc': .3, 'counts': 7}},
            '100': {'1': {'acc': .25, 'counts': 2800}, '.1': {'acc': .25, 'counts': 290},
                    '.005': {'acc': .25, 'counts': 32}, '.0005': {'acc': .25, 'counts': 7}},
            '400': {'1': {'acc': .25, 'counts': 2800}, '.1': {'acc': .25, 'counts': 750},
                    '.005': {'acc': .25, 'counts': 80}, '.0005': {'acc': .25, 'counts': 12}},
            '20000': {'1': {'acc': 1, 'counts': 4000}, '.1': {'acc': 1, 'counts': 400},
                      '.005': {'acc': 1, 'counts': 42},
                      '.0005': {'acc': 1, 'counts': 8}}}
        aci_hi_acc = {
            '20': {'1': {'acc': .95, 'counts': 2800}, '.1': {'acc': .95, 'counts': 290},
                   '.005': {'acc': .95, 'counts': 32},
                   '.0005': {'acc': .95, 'counts': 7}},
            '45': {'1': {'acc': .4, 'counts': 2800}, '.1': {'acc': .4, 'counts': 290},
                   '.005': {'acc': .4, 'counts': 32},
                   '.0005': {'acc': .4, 'counts': 7}},
            '100': {'1': {'acc': .35, 'counts': 2800}, '.1': {'acc': .35, 'counts': 290},
                    '.005': {'acc': .35, 'counts': 32}, '.0005': {'acc': .35, 'counts': 7}},
            '400': {'1': {'acc': .35, 'counts': 2800}, '.1': {'acc': .35, 'counts': 750},
                    '.005': {'acc': .35, 'counts': 80}, '.0005': {'acc': .35, 'counts': 12}}}

        # AC DC coupled Current Spec 	90 day spec
        acdci_lo_acc = {'20': {'1': {'acc': 1.55, 'counts': 16000}, '.1': {'acc': 1.55, 'counts': 1600},
                             '.005': {'acc': 1.55, 'counts': 165}, '.0005': {'acc': 1.55, 'counts': 20}},
                      '45': {'1': {'acc': .4, 'counts': 16000}, '.1': {'acc': .4, 'counts': 1600},
                             '.005': {'acc': .4, 'counts': 165}, '.0005': {'acc': .4, 'counts': 20}},
                      '100': {'1': {'acc': .3, 'counts': 16000}, '.1': {'acc': .3, 'counts': 1600},
                              '.005': {'acc': .3, 'counts': 165}, '.0005': {'acc': .3, 'counts': 20}},
                      '400': {'1': {'acc': .65, 'counts': 16000}, '.1': {'acc': .65, 'counts': 3750},
                              '.005': {'acc': .65, 'counts': 375}, '.0005': {'acc': .65, 'counts': 42}},
                      '20000': {'.95': {'acc': .95, 'counts': 17500}, '..95': {'acc': .95, 'counts': 1750},
                                '.005': {'acc': .95, 'counts': 180}, '.0005': {'acc': .95, 'counts': 22}}}
        acdci_hi_acc = {'20': {'1': {'acc': 1.65, 'counts': 16000}, '.1': {'acc': 1.65, 'counts': 1600},
                             '.005': {'acc': 1.65, 'counts': 165}, '.0005': {'acc': 1.65, 'counts': 20}},
                      '45': {'1': {'acc': .5, 'counts': 16000}, '.1': {'acc': .5, 'counts': 1600},
                             '.005': {'acc': .5, 'counts': 165}, '.0005': {'acc': .5, 'counts': 20}},
                      '100': {'1': {'acc': .4, 'counts': 16000}, '.1': {'acc': .4, 'counts': 1600},
                              '.005': {'acc': .4, 'counts': 165}, '.0005': {'acc': .4, 'counts': 20}},
                      '400': {'1': {'acc': .75, 'counts': 16000}, '.1': {'acc': .75, 'counts': 3750},
                              '.005': {'acc': .75, 'counts': 375}, '.0005': {'acc': .75, 'counts': 42}}}

        # Frequency Spec
        freq_acc = {'10': .05, '400': .01}

        if unit == "dcv":
            if value < 30.3e-3:
                dmm_range = '30mv'
            elif value < 303e-3:
                dmm_range = '300mv'
            elif value < 3.03:
                dmm_range = '3v'
            elif value < 30.3:
                dmm_range = '30v'
            elif value < 303:
                dmm_range = '300v'
            return (value * dcv_acc[dmm_range][plc]['acc']) + (dcv_res[dmm_range][digit] * dcv_acc[dmm_range][plc]['counts'])
        elif unit == "dci":
            if value < 303e-6:
                dmm_range = '300ua'
            elif value < 3.03e-3:
                dmm_range = '3ma'
            elif value < 30.3e-3:
                dmm_range = '30ma'
            elif value < 303e-3:
                dmm_range = '300ma'
            else:
                dmm_range = '1a'
            return (value * dci_acc[dmm_range][plc]['acc']) + dci_res[dmm_range][digit] * dci_acc[dmm_range][plc]['counts']
        elif unit == "ohms2":
            if value < 30.3:
                dmm_range = '30'
            elif value < 303:
                dmm_range = '300'
            elif value < 3.03e3:
                dmm_range = '3k'
            elif value < 30.3e3:
                dmm_range = '30k'
            elif value < 303e3:
                dmm_range = '300k'
            elif value < 3.03e6:
                dmm_range = '3m'
            elif value < 30.3e6:
                dmm_range = '30m'
            elif value < 303e6:
                dmm_range = '300m'
            elif value < 3.03e12:
                dmm_range = '3g'
            return (value * ohms2_acc[dmm_range][plc]['acc']) + ohms_res[dmm_range][digit] * ohms2_acc[dmm_range][plc]['counts']
        elif unit == "ohms4":
            if value < 30.3:
                dmm_range = '30'
            elif value < 303:
                dmm_range = '300'
            elif value < 3.03e3:
                dmm_range = '3k'
            elif value < 30.3e3:
                dmm_range = '30k'
            elif value < 303e3:
                dmm_range = '300k'
            elif value < 3.03e6:
                dmm_range = '3m'
            elif value < 30.3e6:
                dmm_range = '30m'
            elif value < 303e6:
                dmm_range = '300m'
            elif value < 3.03e12:
                dmm_range = '3g'
            return (value * ohms4_acc[dmm_range][plc]['acc']) + ohms_res[dmm_range][digit] * ohms4_acc[dmm_range][plc]['counts']
        elif unit == "acv":
            if float(plc) > 1:
                plc = '1'
            freq = 60  # needs to be fixed
            if freq < 45:
                freq = '20'
            elif freq < 100:
                freq = '45'
            elif freq < 400:
                freq = '100'
            elif freq < 20000:
                freq = '400'
            elif freq < 100000:
                freq = '20000'
            elif freq < 1000000:
                freq = '300000'
            if value < 32.5e-3:
                dmm_range = '30mv'
            elif value < 325e-3:
                dmm_range = '300mv'
            elif value < 3.25:
                dmm_range = '3v'
            elif value < 32.5:
                dmm_range = '30v'
            elif value < 303:
                dmm_range = '300v'
            if value > 32.5:
                acvAcc = acv_hi_acc
            else:
                acvAcc = acv_lo_acc
            return (value * acvAcc[freq][plc]['acc']) + acv_res[dmm_range][digit] * acvAcc[freq][plc]['counts']
        elif unit == "acdcv":
            if float(plc) > 1:
                plc = '1'
            freq = 60  # needs to be fixed
            if freq < 45:
                freq = '20'
            elif freq < 100:
                freq = '45'
            elif freq < 400:
                freq = '100'
            elif freq < 20000:
                freq = '400'
            elif freq < 100000:
                freq = '20000'
            elif freq < 1000000:
                freq = '300000'
            if value < 32.5e-3:
                dmm_range = '30mv'
            elif value < 325e-3:
                dmm_range = '300mv'
            elif value < 3.25:
                dmm_range = '3v'
            elif value < 32.5:
                dmm_range = '30v'
            elif value < 303:
                dmm_range = '300v'
            if value > 32.5:
                acdcv_acc = acdcv_hi_acc
            else:
                acdcv_acc = acdcv_lo_acc
            return (value * acdcv_acc[freq][plc]['acc']) + acv_res[dmm_range][digit] * acdcv_acc[freq][plc]['counts']
        elif unit == "aci":
            if float(plc) > 1:
                plc = '1'
            freq = 60  # needs to be fixed
            if freq < 45:
                freq = '20'
            elif freq < 100:
                freq = '45'
            elif freq < 400:
                freq = '100'
            elif freq < 20000:
                freq = '400'
            elif freq < 100000:
                freq = '20000'
            if value < 30.3e-3:
                dmm_range = '30ma'
            elif value < 303e-3:
                dmm_range = '300ma'
            if value > 303e-3:
                dmm_range = '1a'
                aci_acc = aci_hi_acc
            else:
                aci_acc = aci_lo_acc
            return (value * aci_acc[freq][plc]['acc']) + aci_res[dmm_range][digit] * aci_acc[freq][plc]['counts']
        elif unit == "acdci":
            if float(plc) > 1:
                plc = '1'
            freq = 60  # needs to be fixed
            if freq < 45:
                freq = '20'
            elif freq < 100:
                freq = '45'
            elif freq < 400:
                freq = '100'
            elif freq < 20000:
                freq = '400'
            elif freq < 100000:
                freq = '20000'
            if value < 30.3e-3:
                dmm_range = '30ma'
            elif value < 303e-3:
                dmm_range = '300ma'
            if value > 303e-3:
                dmm_range = '1a'
                acdci_acc = acdci_hi_acc
            else:
                acdci_acc = acdci_lo_acc
            return (value * acdci_acc[freq][plc]['acc']) + aci_res[dmm_range][digit] * acdci_acc[freq][plc]['counts']
        elif unit == "freq":
            if value < 400:
                dmm_range = '10'
            else:
                dmm_range = '400'
            return value * freq_acc[dmm_range]
        elif unit == "per":
            freq = self.get_frequency()
            if freq < 400:
                dmm_range = '10'
            else:
                dmm_range = '400'
            return value * freq_acc[dmm_range]

    def get_frequency(self):
        self.set_measure("freq")
        freq = self.measure()
        self.set_measure(self.unit)
        return freq

    def read(self):
        self.ser.write(b'++read\r\n')
        val = self.readline()
        return val.rstrip('\r\n')

    def measure(self):
        if float(self.get_digits()) > 6.5:
            value = self.read()
            self.ser.write(b'RMATH HIRES\r\n')
            time.sleep(.007)
            self.ser.write(b'++read\r\n')
            hire = self.readline().rstrip('\r\n')
            try:
                float(value)
                float(hire)
                if abs(float(hire)) == 0:
                    return float(value) + float(hire)
                elif abs(float(value)) / abs(float(hire)) > 1e6:
                    return float(value) + float(hire)
                else:
                    time.sleep(.1)
                    return float(value)
            except ValueError:
                return self.measure()
        else:
            value = self.read()
            try:
                float(value)
                return float(value)
            except ValueError:
                return self.measure()

    def get_plc(self):
        if self.gotPlc:
            return self.plc
        else:
            self.ser.write(b'NPLC?\r\n')
            self.plc = self.readline().rstrip('\r\n')[1:]
            try:
                self.plc = float(self.plc)
                self.gotPlc = True
                return self.plc
            except ValueError:
                time.sleep(.1)
                return self.get_plc()

    def get_digits(self):
        self.digits = self.get_plc()
        if float(self.digits) <= .0005:
            self.digits = '3.5'
        elif float(self.digits) <= .005:
            self.digits = '4.5'
        elif float(self.digits) <= .1:
            self.digits = '5.5'
        elif float(self.digits) <= 1:
            self.digits = '6.5'
        elif float(self.digits) <= 10:
            self.digits = '7.5'
        elif float(self.digits) <= 100:
            self.digits = '7.5'
        return self.digits

    def set_measure(self, units):
        self.unit = units
        if self.unit == "dcv":
            self.ser.write(b'F10\r\n')
        elif self.unit == "dci":
            self.ser.write(b'DCI\r\n')
        elif self.unit == "ohms2":
            self.ser.write(b'F40\r\n')
        elif self.unit == "ohms4":
            self.ser.write(b'F50\r\n')
        elif self.unit == "acv":
            self.ser.write(b'ACV\r\n')
        elif self.unit == "acdcv":
            self.ser.write(b'ACDCV\r\n')
        elif self.unit == "aci":
            self.ser.write(b'ACI\r\n')
        elif self.unit == "acdci":
            self.ser.write(b'ACDCI\r\n')
        elif self.unit == "freq":
            self.ser.write(b'FREQ\r\n')
        elif self.unit == "per":
            self.ser.write(b'PER\r\n')
        time.sleep(.2)

    def set_plc(self, plc):
        try:
            float(plc)
            if not (float(plc) == float(100) or float(plc) == float(10) or float(plc) == float(1) or float(
                    plc) == float(.1) or float(plc) == float(.005) or float(plc) == float(.0005)):
                print("PLC incorrect!")
                return
        except ValueError:
            print("PLC incorrect!")
            return
        if float(plc) == float(100):
            plc = 100
        elif float(plc) == float(10):
            plc = 10
        elif float(plc) == float(1):
            plc = 1
        elif float(plc) == float(.005):
            plc = .005
        elif float(plc) == float(.0005):
            plc = .0005
        self.plc = plc
        nplc = "NPLC " + str(plc) + "\r\n"
        self.ser.write(nplc.encode())
        time.sleep(1)

    def set_terminals(self, term):
        if term == "Rear":
            self.ser.write(b"TERM 2\r\n")
        else:
            self.ser.write(b"TERM 1\r\n")
        time.sleep(.5)
