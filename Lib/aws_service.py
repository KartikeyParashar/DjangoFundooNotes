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

    def simple_notification_service(self, Phone_Number):
        """

        :param Phone_Number:request the Phone Number of User
        :return:True, if image uploaded successfully else returns False
        """
        # create an SNS client
        client = boto3.client("sns", aws_access_key_id=settings.AWS_SNS_ACCESS_KEY_ID,
                              aws_secret_access_key=settings.AWS_SNS_SECRET_ACCESS_KEY,
                              region_name=settings.AWS_LOCATION)
        try:
            # sent your sms message
            client.publish(
                PhoneNumber=str(Phone_Number),
                Message="We are delighted that you have started your Fundoo Application!!.."
                        "We look forward to your service"
            )
            return True
        except Exception:
            return False
