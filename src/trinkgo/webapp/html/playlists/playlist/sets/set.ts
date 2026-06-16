
async function get_start_and_play_song(button: HTMLButtonElement, set_song_id: number): Promise<void>
{
	button.disabled = true;

	let on_play = () =>
	{
		button.innerHTML = "Pause";
		button.onclick = async () => await (PLAYER as Player).pause();
		button.disabled = false;
	}

	let on_pause = () =>
	{
		button.innerHTML = "Play";
		button.onclick = async () => get_start_and_play_song(button, set_song_id);
	}

	let start = parseInt((document.getElementById(`set_song_start-${set_song_id}-input`) as HTMLInputElement).value);
	let duration = parseInt(
		(document.getElementById(`set_song_duration-${set_song_id}-input`) as HTMLInputElement).value
	);
	try
	{
		await (PLAYER as Player).play_set_song(set_song_id, on_play, on_pause, start, duration);
	}
	catch(error)
	{
		alert(error);
	}
}


async function update_set_song(set_song_id: number): Promise<void>
{
	let playlist_id = window.location.pathname.split("/")[2];

	let label = (document.getElementById(`set_song_label-${set_song_id}-input`) as HTMLInputElement).value;
	let start = (document.getElementById(`set_song_start-${set_song_id}-input`) as HTMLInputElement).value;
	let duration = (document.getElementById(`set_song_duration-${set_song_id}-input`) as HTMLInputElement).value;

	try
	{
		let response = await fetch(
			`/api/set_songs/${set_song_id}/update`,
			{
				method: `POST`,
				headers: {"Content-Type": "application/json"},
				body: JSON.stringify({playlist_id, label, start, duration})
			}
		);
		if(response.status != 204)
		{
			return alert(`${response.status}`+response.body);
		}
	}
	catch(error)
	{
		console.error(error);
		alert(error);
	}
}


function update_duration(set_song_id: number, song_length: number): void
{
	const start_input = document.getElementById(`set_song_start-${set_song_id}-input`) as HTMLInputElement;
	const duration_input = document.getElementById(`set_song_duration-${set_song_id}-input`) as HTMLInputElement;

	if(parseInt(start_input.value) < 0)
	{
		start_input.value = (0).toString();
	}
	if(song_length < parseInt(start_input.value))
	{
		start_input.value = (song_length).toString();
	}

	if(parseInt(start_input.value) + parseInt(duration_input.value) > song_length)
	{
		duration_input.value = (song_length - parseInt(start_input.value)).toString();
	}
}