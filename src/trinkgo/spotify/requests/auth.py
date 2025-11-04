#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.09.25                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


import requests


def get_access_token(code: str, protocol_and_netloc: str):
	# FROM: https://developer.spotify.com/documentation/web-playback-sdk/howtos/web-app-player
	#    @: Request Access Token
	url = "https://accounts.spotify.com/api/token"
	headers = {
		"Authorization": "Basic OGRjN2Y4Yjc1NzkzNGQ5ZWJhZjM5ZjkzNDdiY2NjNTY6N2U5YzQyMTI3OWI3NGQ2OWE2YTliNTBlNDkzY2ZhOGU=",
		"Content-Type": "application/x-www-form-urlencoded",
	}
	params = {
		"code": code,
		"grant_type": "authorization_code",
		"redirect_uri": f"{protocol_and_netloc}/authenticated",
	}
	response = requests.post(url, headers=headers, params=params)

	return response.json()


def refresh_access_token(refresh_token: str):
	# FROM: https://developer.spotify.com/documentation/web-api/tutorials/refreshing-tokens
	url = "https://accounts.spotify.com/api/token"
	headers = {
		"Content-Type": "application/x-www-form-urlencoded",
		"Authorization": "Basic OGRjN2Y4Yjc1NzkzNGQ5ZWJhZjM5ZjkzNDdiY2NjNTY6N2U5YzQyMTI3OWI3NGQ2OWE2YTliNTBlNDkzY2ZhOGU=",
	}
	params = {
		"grant_type": "refresh_token",
		"refresh_token": refresh_token,
	}
	response: requests.Response = requests.post(url, headers=headers, params=params)
	response.raise_for_status()

	return response.json()
