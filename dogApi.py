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
    API = "https://api.thedogapi.com/v1/images/search"

    # session
    async with aiohttp.ClientSession() as dogapiSession:
        async with dogapiSession.get(API, headers=headers, params=parameters) as dogapiResponse:
            if dogapiResponse.status != 200 or "application/json" not in dogapiResponse.headers["content-Type"]:
                return "API is unreachable, try again later"
            else:
                url = await dogapiResponse.json()
                return url[0]["url"]

###################################################################################################################################################
# END OF FILE
###################################################################################################################################################