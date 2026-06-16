
const PLAY_NEXT_RANDOM: HTMLButtonElement = document.getElementById("play_next_random-button") as HTMLButtonElement;
const PLAYED_SONGS_TABLE: HTMLTableElement = document.getElementById("played_songs-tbody") as HTMLTableElement;


async function play_next(set_song_id: number|null=null): Promise<void>
{
	PLAY_NEXT_RANDOM.disabled = true;

	try
	{
		let response = await fetch(
			`/api/rounds/{{ round.id }}/played_set_songs/new`,
			{
				method: `POST`,
				headers: {"Content-Type": "application/json"},
				body: JSON.stringify({set_song_id})
			}
		);

		if(response.status != 200)
		{
			throw new Error(`Unexpected ${response.status} Error: ${await response.text()}`);
		}
		let response_json = await response.json();

		let created_element = document.createElement("tbody");
		created_element.innerHTML = response_json.html;
		PLAYED_SONGS_TABLE.prepend(created_element.firstChild as Node);

		document.getElementById(`unplayed_song_${response_json.set_song_id}-tr`)!.remove();

		let play_button: HTMLButtonElement = document.getElementById(
			`played_set_song_${response_json.set_song_id}-button`
		) as HTMLButtonElement;
		let on_play = async () =>
		{
			// let play_button: HTMLButtonElement = document.getElementById(`played_set_song_${response_json.set_song_id}-button`);
			play_button.innerHTML = "Pause";
			play_button.onclick = async () => await (PLAYER as Player).pause();
		}
		let on_pause = async () =>
		{
			// let play_button: HTMLButtonElement = document.getElementById(`played_set_song_${response_json.set_song_id}-button`);
			play_button.innerHTML = "Play Again";
			play_button.onclick = async () =>
			{
				await play_again(
					play_button,
					response_json.set_song_id,
					null,
					response_json.duration
				);
			};
		}
		await (PLAYER as Player).play_set_song(
			response_json.set_song_id,
			on_play,
			on_pause,
			null,
			response_json.duration
		);
	}
	catch(error)
	{
		console.error(error);
		alert(error);
	}

	PLAY_NEXT_RANDOM.disabled = false;
}


async function play_again(
	button: HTMLButtonElement,
	set_song_id: number,
	start: number|null,
	duration: number
): Promise<void>
{
	button.disabled = true;

	try
	{
		let on_play = async () =>
		{
			button.innerHTML = "Pause";
			button.onclick = async () => await (PLAYER as Player).pause();
			button.disabled = false;
		}
		let on_pause = async () =>
		{
			button.innerHTML = "Play Again";
			button.onclick = async () => await play_again(button, set_song_id, start, duration);
		}
		await (PLAYER as Player).play_set_song(set_song_id, on_play, on_pause, start, duration);
	}
	catch(error)
	{
		alert(error);
	}
}