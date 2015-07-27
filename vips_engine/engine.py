from tempfile import NamedTemporaryFile

from thumbor.engines import BaseEngine
from gi.repository import Vips

C_NO_WEBP_OUTPUT = 'VIPS_ENGINE_NO_WEBP_OUTPUT'

C_SCALE_ON_LOAD = 'VIPS_ENGINE_SCALE_ON_LOAD'

C_TMP_DIR = 'VIPS_ENGINE_TMP_DIR'

__author__ = 'konstantin.burov'


class Engine(BaseEngine):
    @property
    def size(self):
        return self.image.width, self.image.height

    def create_image(self, buffer):
        if self.get_mimetype(buffer) == 'image/jpeg' and self.context.config.get(C_SCALE_ON_LOAD, True):
            self._f = NamedTemporaryFile(bufsize=len(buffer), dir=self.context.config.get(C_TMP_DIR, None))
            self._f.write(buffer)
            # just read image width and height
            vips_image = Vips.Image().new_from_file(self._f.name, access=Vips.Access.SEQUENTIAL)
            width = vips_image.width
            height = vips_image.height
            factor = 1
            out_width = self.context.request.width
            out_height = self.context.request.height
            while width/factor > out_width*2 and height*2/factor > 2*out_height:
                factor *= 2
            vips_image = Vips.Image().new_from_file(self._f.name, access=Vips.Access.SEQUENTIAL, shrink=factor)
        else:
            vips_image = Vips.Image().new_from_buffer(data=buffer, option_string=None)
        return vips_image

    def resize(self, width, height):
        self.image = self.image.resize(width/self.size[0])

    def read(self, extension, quality):
        if extension == '.gif':
            # VIPS doesn't support gif output, fall back to PNG
            extension = '.png'
        if extension == '.webp' and self.context.config.get(C_NO_WEBP_OUTPUT, False):
            extension = '.jpg'
        if extension == '.jpg' or extension == '.webp':
            format_string = "{}[Q={}]".format(extension, int(quality))
        else:
            format_string = extension
        to_buffer = self.image.write_to_buffer(format_string=format_string)
        if hasattr(self, '_f'):
            self._f.close()
        return to_buffer

    def crop(self, left, top, right, bottom):
        self.image = self.image.crop(left, top, right-left, bottom-top)

    def normalize(self):
        pass
