from datetime import datetime
import io
from tempfile import NamedTemporaryFile, SpooledTemporaryFile

__author__ = 'konstantin.burov'

from gi.repository import Vips

if __name__ == '__main__':
    now = datetime.now()
    vips_image = Vips.Image().jpegload('/Users/konstantin.burov/tmp/w5616-h3744-2012102200_1_pi_150708_072254.jpeg', shrink=8, access=Vips.Access.SEQUENTIAL)
    print vips_image.width
    print datetime.now() - now

    b = open('/Users/konstantin.burov/tmp/w5616-h3744-2012102200_1_pi_150708_072254.jpeg', 'rU').read()

    now = datetime.now()
    f = NamedTemporaryFile(delete=True)
    f.write(b)
    vips_image = Vips.Image().jpegload(f.name, shrink=8, access=Vips.Access.SEQUENTIAL)
    print vips_image.width
    print datetime.now() - now
    now = datetime.now()
    vips_image.write_to_buffer(format_string='.jpg')
    print datetime.now() - now
    f.close()
