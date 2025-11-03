#!/opt/homebrew/bin/python3
# -*- coding: utf-8 -*-
__author__ = "MPZinke"

########################################################################################################################
#                                                                                                                      #
#   created by: MPZinke                                                                                                #
#   on 2025.06.01                                                                                                      #
#                                                                                                                      #
#   DESCRIPTION:                                                                                                       #
#   BUGS:                                                                                                              #
#   FUTURE:                                                                                                            #
#                                                                                                                      #
########################################################################################################################


from spotify.classes import Song
from webapp.router import app
from webapp.router.api import api_blueprint
from webapp.router.auth import auth_blueprint, login_manager
from webapp.router.events import events_blueprint
from webapp.router.home import home_blueprint
from webapp.router.playlists import playlists_blueprint


def main():
	login_manager.init_app(app)
	app.register_blueprint(api_blueprint)
	app.register_blueprint(auth_blueprint)
	app.register_blueprint(events_blueprint)
	app.register_blueprint(home_blueprint)
	app.register_blueprint(playlists_blueprint)
	app.run(host="0.0.0.0", port=8080, debug=True)


main()
