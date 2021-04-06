# import necessary libraries and packages
from skytrip.utils.helper import finalize_response, get_exception_message
import inspect
import datetime

class DBreadHelper:

    def map_response(self, response=[], target_map={}):
        """
        map_response() => Maps Database Query Response to Object.
        params => response (array)
        """
        try:

            result = []

            for record in response:

                # define initial num of iteration
                numOfIteration = 0

                # make a copy of original map so that it doesn't change with each record update
                original_map = target_map.copy()

                # loop through target maps
                for key, value in target_map.items():

                    # check if data type is datetime -> If so then convert to string
                    if type(record[numOfIteration]) == datetime.datetime:
                        # assign map value
                        target_map[key] = record[numOfIteration].strftime("%Y-%m-%d %H:%M:%S")
                    else:
                        # assign map value
                        target_map[key] = record[numOfIteration]

                    # increment iterator
                    numOfIteration += 1

                # insert record into result array
                result.append(target_map)
                
                # replace updated map with original map
                target_map = original_map

            # format response
            formatted_response = {
                "statusCode": 200,
                "body": {
                    "responseData": result
                }
            }
            
            # return formatted response
            return formatted_response
        
        # ------- Handle Exceptions -------
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to Map Response!"
                )
            )

    def map_detail_response(self, response=[], target_map={}):
        """
        map_detail_response() => Maps Database Query Response to Object.
        params => response (array)
        """
        try:

            # define initial num of iteration
            numOfIteration = 0

            # loop through target maps
            for key, value in target_map.items():

                # check if data type is datetime -> If so then convert to string
                if type(response[numOfIteration]) == datetime.datetime:
                    # assign map value
                    target_map[key] = response[numOfIteration].strftime("%Y-%m-%d %H:%M:%S")
                else:
                    # assign map value
                    target_map[key] = response[numOfIteration]

                # increment iterator
                numOfIteration += 1

            # format response
            formatted_response = {
                "statusCode": 200,
                "body": {
                    "responseData": target_map
                }
            }
            
            # return formatted response
            return formatted_response
        
        # ------- Handle Exceptions -------
        except Exception as E:
            raise Exception(
                get_exception_message(
                    Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                    msg="Failed to Map Detail Response!"
                )
            )
