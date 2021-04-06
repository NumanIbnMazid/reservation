"""
Helper File for SKYTRIP Application
"""
# import necessary modules and libraries
import inspect
import json
import errno
import json
import os
import psycopg2
import boto3
from skytrip_config.config import SkyTripConfig


"""
************************ Generate Exception Message Functions ************************
"""


def get_root_exception_message(Ex=None, gdsResponse=None, appResponse=None, file=None, parent=None, line=None, msg=None, severity="Error"):
    """
    get_root_error() => Generates error for root handler of skytrip modules.
    params => Ex (Exception Object), gdsResponse (response from gds), appResponse (response from skytrip), file (__file__), parent (parent method/function/class), line (line number), msg (custom exception message)
    return => Object (Formatted error message)
    """
    message = {}
    statusCode = 400
    available_severities = ["error", "warning", "info", "success"]

    try:

        if type(appResponse) == dict:
            if appResponse is not None:
                statusCode = appResponse.get("statusCode", statusCode)
            elif gdsResponse is not None:
                statusCode = gdsResponse.get("statusCode", statusCode)
            else:
                statusCode = 400

        exceptionDescription = get_exception_message(
            Ex=Ex, file=file, parent=parent, line=line, msg=msg
        )

        severities_present = [severity.title() for severity in exceptionDescription.split("~") if severity.lower() in available_severities]

        selected_severity = max(severities_present) if len(severities_present) >= 1 else available_severities[0].title()

        message = {
            'statusCode': statusCode,
            'body': {
                "responseData": {
                    "Messages": {
                        "Severity": f"@**{selected_severity}**@",
                        "Description": exceptionDescription,
                        "GDS_Response": gdsResponse,
                        "App_Response": appResponse
                    }
                }
            }
        }

    except Exception as E:

        message = {
            'statusCode': statusCode,
            'body': {
                "responseData": {
                    "Messages": {
                        "Severity": "@**Error**@",
                        "Description": f"An Exception Occured! \n Arguments: [{str(E)}]",
                        "GDS_Response": None,
                        "App_Response": None
                    }
                }
            }
        }
    
    return message


def get_exception_message(Ex=None, file=None, parent=None, line=None, msg=None, severity="Error"):
    """
    get_exception_message() => Generates dynamic exception messages.
    params => Ex (Exception object), file (__file__), parent (parent method/function/class), line (line number), msg (custom exception message)
    return => message (dynamically generated exception message) 
    """
    # define util vars
    tab = "\t"
    br = "\n"
    empty = ""
    common_msg = "An Exception Occured!"

    try:
        # get file name
        filename = file.split("/")[-1].replace(".py", "")
        if Ex is not None:
            message = f"**[ ~{severity}~ ({filename}) -> {parent} -> {line}: {br} Exception Type: {Ex.__class__.__name__} {br} Arguments: [{str(Ex)}] {br if msg is not None else empty} {msg if msg is not None else empty} ]**"
            # message = {
            #     "object": "Error!",
            #     "filename": filename,
            #     "parent": parent,
            #     "linenumber": line,
            #     "exception_type": Ex.__class__.__name__,
            #     "exception_object": str(Ex),
            #     "message": msg
            # }
        else:
            message = f"**[ ~{severity}~ ({filename}) -> {parent} -> {line}: {common_msg if msg is None else empty} {br if msg is not None else empty} {msg if msg is not None else empty} ]**"
            # message = message = {
            #     "object": "Error!",
            #     "filename": filename,
            #     "parent": parent,
            #     "linenumber": line,
            #     "message": msg
            # }
    except Exception as E:
        message = f"**[ ~{severity}~ {common_msg} {br} Ex={Ex}, file={file}, parent={parent}, line={line}, msg={msg} {br}{tab} Exception Handler Failure Message: {str(E)} ]**"
        # message = {
        #     "object": "Error!",
        #     "filename": filename,
        #     "parent": parent,
        #     "linenumber": line,
        #     "message": msg if msg is not None else common_msg
        # }

    return message



"""
************************ Finalize Response ************************
"""


