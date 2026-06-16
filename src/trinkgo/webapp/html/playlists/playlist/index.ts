
async function set_button_and_play_song(button: HTMLButtonElement, id: number): Promise<void>
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
		button.onclick = async () => set_button_and_play_song(button, id);
	}

	try
	{
		await (PLAYER as Player).play_song(id, on_play, on_pause);
	}
	catch(error)
	{
		alert(error);
	}
}
