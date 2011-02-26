from google.appengine.api import lib_config
from google.appengine.ext import db
from google.appengine.ext.webapp import blobstore_handlers


class ImageUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        try:
            image = None
            key = self.request.get('key', None)
            if key is not None:
                image = db.get(db.Key(encoded=key))
            if image is not None:
                uploads = self.get_uploads()
                if len(uploads) == 1:
                    image.blob_info = uploads[0]
                    image.put()
                    from agar.image import ConfigDefaults
                    config = lib_config.register('agar_image', ConfigDefaults.__dict__)
                    self.redirect(config.UPLOAD_URL)
                else:
                    import logging
                    logging.error("OLD: No uploaded image found")
                    self.error(400)
            else:
                import logging
                logging.error("OLD: No valid image key provided: %s" % key)
                self.error(400)
        except Exception, e:
            import logging
            logging.error("OLD: Image upload exception: %s" % e)
            from agar.env import on_production_server
            self.handle_exception(e, not on_production_server)
