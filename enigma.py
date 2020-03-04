import plugboard
import rotor
import reflector

ROTOR = {
    'I'     : rotor.RotorI,
    'II'    : rotor.RotorII,
    'III'   : rotor.RotorIII,
    'IV'    : rotor.RotorIV,
    'V'     : rotor.RotorV,
    'VI'    : rotor.RotorVI,
    'VII'   : rotor.RotorVII,
    'VIII'  : rotor.RotorVIII,
    'Beta'  : rotor.RotorBeta,
    'Gamma' : rotor.RotorGamma,
    }

REFLECTOR = {
    'B'     : reflector.ReflectorB,
    'C'     : reflector.ReflectorC,
    'BThin' : reflector.ReflectorBThin,
    'CThin' : reflector.ReflectorCThin,
    }

class Enigma(object):
    def __init__(self, r1, r2, r3, rf, pos=None, ring=None, cables=None):
        if pos is None:
            pos = [None] * 3
        if ring is None:
            ring = [None] * 3
        self.pb = plugboard.Plugboard(cables)
        self.r1 = ROTOR[r1](pos[0], ring[0])
        self.r2 = ROTOR[r2](pos[1], ring[1], doublestep=True)
        self.r3 = ROTOR[r3](pos[2], ring[2])
        self.rf = REFLECTOR[rf]()

    def getPosition(self):
        return ''.join(r.getPosition() for r in (self.r1, self.r2, self.r3))

    def setPosition(self, pos):
        self.r1.setPosition(pos[0])
        self.r2.setPosition(pos[1])
        self.r3.setPosition(pos[2])

    def setRing(self, ring):
        self.r1.setRing(ring[0])
        self.r2.setRing(ring[1])
        self.r3.setRing(ring[2])

    def translate(self, data_in):
        data_out = []
        for c in data_in:
            turnover = self.r3.step()
            turnover = self.r2.step(turnover)
            self.r1.step(turnover)

            p0 = self.pb.translate(c)
            p1 = self.r3.rtrans(p0)
            p2 = self.r2.rtrans(p1)
            p3 = self.r1.rtrans(p2)
            p4 = self.rf.translate(p3)
            p5 = self.r1.ltrans(p4)
            p6 = self.r2.ltrans(p5)
            p7 = self.r3.ltrans(p6)
            p8 = self.pb.translate(p7)

            data_out.append(p8)

        return ''.join(data_out)

    def match(self, plain, cipher):
        for i, p in enumerate(plain):
            c = self.translate(p)
            if c != cipher[i]:
                return False
        return True

class Enigma4(object):
    def __init__(self, r1, r2, r3, r4, rf, pos=None, ring=None, cables=None):
        if pos is None:
            pos = [None] * 4
        if ring is None:
            ring = [None] * 4
        self.pb = plugboard.Plugboard(cables)
        self.r1 = ROTOR[r1](pos[0], ring[0])
        self.r2 = ROTOR[r2](pos[1], ring[1])
        self.r3 = ROTOR[r3](pos[2], ring[2], doublestep=True)
        self.r4 = ROTOR[r4](pos[3], ring[3])
        self.rf = REFLECTOR[rf]()

    def getPosition(self):
        return ''.join(r.getPosition() for r in (self.r1, self.r2, self.r3, self.r4))

    def setPosition(self, pos):
        self.r1.setPosition(pos[0])
        self.r2.setPosition(pos[1])
        self.r3.setPosition(pos[2])
        self.r4.setPosition(pos[3])

    def setRing(self, ring):
        self.r1.setRing(ring[0])
        self.r2.setRing(ring[1])
        self.r3.setRing(ring[2])
        self.r4.setRing(ring[3])

    def translate(self, data_in):
        data_out = []
        for c in data_in:
            turnover = self.r4.step()
            turnover = self.r3.step(turnover)
            self.r2.step(turnover)

            p0 = self.pb.translate(c)
            p1 = self.r4.rtrans(p0)
            p2 = self.r3.rtrans(p1)
            p3 = self.r2.rtrans(p2)
            p4 = self.r1.rtrans(p3)
            p5 = self.rf.translate(p4)
            p6 = self.r1.ltrans(p5)
            p7 = self.r2.ltrans(p6)
            p8 = self.r3.ltrans(p7)
            p9 = self.r4.ltrans(p8)
            pA = self.pb.translate(p9)

            data_out.append(pA)

        return ''.join(data_out)

