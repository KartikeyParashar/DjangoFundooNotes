import logging
import boto3
from botocore.exceptions import ClientError
from django.http.response import HttpResponse

from FUNDOONOTES import settings

logger = logging.getLogger(__name__)


class CloudUpload:

    def upload_image(self, image):
        """

        :param image:request the image from the user
        :return:True, if image uploaded successfully else returns False
        """
        # import pdb
        # pdb.set_trace()
        upload = boto3.resource('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                region_name=settings.AWS_LOCATION)
        try:
            upload.meta.client.upload_fileobj(image, settings.AWS_STORAGE_BUCKET_NAME, str(image))
            return True
        except ClientError as e:
            logger.error(e)
            return False
        except Exception:
            return False
