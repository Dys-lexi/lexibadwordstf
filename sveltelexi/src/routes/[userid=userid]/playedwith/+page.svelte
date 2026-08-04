<script lang="ts">
	import { page } from '$app/state';
	import Profile from '$lib/morestuff/profile.svelte';
	import Playedwith from '$lib/morestuff/playedwith.svelte';
	import '../Page.css';
	import './Page.css';

	let { data } = $props();
	let { personresults, statuscode } = $derived(await data.profile);
</script>

{#if statuscode == 200}
	<div class="nonoresultsholder">
		<!-- {@render Profile(personresults.steam64)} -->
		<Profile steam64={personresults.steam64} profiledefault={personresults} />
		<!-- <div class="playedwithperson playedwithpersonpersonal">
							
								<img
									class="playedwithphoto"
									src={personresults.avatarurl}
									alt="avatar"
								/>
								<div class = "playedwithname" >Plays With</div>
							</div> -->
		<div class="outlinethingy">
		<Playedwith personresults={personresults} more={true} />
		</div>
	</div>
{:else}
	<h1 style="color: red">
		Something went wrong :( {statuscode}
	</h1>
{/if}

<svelte:head>
	<title>{statuscode === 200 ? personresults.currentusername : 'LexiSlurs'}</title>

	{#if statuscode === 200}
		<meta name="description" content={`playedwithdata for ${personresults.currentusername}`} />
		<meta
			property="og:description"
			content={`playedwithdata for ${personresults.currentusername}`}
		/>
		<meta property="og:image" content={`/${personresults.steam64}/wordcloud`} />
		<meta
			name="twitter:description"
			content={`playedwithdata for ${personresults.currentusername}`}
		/>
		<meta name="twitter:image" content={`/${personresults.steam64}/wordcloud`} />
	{:else if statuscode === 404}
		<meta name="description" content="User not found" />
		<meta property="og:description" content="User not found" />
		<meta property="og:image" content={`/${personresults.steam64}/wordcloud`} />
		<meta name="twitter:description" content="User not found" />
		<meta name="twitter:image" content={`/${personresults.steam64}/wordcloud`} />
	{:else}
		<meta name="description" content="Error finding information" />
		<meta property="og:description" content="Error finding information" />
		<meta property="og:image" content={`/${personresults.steam64}/wordcloud`} />
		<meta name="twitter:description" content="Error finding information" />
		<meta name="twitter:image" content={`/${personresults.steam64}/wordcloud`} />
	{/if}

	<meta property="og:type" content="website" />
	<meta property="og:url" content={page.url.href} />
	<meta property="og:title" content="LexiSlurs" />

	<!-- <meta property="og:image:width" content="184" />
	<meta property="og:image:height" content="184" /> -->

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="LexiSlurs" />
</svelte:head>
