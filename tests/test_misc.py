import unittest
from uk_post_code import parse_uk_postcode


class UkPostCodeTestCase(unittest.TestCase):
    def testParse(self):
        self.assertEqual(parse_uk_postcode('SW1W 0NY'), ('SW1W', '0NY'))
        self.assertEqual(parse_uk_postcode('PO167GZ'), ('PO16', '7GZ'))
        self.assertEqual(parse_uk_postcode('WC1A1AA'), ('WC1A', '1AA'))

    def testLength(self):
        self.assertRaises(ValueError, parse_uk_postcode, 'SW1V1QR1')
        self.assertRaises(ValueError, parse_uk_postcode, 'SW1V')

    def testArea(self):
        for c in 'QVX':
            self.assertRaises(ValueError, parse_uk_postcode, '%sA1V1QR1' % c)
        for c in 'IJZ':
            self.assertRaises(ValueError, parse_uk_postcode, 'C%s1 4' % c)

    def testDistrict(self):
        self.assertRaises(ValueError, parse_uk_postcode, 'BR98 1AA')
        self.assertRaises(ValueError, parse_uk_postcode, 'SO1 2EU')


    def testUnit(self):
        for c in 'CIKMOV':
            self.assertRaises(ValueError, parse_uk_postcode, 'L18J%s' %c)
            self.assertRaises(ValueError, parse_uk_postcode, 'GU16 7%sF' %c)

    #@unittest.skip('Long test')
    def testAll(self):
        import csv, io, sys, re
        import urllib, zipfile, StringIO
        print 'Fetching postcodes file...'
        zf = urllib.urlopen('http://www.doogal.co.uk/files/postcodes.zip').read()
        print 'Opening file...'
        with zipfile.ZipFile(StringIO.StringIO(zf), 'r') as z:
            f = z.open('postcodes.csv', 'r')
            f.readline()  # skip header
            reader = csv.reader(io.BufferedReader(f), delimiter=',')
            print 'Checking each row...'
            i = 0
            for row in reader:
                pc = row[0]
                if pc[:3] in ('NPT', 'W1M', 'W1N', 'W1R',
                              'W1V', 'W1X', 'W1Y',): continue  # deprecated
                if pc[:4] in ('BR98', 'SR43', 'SR88', 'WC99'): continue  # deprecated
                if re.match(r'^AB[1-9] $', pc[:4]): continue  # deprecated
                if re.match(r'^SO[1-9] $', pc[:4]): continue  # deprecated

                parse_uk_postcode(pc)
                i += 1
                if i % 10000 == 0 :
                    print i, '...' ,
                    sys.stdout.flush()
            print


if __name__ == '__main__':
    unittest.main()
