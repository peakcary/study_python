import requests


def upload_file(file_path, url="http://192.168.1.202:7672/front/file/data/upload"):
    """
    Upload a file to the specified URL.

    :param file_path: Path to the file to upload.
    :param url: The URL of the upload service.
    :return: A dictionary with the status and response details.
    """
    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            files = {'file': file}

            # Send POST request to the upload endpoint
            response = requests.post(url, files=files)

            # Raise an exception for HTTP errors
            response.raise_for_status()

            return {
                "status": "success",
                "status_code": response.status_code,
                "response_text": response.text
            }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": "File not found. Please check the file path."
        }
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e)
        }


# Example usage
file_path = "/Users/peakom/Downloads/1.jpg"  # Replace with your file path
response = upload_file(file_path)
print(response)