if __name__ == '__main__':
    import unittest

    class TestEnigma(unittest.TestCase):

        def test_Position(self):
            e = Enigma('III', 'IV', 'V', 'B', 'AJD')
            self.assertEqual(e.translate('A'), 'P')
            self.assertEqual(e.getPosition(), 'BKE')
            self.assertEqual(e.translate('A'), 'J')
            self.assertEqual(e.getPosition(), 'BKF')
            e.setPosition('QIY')
            self.assertEqual(e.translate('A'), 'D')
            self.assertEqual(e.getPosition(), 'QIZ')
            self.assertEqual(e.translate('A'), 'E')
            self.assertEqual(e.getPosition(), 'QJA')
            self.assertEqual(e.translate('A'), 'L')
            self.assertEqual(e.getPosition(), 'RKB')
            self.assertEqual(e.translate('A'), 'F')
            self.assertEqual(e.getPosition(), 'RKC')
            self.assertEqual(e.translate('A'), 'D')
            self.assertEqual(e.getPosition(), 'RKD')

        def test_Ring(self):
            e = Enigma('VIII', 'VII', 'VI', 'C', ring='VGI')
            self.assertEqual(e.translate('A' * 1000),
                'HLKGS' 'NQVEQ' 'PFFOR' 'OWZLB' 'XPZPN' 'CLYYE' 'KWCEQ' 'DKEXI' 'JIUQE' 'YZGID'
                'DJOUE' 'HVVOV' 'EYQZD' 'WUFXN' 'HDCHZ' 'FLINT' 'EMFZI' 'HUSBP' 'EDBCQ' 'MZJUC'
                'BEWDC' 'JDLOK' 'NGHEU' 'SVFFG' 'LIBOF' 'GHBHG' 'EXNCO' 'BWOPB' 'GHKIY' 'LWOED'
                'WPGOD' 'OXLXF' 'PEZLI' 'TBMWU' 'EPWLB' 'EDPHY' 'HLLDC' 'EEWPI' 'GHTEE' 'YXCEY'
                'ZJBCJ' 'IWZOO' 'UHQJU' 'FNFSW' 'ICMBK' 'YXNJS' 'WKUOU' 'UDIVU' 'TRRVY' 'IWZEX'
                'QRTBM' 'FYEOW' 'IRHZN' 'RXUNL' 'CJRJQ' 'EBWNX' 'ERNTX' 'LKDEZ' 'UKEEQ' 'ERSZB'
                'EPGGM' 'IDNMP' 'FKDJC' 'MNCVE' 'QLCLZ' 'SKTFL' 'KEHEP' 'JYKOQ' 'RHWSB' 'KZXVG'
                'YQOML' 'BYIYN' 'OSIML' 'RJYFW' 'LHNXC' 'JCVVR' 'HLTES' 'VDNOR' 'HYKEW' 'SKBXX'
                'MHNCR' 'ZGVYX' 'TWGUI' 'OWGTI' 'FHLHW' 'RYZJL' 'EDNLJ' 'EKQYC' 'ZENBV' 'LILMG'
                'DEFSB' 'KKBZG' 'MZTDQ' 'FFJYV' 'XDPQY' 'WMEOS' 'ZDEVU' 'XBUTK' 'HMHCS' 'ZCBKI'
                'ZXYEC' 'SEUIV' 'LOROG' 'CJMPK' 'VOBZI' 'JMKZF' 'WZSCU' 'VCRVV' 'VIGMC' 'OKCDG'
                'UHDKK' 'NBFJD' 'TKYHT' 'BKGXH' 'OQHHK' 'ZEMKE' 'QYTHG' 'JWBOV' 'IDORL' 'TROKU'
                'YYVKC' 'PUYLP' 'FSHPW' 'HGDDP' 'TJSZM' 'VDQOH' 'YRGHN' 'ITKPY' 'PORFF' 'VDBPH'
                'JUUCV' 'NWXJP' 'BRWTY' 'WTGMQ' 'RBGOF' 'YPTMU' 'CBRSC' 'MXBMC' 'KZUJV' 'VMQPP'
                'CBUMO' 'LBGZG' 'RBZYR' 'IQLMK' 'EOQJK' 'XDLJD' 'QQXJI' 'JTJBD' 'MITXY' 'BECYH'
                'XZDXR' 'URBVY' 'FEQVV' 'KQXQG' 'HIGWS' 'BFYSB' 'FJQBG' 'UQJUG' 'PPFET' 'SHNDL'
                'SKXIQ' 'SSFWI' 'NXTWS' 'LYRTP' 'TVRPU' 'ZTFXM' 'BCERR' 'DKOIO' 'SYVJZ' 'UURTB'
                'RWYWZ' 'UPWDF' 'GGTIE' 'SYKIF' 'DPNUL' 'HHREW' 'VULDM' 'HWETM' 'VLSTB' 'OWWBY'
                'NMLTF' 'EGBNB' 'PRYQC' 'UCIDK' 'IJQXZ' 'RMHUQ' 'ROKIB' 'ZNHRM' 'SMSZU' 'YVPBZ'
                'KKZSL' 'WOFLL' 'NSOLJ' 'HSDHW' 'VOEND' 'SQBKS' 'HJOFL' 'JLKWQ' 'TXXFG' 'VZREE')

        def test_Plugboard(self):
            e = Enigma('V', 'II', 'IV', 'C', cables=['AB', 'QZ', 'LM', 'OE', 'NC', 'TW'])
            self.assertEqual(e.translate('A' * 1000),
                'EEPCB' 'EVSCT' 'XNWCC' 'GUXKZ' 'LCGMU' 'VLHYB' 'RSQYR' 'RTJTM' 'QIDJJ' 'BJVHC'
                'TFHYX' 'QPKPM' 'IUCRJ' 'VVRMI' 'VKUQL' 'LPMYX' 'JLWHI' 'QVNQS' 'OCRDR' 'BMCWW'
                'LUVUF' 'XSJRU' 'EVWLN' 'BSRYN' 'UCKTM' 'MXSMI' 'GCCNY' 'HQDKJ' 'XCXWB' 'QTTXZ'
                'TLLYR' 'QLXOE' 'GISKD' 'VBTDT' 'MLDQD' 'VKDUI' 'FKDYF' 'FSNNF' 'EWWSO' 'ISHJL'
                'YNDNL' 'UWUUX' 'HJKJM' 'OOGXG' 'CFLJY' 'XNZES' 'UBZEL' 'HIMUF' 'FFQZM' 'OWVRU'
                'MILYY' 'NTRCR' 'QSJCF' 'UJRBZ' 'CRDLR' 'NLTOK' 'BTXSR' 'YGZXL' 'IUBTV' 'JPXEI'
                'BDOLR' 'DJWXI' 'HGGJE' 'HNKOD' 'EEKHI' 'PKWZP' 'ROGXQ' 'RJWQR' 'TODWO' 'ZIUOX'
                'RDVTI' 'KZDPJ' 'DOPGP' 'TGHNQ' 'WKDRI' 'PVLQO' 'ONQWK' 'TQHJN' 'WGEZS' 'XGMJP'
                'TDHUO' 'IWJWN' 'JKOJN' 'XMMBR' 'UKKOM' 'QVBTF' 'EWJWV' 'TBYVC' 'MEUCM' 'NWVIT'
                'MJJRS' 'KBOFX' 'PKKJY' 'OKHVH' 'CLSXZ' 'JGMFU' 'WSTVX' 'MGQUQ' 'QQJOV' 'FUVOC'
                'XXHHJ' 'IQVFP' 'MKQLU' 'QYHZP' 'NSISQ' 'LGRZH' 'JIRIF' 'ZILTU' 'JMYPG' 'LVKNS'
                'YKYKD' 'GGZWP' 'LVGXR' 'WGNNB' 'EOWHQ' 'PVROI' 'UCEQQ' 'DXVCH' 'ZRBBR' 'HNOPM'
                'GDQGW' 'TLITW' 'OCWIH' 'FIHBS' 'FEBUX' 'PQIRO' 'LTUNG' 'TCCJJ' 'ZTNOX' 'ORRRY'
                'QWFFR' 'RFBQY' 'QYUVG' 'NMREC' 'NHWSW' 'HEGQW' 'EJVCU' 'MYTLN' 'TFTOF' 'FFLCG'
                'SMIFF' 'FOCCQ' 'HHTIH' 'UFIOK' 'EBNVU' 'XXKTU' 'ESENV' 'FPDST' 'FIWXH' 'LSHBC'
                'LKBYV' 'XFFOS' 'RTHZB' 'CVTRQ' 'KCGZM' 'PVXXS' 'ZIPET' 'UXXJR' 'FUGSQ' 'FXWEZ'
                'NYNHZ' 'KIVIV' 'VNVMI' 'VXVQG' 'MLPYP' 'NPNDH' 'KTLTQ' 'XQQZO' 'UONSM' 'VHYMX'
                'IGQCF' 'UGBOH' 'QJJSL' 'YUGHH' 'WQLMN' 'WTMZY' 'EBLLK' 'DSOEW' 'YUNIR' 'CWRWQ'
                'TNBHK' 'LJNNN' 'BMWES' 'TDEKB' 'CJNFZ' 'GVWJM' 'PYDYL' 'EFGYQ' 'GHPVV' 'UIPHU'
                'VZVPX' 'UUQXP' 'PPGKN' 'ZEISZ' 'ZKXHX' 'OPUQX' 'YYTRT' 'MQVLH' 'HOFWM' 'YTNON')

        def test_translate(self):
            e = Enigma('I', 'II', 'III', 'B')
            self.assertEqual(e.translate('A' * 1600),
                'BDZGO' 'WCXLT' 'KSBTM' 'CDLPB' 'MUQOF' 'XYHCX' 'TGYJF' 'LINHN' 'XSHIU' 'NTHEO'
                'RXPQP' 'KOVHC' 'BUBTZ' 'SZSOO' 'STGOT' 'FSODB' 'BZZLX' 'LCYZX' 'IFGWF' 'DZEEQ'
                'IBMGF' 'JBWZF' 'CKPFM' 'GBXQC' 'IVIBB' 'RNCOC' 'JUVYD' 'KMVJP' 'FMDRM' 'TGLWF'
                'OZLXG' 'JEYYQ' 'PVPBW' 'NCKVK' 'LZTCB' 'DLDCT' 'SNRCO' 'OVPTG' 'BVBBI' 'SGJSO'
                'YHDEN' 'CTNUU' 'KCUGH' 'REVWB' 'DJCTQ' 'XXOGL' 'EBZMD' 'BRZOS' 'XDTZS' 'ZBGDC'
                'FPRBZ' 'YQGSN' 'CCHGY' 'EWOHV' 'JBYZG' 'KDGYN' 'NEUJI' 'WCTYC' 'YTUUM' 'BOYVU'
                'NNQUK' 'KSOBS' 'CORSU' 'OSCNV' 'ROQLH' 'EUDSU' 'KYMIG' 'IBSXP' 'IHNTU' 'VGGHI'
                'FQTGZ' 'XLGYQ' 'CNVNS' 'RCLVP' 'YOSVR' 'BKCEX' 'RNLGD' 'YWEBF' 'XIVKK' 'TUGKP'
                'VMZOT' 'UOGMH' 'HZDRE' 'KJHLE' 'FKKPO' 'XLWBW' 'VBYUK' 'DTQUH' 'DQTRE' 'VRQJM'
                'QWNDO' 'VWLJH' 'CCXCF' 'XRPPX' 'MSJEZ' 'CJUFT' 'BRZZM' 'CSSNJ' 'NYLCG' 'LOYCI'
                'TVYQX' 'PDIYF' 'GEFYV' 'XSXHK' 'EGXKM' 'MDSWB' 'CYRKI' 'ZOCGM' 'FDDTM' 'WZTLS'
                'SFLJM' 'OOLUU' 'QJMIJ' 'SCIQV' 'RUIST' 'LTGNC' 'LGKIK' 'TZHRX' 'ENRXJ' 'HYZTL'
                'XICWW' 'MYWXD' 'YIBLE' 'RBFLW' 'JQYWO' 'NGIQQ' 'CUUQT' 'PPHBI' 'EHTUV' 'GCEGP'
                'EYMWI' 'CGKWJ' 'CUFKL' 'UIDMJ' 'DIVPJ' 'DMPGQ' 'PWITK' 'GVIBO' 'OMTND' 'UHQPH'
                'GSQRJ' 'RNOOV' 'PWMDN' 'XLLVF' 'IIMKI' 'EYIZM' 'QUWYD' 'POULT' 'UWBUK' 'VMMWR'
                'LQLQS' 'QPEUG' 'JRCXZ' 'WPFYI' 'YYBWL' 'OEWRO' 'UVKPO' 'ZTCEU' 'WTFJZ' 'QWPBQ'
                'LDTTS' 'RMDFL' 'GXBXZ' 'RYQKD' 'GJRZE' 'ZMKHJ' 'NQYPD' 'JWCJF' 'JLFNT' 'RSNCN'
                'LGSSG' 'JCDLX' 'UJBLT' 'FGKHJ' 'GQUNC' 'QDEST' 'XZDTU' 'WJBRO' 'VGJSF' 'RMRWE'
                'XTVHI' 'ITRFY' 'GPDUF' 'BMHFG' 'IICNX' 'BKEFR' 'QPGDT' 'VHSWN' 'BENJG' 'RHQQQ'
                'CVNIX' 'XNVCO' 'HXYGK' 'PDZIJ' 'ELWNS' 'JISWI' 'UIDNI' 'GHVTG' 'YEVPB' 'MZXYW'
                'VDIKY' 'VEFEK' 'MCTMR' 'UWOWU' 'CJVFU' 'GXLCT' 'SIXTC' 'JNXLK' 'WVHDD' 'DMVPI'
                'MEDXY' 'ZPCIQ' 'PQKLO' 'VERJD' 'UOWRW' 'YCXYK' 'MPPLZ' 'FEWPU' 'NZQMO' 'ETYFO'
                'UXTWT' 'HSYYR' 'EOMUQ' 'CMITU' 'RDSFM' 'MSORL' 'ICQTP' 'PRNWE' 'UPJQE' 'XBCZN'
                'JJWJC' 'UFKOM' 'QIBJL' 'HHYNC' 'VCQYG' 'IBEZF' 'YGTDS' 'FGQYZ' 'UQXYV' 'UDRYT'
                'KIXZL' 'SKRVT' 'EFLSN' 'OIWPX' 'TFQMV' 'JMYWF' 'UPTMY' 'HCZCC' 'XOFSH' 'FFSLW'
                'RSNVM' 'LFQIP' 'BNXWM' 'TRSVF' 'QSPNZ' 'OSULT' 'UNRVQ' 'BUEKD' 'KPPNE' 'YGNVM'
                'HMEEX' 'YRQGX' 'HWWQE' 'XYGBX' 'LEPKS' 'PQSMC' 'XSNGT' 'QSPWG' 'GOQDJ' 'HVRRI'
                'ELKTI' 'GQQKO' 'MBOYO' 'UVGDH' 'TCOEE' 'WKNHH' 'DCOVQ' 'ZBVBB' 'FSPQQ' 'ONXTY'
                'YHXZM' 'RODBB' 'BHZWY' 'DODFL' 'PRUCB' 'DHTCR' 'HTUHH' 'XWJMT' 'OSYUU' 'JZIWX'
                'YEVBK' 'GFHYC' 'SGLTB' 'OBLVS' 'PCQOW' 'BTRVG' 'SGFTF' 'SDNLT' 'MYOXF' 'UGKMZ'
                'ZSOHX' 'CNGFU' 'GQPEL' 'SPSMR' 'TXSTT' 'PIUNL' 'DFIFK' 'CLVSQ' 'WLQON' 'LYVNW'
                'JHYKB' 'HRIHL' 'NGIHD' 'MDSHE' 'JHRZI' 'GZKUM' 'YZVYO' 'PCBMZ' 'YIBTZ' 'FYGID'
                )

        def test_4rotor_as_3rotor(self):
            e3 = Enigma('I', 'II', 'III', 'B')
            e4 = Enigma4('Beta', 'I', 'II', 'III', 'BThin')
            c = 'A' * 1600
            self.assertEqual(e3.translate(c), e4.translate(c))

        def test_4rotor(self):
            e = Enigma4('Gamma', 'VI', 'VII', 'IV', 'CThin', cables=['AX', 'BU', 'FY', 'DH', 'IL', 'MW', 'VP'])
            e.setPosition('QKTE')
            e.setRing('CLRM')
            self.assertEqual(e.translate('A' * 1600),
                'EGRR' 'RKKJ' 'WGPO' 'MEBD' 'TOZB' 'RJJC' 'GXTC' 'JGMV' 'RZWK' 'UJVI' 'ZJDT' 'CICZ'
                'ZXGY' 'EXUG' 'PTQP' 'ELPL' 'XQTW' 'MKBV' 'OXEI' 'WXHG' 'ORSJ' 'FIPH' 'YGUC' 'ITNF'
                'RRPG' 'PRNJ' 'IYEB' 'KXDJ' 'UGIT' 'LRMM' 'NOLC' 'NQTF' 'CJRO' 'WJED' 'SQKH' 'NDLQ'
                'KKWB' 'HPFO' 'TJTC' 'ZPXS' 'JVFT' 'OLEG' 'VBLM' 'UFRF' 'NGMF' 'ESIQ' 'ZQKG' 'HYWX'
                'WDXX' 'ELXT' 'KPHX' 'QNGW' 'HXRW' 'DVOJ' 'GWHZ' 'VVNQ' 'JOVG' 'ZGFK' 'KZID' 'FCWE'
                'RUGW' 'EJIY' 'CTDB' 'NICG' 'IRHQ' 'ITUB' 'ODZU' 'UELQ' 'HLDG' 'LRLC' 'KBUU' 'XDCO'
                'TNEK' 'DZBG' 'UDQZ' 'PJTQ' 'KPQW' 'YXYP' 'NNYJ' 'DFHG' 'EHXI' 'DXDW' 'LRSX' 'WREI'
                'HQDL' 'OKQY' 'FCLS' 'VYET' 'WRLY' 'RGZY' 'QQNO' 'MUEW' 'KLZQ' 'QLSQ' 'YFPR' 'IUHU'
                'QGQQ' 'XOII' 'BWJJ' 'MLCC' 'STKC' 'MTIH' 'JSGS' 'PRQN' 'JVSB' 'UYRS' 'POYJ' 'ZQDV'
                'ERUJ' 'EPRB' 'JLKF' 'LPFN' 'NIFZ' 'EFVK' 'IORM' 'NLJH' 'OEUK' 'UTKF' 'OWSX' 'XYOI'
                'JVBN' 'MKVM' 'WBBZ' 'TZCC' 'VNWV' 'NMXS' 'JNVZ' 'WNPH' 'GCTI' 'KZPP' 'XOMO' 'VVII'
                'ZJIM' 'VKIP' 'YIIZ' 'JQLY' 'STRD' 'FGYQ' 'GTOI' 'OESL' 'HGOI' 'DCIL' 'BUET' 'BOPQ'
                'BYLJ' 'LUQS' 'MTGS' 'HOZO' 'PBOD' 'UBCY' 'INMR' 'WMMD' 'IRGK' 'JTQH' 'FLJQ' 'KROK'
                'RKKB' 'ZUUU' 'OYHG' 'MNBW' 'ZFZG' 'ZZEI' 'KYEC' 'VQMB' 'RUSH' 'FJZD' 'ZXUV' 'QLBG'
                'ZHHQ' 'IQKP' 'HUUV' 'XYPI' 'BWDN' 'WRMV' 'WOLZ' 'WXZZ' 'VGXG' 'YBPY' 'YWNC' 'LLGG'
                'QFBZ' 'VNZY' 'ESVV' 'HFEK' 'OKGT' 'LIMR' 'EHWX' 'YTTQ' 'ROFH' 'LQIR' 'JDSV' 'DFJK'
                'SFBN' 'UBJK' 'CMJR' 'GVDF' 'FGHY' 'EXHF' 'XXXL' 'VJEB' 'EXSN' 'KVHE' 'OFRO' 'WBQK'
                'CEGI' 'DKPR' 'YUCL' 'DJPM' 'BPUV' 'LZCU' 'IKGC' 'IICH' 'FDWZ' 'UUUT' 'YIQN' 'TZIM'
                'TRWC' 'RXBN' 'DJZR' 'JYVF' 'QXGG' 'YRPW' 'URLK' 'ELQF' 'UGJX' 'KVFR' 'RTJH' 'OKFW'
                'OFZV' 'NWHF' 'PUVW' 'LCKJ' 'MFYB' 'NGRX' 'CDFN' 'XTJM' 'JVBG' 'OCGO' 'HFUB' 'OHKE'
                'JFUD' 'FYFH' 'SNQT' 'TSHQ' 'FPGX' 'IUSE' 'VYTD' 'VSIU' 'YRJU' 'KVFP' 'BDBI' 'DXFI'
                'FZOW' 'UYEC' 'CUZL' 'BWPH' 'YLBS' 'XCQP' 'BQMJ' 'HGLV' 'TIJX' 'SEVF' 'MUBL' 'OOGZ'
                'HBBN' 'YUQP' 'RBQK' 'NWSZ' 'WVRS' 'RLGS' 'WBJP' 'BLVZ' 'LLBY' 'EZKC' 'SBQP' 'SHCK'
                'ZKSP' 'MKIQ' 'JKHY' 'VUGD' 'FPYP' 'HXGW' 'IWNX' 'QWUW' 'PMTQ' 'EIHQ' 'RQQM' 'GZME'
                'XLVC' 'KPSN' 'KYVS' 'UKXZ' 'QZGD' 'FZWQ' 'TOBI' 'MKIS' 'CSJP' 'TTEF' 'YDYU' 'YNHC'
                'CFPL' 'HBXU' 'MUYM' 'CJZX' 'NDMF' 'ISSB' 'SEMQ' 'GULI' 'KXQT' 'OWOH' 'SEGM' 'EIFN'
                'WRYK' 'QKLL' 'HFQU' 'TUBE' 'THUW' 'GDNV' 'JNSC' 'SIFE' 'RDLM' 'RJUT' 'TIBB' 'CRVC'
                'MWVS' 'LGCR' 'PJWJ' 'LCZE' 'GTTT' 'NOJV' 'CLPR' 'WJBJ' 'UBUY' 'CKPP' 'YGBO' 'ZMUF'
                'PNNT' 'ZFVI' 'FQQD' 'GUUJ' 'XDCR' 'LVFN' 'JOPV' 'XVTZ' 'WHOM' 'QCGU' 'JJLV' 'CFQT'
                'FBDO' 'YIOZ' 'DLBY' 'ESYF' 'LFTN' 'ETTL' 'RNZT' 'ZJBX' 'SFZR' 'VHYM' 'OBSM' 'RRFK'
                'ZJJI' 'UURJ' 'YVGB' 'DSWN' 'CJGN' 'LLVH' 'VQGO' 'IECY' 'NWWB' 'XVOO' 'UJOI' 'NYIX'
                'GWMD' 'RRFC' 'OCOL' 'UDVN' 'QGJW' 'PKWW' 'FUUN' 'HMGU' 'UNOX' 'ZVWR' 'SCFH' 'NWLG'
                'ERIL' 'XNHJ' 'FURD' 'UUEJ' 'VWSY' 'WSSZ' 'MILI' 'WEGH' 'VFBD' 'OMRO' 'OBCP' 'DHNE'
                'LHUM' 'PXPE' 'RTXP' 'BJON')

        def test_match(self):
            eA = Enigma('I', 'II', 'III', 'B')
            eB = Enigma('I', 'II', 'III', 'B')
            eC = Enigma('I', 'II', 'III', 'C')
            p = 'A' * 1600
            c = eA.translate(p)
            self.assertTrue(eB.match(p, c))
            self.assertFalse(eC.match(p, c))

        def test_half_double_step(self):
            e = Enigma('I', 'IV', 'V', 'B', pos='FJN', ring='AOA', cables=['AL', 'CT', 'FN', 'OY'])
            p = e.translate('A')
            self.assertEqual(p, 'B')
            self.assertEqual(e.getPosition(), 'GKO')
            e.setPosition('GJO')
            p = e.translate('A')
            self.assertEqual(p, 'Q')
            self.assertEqual(e.getPosition(), 'HKP')

    unittest.main()