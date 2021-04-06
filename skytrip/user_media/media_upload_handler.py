from skytrip.user_media.media_config import UserMediaConfig
import boto3
import base64
import json
from skytrip.utils.helper import get_root_exception_message, get_exception_message, finalize_response
import inspect
from skytrip.user_media.db_handler import DBhandler


class MediaUploadHandler:
    
    __user_media_config = UserMediaConfig()

    def __init__(self, EventBodyData=None):
        self.event_body_data = EventBodyData

    def format_response(self, response_dict={}):
        statusCode = 200

        formatted_response = {
            "statusCode": statusCode,
            "body": {
                "responseData": response_dict
            }
        }

        return formatted_response


    def validate_media_upload_request(self, EventBodyData=None):
        try:
            target_validation_fields = [
                "UserID", "Username", "MediaBase64String", "MediaCategory", "MediaContentType", "MediaExtension"
            ]

            for validation_field in target_validation_fields:
                # validate if exists user ID
                if EventBodyData.get(validation_field, None) is None:
                    raise ValueError(
                        get_exception_message(
                            Ex=None, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                            msg=f"{validation_field} is required! Pass {validation_field} with the request parameter."
                        )
                    )
            
            # return body data
            return EventBodyData

        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to validate media upload request!"
                )
            )

    def upload_media(self):
        result = None

        try:
            # validate request
            self.validate_media_upload_request(EventBodyData=self.event_body_data)
            # S3 Config
            s3 = boto3.client("s3")
            s3_root_url = "https://skytripb2cmedia.s3-ap-southeast-1.amazonaws.com/"
            # User Information
            user_id = self.event_body_data.get("UserID", None)
            username = self.event_body_data.get("Username", None)
            #  Media Information
            MediaBase64String = self.event_body_data.get("MediaBase64String", None)
            media_category = self.event_body_data.get("MediaCategory", None).upper()
            media_content_type = self.event_body_data.get("MediaContentType", None)
            media_extension = self.event_body_data.get("MediaExtension", None)
            # Define folder Location
            folder_loc = f"Users/{username}/Media/{media_category}/"
            media_file_name = str(user_id) + "_" + str(username) + "_" + str(media_category) + str(media_extension)
            decoded_content = base64.b64decode(MediaBase64String)

            # Upload Media to S3
            s3.put_object(
                Bucket=self.__user_media_config.bucket_name, 
                Key=folder_loc + media_file_name,
                ContentType=media_content_type,
                Body=decoded_content,
                ACL='public-read-write',
                ServerSideEncryption='AES256'
            )

            # s3_bucket_url = self.__user_media_config.bucket_url

            # Assign uploaded media file URL to result
            result = {
                "MediaS3URL": s3_root_url + folder_loc + media_file_name
            }

            # get formatted response
            formatted_response = self.format_response(result)

            # ------------------- *** validate structure and finalize response *** -------------------
            finalized_response = finalize_response(response=formatted_response)

            # ------------------- *** insert uploaded media data into Database *** -------------------
            if finalized_response.get("statusCode", None) == 200:
                db_handler = DBhandler()
                db_uploaded_media_id = db_handler.insert_data(
                    request=self.event_body_data,
                    response=finalized_response
                )
                # insert DBpnrID in finalized response
                finalized_response["body"]["responseData"]["DBuploadedMediaID"] = db_uploaded_media_id

            # return finalized resposne
            return finalized_response

        # ------------------- *** handle exceptions *** -------------------
        except Exception as E:
            return get_root_exception_message(
                Ex=E, gdsResponse=None, appResponse=result, file=__file__,
                parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                msg="Failed to upload media!"
            )
