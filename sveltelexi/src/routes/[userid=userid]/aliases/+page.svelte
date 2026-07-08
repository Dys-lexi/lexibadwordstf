<script lang="ts">
	import type { Aliases } from '$lib/morestuff/types';

	import { page } from '$app/state';
	import Profile from '$lib/morestuff/profile.svelte';
	import '../Page.css';
	import './Page.css';
	import Hoverprofile from '$lib/morestuff/hoverprofile.svelte';
	import Miniprofile from '$lib/morestuff/miniprofile.svelte';
	import type { PageProps } from './$types';
	import { getaliases } from '$lib/remote/data.remote';
	let { params }: PageProps = $props();
	const aliases = $derived(getaliases(params.userid));
</script>

<div class="nonoresultsholder">
	<Profile steam64={params.userid} />
	{#await aliases then { aliases }}
		{#each aliases as alias, index (index)}
			<div class="nonowordbox">
			<div class="dateholder">	<a class="nonowordtimestamp" href={`https://logs.tf/${alias.firstlog}`}>
					<span class="loglink underlineme" >first seen </span> <span style = "color:#eeeeee" class="nonowordmessage">{new Date(alias.firstseen * 1000).toLocaleDateString()} </span><span class="nonowordname" >{new Date(alias.firstseen * 1000).toLocaleTimeString()}{' '}</span> 
				</a>
				<a class="nonowordtimestamp" href={`https://logs.tf/${alias.lastlog}`}>
				<span class="loglink underlineme" >	last seen </span><span  style = "color:#eeeeee"  class="nonowordmessage">{new Date(alias.lastseen * 1000).toLocaleDateString()} </span><span class="nonowordname" >{new Date(alias.lastseen * 1000).toLocaleTimeString()}{' '}</span> 
				</a></div>
				{alias.name}
			</div>
		{/each}
	{/await}
</div>
