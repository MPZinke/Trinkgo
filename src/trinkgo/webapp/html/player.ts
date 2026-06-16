
var PLAYER: Player | null = null;


// FROM: https://developer.spotify.com/documentation/web-playback-sdk/reference#spotifyplayer
interface SpotifyPlayerInterface
{
	connect(): Promise<void>;
	disconnect(): Promise<void>;
	addListener(event_name: string, callback: (web_playeback_player:WebPlaybackPlayer)=>void): boolean;
	addListener(event_name: string, callback: (web_playeback_state:WebPlaybackState)=>void): boolean;
	removeListener(event_name: string): boolean;
	removeListener(event_name: string, callback: (web_playeback_player:WebPlaybackPlayer)=>void): boolean;
	getCurrentState(): Promise<void>;
	setName(name: string): Promise<void>;
	getVolume(): Promise<number>;
	setVolume(volume: number): Promise<void>;
	pause(): Promise<void>;
	resume(): Promise<void>;
	togglePlay(): Promise<void>;
	seek(position_ms: number): Promise<void>;
	previousTrack(): Promise<void>;
	nextTrack(): Promise<void>;
	activateElement(): Promise<void>;
}


interface WebPlaybackPlayer
{
	device_id: string;
}


interface WebPlaybackState
{
	context: {
		uri: string,
		metadata: object,
	},
	disallows: {
		pausing: boolean,
		peeking_next: boolean,
		peeking_prev: boolean,
		resuming: boolean,
		seeking: boolean,
		skipping_next: boolean,
		skipping_prev: boolean

	},
	paused: boolean,
	position: number,
	repeat_mode: number,

	shuffle: boolean,
	track_window: {
		current_track: WebPlaybackTrack,
		previous_tracks: WebPlaybackTrack[],
		next_tracks: WebPlaybackTrack[],
	}
}


interface WebPlaybackTrack
{
	uri: string,
	id: string,
	type: string,
	media_type: string,
	name: string,
	is_playable: true,
	album: {
		uri: string,
		name: string,
		images: [
			{url: string}
		]
	},
	artists: [
		{uri: string, name: string}
	]
}


class Player
{
	id: string | null;
	playing: string | null;
	is_ready: boolean;
	player: SpotifyPlayerInterface;
	on_play: ()=>void;
	on_pause: ()=>void;
	timer: Timer | null;


	constructor()
	{
		this.id = null;
		this.playing = null;
		this.is_ready = false;
		this.player = new (window as any).Spotify.Player(
			{
				name: 'trinkgo',
				getOAuthToken: (cb: (auth_token: string)=>void) => { cb("{{ current_user.access_token }}"); },
				volume: 0.5,
			}
		);
		// FROM: https://developer.spotify.com/documentation/web-playback-sdk/reference#spotifyplayeraddlistener
		//  AND: https://developer.spotify.com/documentation/web-playback-sdk/reference#webplaybackplayer-object
		this.player.addListener("ready", this.ready.bind(this));
		this.player.addListener("not_ready", this.not_ready.bind(this));
		this.player.addListener("player_state_changed", this.player_state_changed.bind(this));

		this.player.connect();

		this.on_play = () => {};
		this.on_pause = () => {};
		this.timer = null;
	}


	ready(web_playback_player: WebPlaybackPlayer)
	{
		this.id = web_playback_player.device_id;
		this.is_ready = true;
		console.log(`Player ${this.id} is ready.`);
	}


	not_ready(web_playback_player: WebPlaybackPlayer)
	{
		this.is_ready = false;
		alert("Player has gone offline. Please try refreshing your browser.");
	}


	player_state_changed(web_playback_state: WebPlaybackState)
	{
		if(web_playback_state === null)
		{
			return;
		}

		let previously_playing = this.playing;
		this.playing = web_playback_state.paused ? null : web_playback_state.track_window.current_track.id;

		// Skip if redundant.
		if(previously_playing === this.playing)
		{
			return;
		}

		if(this.playing !== null)
		{
			if(this.timer !== null)
			{
				this.timer.start();
			}
			this.on_play()
		}
	}


	// —————————————————————————————————————————————————— API  —————————————————————————————————————————————————— //

	async pause()
	{
		await this.player.pause();
		this.on_pause();

		if(this.timer !== null)
		{
			this.timer.cancel();
			this.timer = null;
		}
	}


	async play_set_song(
		set_song_id: number,
		on_play=() => {},
		on_pause=() => {},
		start: number|null=null,
		duration: number|null=null
	)
	{
		await this.pause();

		this.on_play = on_play;
		this.on_pause = on_pause;
		if(duration !== null)
		{
			this.timer = new Timer(this, duration);
		}

		let response = await fetch(
			`/api/set_songs/${set_song_id}/play`,
			{
				method: `POST`,
				headers: {"Content-Type": "application/json"},
				body: JSON.stringify({player_id: this.id, start})
			}
		);

		if(response.status != 204)
		{
			throw new Error(`Unexpected ${response.status} Error: ${await response.text()}`);
		}
	}


	async play_song(id: number, on_play=() => {}, on_pause=() => {})
	{
		await this.pause();

		this.on_play = on_play;
		this.on_pause = on_pause;

		let response = await fetch(
			`/api/songs/${id}/play`,
			{
				method: `POST`,
				headers: {"Content-Type": "application/json"},
				body: JSON.stringify({player_id: this.id})
			}
		);

		if(response.status != 204)
		{
			throw new Error(`Unexpected ${response.status} Error: ${await response.text()}`);
		}
	}
}


class Timer
{
	player: Player;
	duration: number
	timeout: ReturnType<typeof setTimeout>|null;


	constructor(player: Player, duration: number)
	{
		this.player = player;
		this.duration = duration;

		this.timeout = null;
	}


	start()
	{
		if(this.timeout !== null)
		{
			return alert("Timer already running");
		}

		// FROM: https://www.w3schools.com/jsref/met_win_settimeout.asp
		this.timeout = setTimeout(this.on_timeout.bind(this), this.duration);
	}


	cancel()
	{
		if(this.timeout !== null)
		{
			// FROM: https://www.w3schools.com/jsref/met_win_cleartimeout.asp
			clearTimeout(this.timeout);
		}
	}


	on_timeout()
	{
		this.player.pause();
		this.timeout = null;
	}
}


function onSpotifyWebPlaybackSDKReady()
{
	PLAYER = new Player();
}

window.onSpotifyWebPlaybackSDKReady = onSpotifyWebPlaybackSDKReady;
