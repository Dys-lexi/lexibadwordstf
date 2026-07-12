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
		let { data,params } = $props();
	let { personresults, statuscode } = $derived(await data.profile);
	const aliases = $derived(getaliases(params.userid));
</script>
{#if statuscode == 200}
<div class="nonoresultsholder">
	<Profile steam64={params.userid} profiledefault={personresults} />
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
{:else}
<h1  style="color: red">
				Something went wrong :( {statuscode}
			</h1>
{/if}

<svelte:head>
	<title>{statuscode === 200 ? personresults.currentusername : 'LexiSlurs'}</title>

	{#if statuscode === 200}
		<meta name="description" content={`Aliases for ${personresults.currentusername}`} />
		<meta
			property="og:description"
			content={`Aliases for ${personresults.currentusername}`}
		/>
		<meta property="og:image" content={`${page.url.origin}/api/wordcloud/${personresults.steam64}`} />
		<meta
			name="twitter:description"
			content={`Aliases for ${personresults.currentusername}`}
		/>
		<meta name="twitter:image" content={`${page.url.origin}/api/wordcloud/${personresults.steam64}`} />
	{:else if statuscode === 404}
		<meta name="description" content="User not found" />
		<meta property="og:description" content="User not found" />
		<meta property="og:image" content={`${page.url.origin}/api/wordcloud/${personresults.steam64}`} />
		<meta name="twitter:description" content="User not found" />
		<meta name="twitter:image" content={`${page.url.origin}/api/wordcloud/${personresults.steam64}`} />
	{:else}
		<meta name="description" content="Error finding information" />
		<meta property="og:description" content="Error finding information" />
		<meta property="og:image" content={`${page.url.origin}/api/wordcloud/${personresults.steam64}`} />
		<meta name="twitter:description" content="Error finding information" />
		<meta name="twitter:image" content={`${page.url.origin}/api/wordcloud/${personresults.steam64}`} />
	{/if}

	<meta property="og:type" content="website" />
	<meta property="og:url" content={page.url.href} />
	<meta property="og:title" content="LexiSlurs" />

	<!-- <meta property="og:image:width" content="184" />
	<meta property="og:image:height" content="184" /> -->

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="LexiSlurs" />
</svelte:head>
