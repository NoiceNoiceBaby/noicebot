###################################################################################################################################################
# IMPORTS
###################################################################################################################################################
import aiohttp

###################################################################################################################################################
# API
###################################################################################################################################################
async def get(apiKey, mimeType):
    # lists
    headers = {
        "x-api-key" : apiKey,
        "content-Type" : "application/json"
    }
    # lists 
    parameters = {
        "mimeTypes" : mimeType
    }

    # variables to declare 
    API = "https://api.thecatapi.com/v1/images/search"

    # session
    async with aiohttp.ClientSession() as catapiSession:
        async with catapiSession.get(API, headers=headers, params=parameters) as catapiResponse:
            if catapiResponse.status != 200 or "application/json" not in catapiResponse.headers["content-Type"]:
                return "API is unreachable, try again later"
            else:
                url = await catapiResponse.json()
                return url[0]["url"]

###################################################################################################################################################
# END OF FILE
###################################################################################################################################################