def finalize_response(response=None):
    """
    finalize_response() => Finalizes response and checks if meets skytrip standard response structure if not then adopts.
    params => response (response from gds)
    return => object (Formatted response)
    """
    ideal_node = {
        'statusCode': None,
        'body': {
            "responseData": None
        }
    }

    finalized_node = {}
    num_validator = 3
    validator_results = []

    try:

        if response is not None:
            if type(response) == dict:
                # define status code
                if "statusCode" not in response.keys():
                    finalized_node["statusCode"] = 400
                else:
                    validator_results.append(1)
                
                # define body
                if "body" not in response.keys():
                    finalized_node["body"] = {
                        "responseData": response
                    }
                else:
                    validator_results.append(1)
                
                # define response data
                if "body" in response.keys() and "responseData" not in response["body"].keys():
                    finalized_node["body"]["responseData"] = response
                else:
                    validator_results.append(1)
            else:
                finalized_node = ideal_node
                finalized_node["statusCode"] = 400
                finalized_node["body"]["responseData"] = response
        else:
            return ideal_node

    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                msg=f"Failed to finalize response!"
            )
        )

    # return response
    if validator_results.count(1) < num_validator:
        return finalized_node
    return response



"""
************************ Generate JSON File Functions ************************
"""

def get_req_res_target_dir(gds_name="other"):
    """
    get_req_res_target_dir() => generates requests and responses target directory to save JSON files.
    params => gds_name (string)
    return => object => {"gds_name": {"req": "example/requests/directory/", "res": "example/response/directory/"}}
    """
    # requests and responses sample save directory
    req_res_parent_dir = "Req_Res_Samples/"
    # generate directories
    responses_target_dir = req_res_parent_dir + "responses/"
    requests_target_dir = req_res_parent_dir + "requests/"
    dirs = {}
    dirs[gds_name.lower()] = {
        "req": requests_target_dir + gds_name.lower() + "/",
        "res": responses_target_dir + gds_name.lower() + "/"
    }
    return dirs


def create_dirs_files(filename="test", create_init=True):
    """
    create_dirs_files() => dynamically creates directories and files.
    params => filename (string)
    """
    if not os.path.exists(os.path.dirname(filename)):
        try:
            # os.makedirs(os.path.dirname(filename))
            # __init__.py file generation
            dirs = filename.split("/")
            target_dirname = ""
            for idx, single_dir in enumerate(dirs):
                if not idx == len(dirs) - 1:
                    target_dirname = target_dirname + single_dir + "/"
                    if not os.path.exists(os.path.dirname(target_dirname)):
                        os.makedirs(os.path.dirname(target_dirname))

                        # create init file
                        if create_init == True:
                            target_filename = target_dirname + "__init__.py"
                            f = open(target_filename, "w+")
                            f.close()

        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def generate_json(gds="other", isReq=False, filename="test", data=None, files=None):
    """
    generate_json() => Generates json file.
    params => gds (string), isReq (boolean), filename (string), data (any), files (list)
    """
    try:

        if files == None:
            target_dir = get_req_res_target_dir(gds)
            data_type = "req" if isReq == True else "res"
            filename = target_dir[gds][data_type] + filename
            # create dirs and files
            create_dirs_files(filename=filename)
            # generate json file
            with open(filename, "w") as outfile:
                json.dump(data, outfile, indent=4)
        else:
            generate_JSON_files_from_list(files=files)

    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[0][2],
                msg=f"Failed to generate JSON file(s)!"
            )
        )


def generate_JSON_files_from_list(files=[]):
    """
    generate_JSON_files() => Generates json files from list.
    params => files (list)
    """
    # loop through files
    for file in files:
        # generate json file
        generate_json(
            gds=file["gds"], isReq=file["isReq"], filename=file["filename"], data=file["data"], files=None
        )


"""
************************ Databse Helper Functions ************************
"""


def connect_db():
    """
    connect_db() => Connects to AWS RDS and returns connection instance.
    """
    try:
        __skytrip_conf = SkyTripConfig()
        con = psycopg2.connect(
            database=__skytrip_conf.db_name,
            host=__skytrip_conf.db_host,
            port=__skytrip_conf.db_port,
            user=__skytrip_conf.db_user,
            password=__skytrip_conf.db_password,
        )

        # return connection instance
        return con

    except Exception as E:
        raise Exception(
            get_exception_message(
                Ex=E, file=__file__, parent=inspect.stack()[0][3], line=inspect.stack()[
                    0][2],
                msg=f"Failed to create db connection!"
            )
        )
