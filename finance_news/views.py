import os
import json
import pandas as pd
from django.http import HttpResponse, HttpResponseBadRequest

from chatbot.utils.logger import logger


def append_data_to_csv(res: pd.DataFrame, path: str) -> None:
    hdr = False if os.path.isfile(path) else True
    res.to_csv(path, mode="a", header=hdr, index=False)


def index(request):
    try:
        logger.info("Request received")
        logger.info(request.body)

        body = json.loads(request.body)

        result_df = pd.DataFrame(body, index=[0])
        file_path = "./finance_news.csv"
        append_data_to_csv(result_df, file_path)

        return HttpResponse("200")

    except Exception as e:
        logger.error(f"Error: {e}")
        return HttpResponseBadRequest()
