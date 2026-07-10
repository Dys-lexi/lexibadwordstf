<script lang="ts">
	import type { Userdetails } from '$lib/morestuff/types';

	import { page } from '$app/state';
	import Profile from '$lib/morestuff/profile.svelte'
	import '../Page.css';
	import './Page.css';

	import Miniprofile from '$lib/morestuff/miniprofile.svelte'
	import { playedwithdetails } from '$lib/remote/data.remote';
	let { data } = $props();
	let { personresults, statuscode } = $derived(data);
</script>

{#if statuscode == 200}
	<div class="nonoresultsholder">

			<!-- {@render Profile(personresults.steam64)} -->
			<Profile steam64={personresults.steam64} profiledefault={personresults}/>
			<!-- <div class="playedwithperson playedwithpersonpersonal">
							
								<img
									class="playedwithphoto"
									src={personresults.avatarurl}
									alt="avatar"
								/>
								<div class = "playedwithname" >Plays With</div>
							</div> -->
	
		{#await playedwithdetails({steam64: personresults.steam64, more: true})}
			Loading playedwith data
		{:then {playedwithdata}}

					{#if playedwithdata.playedwith.length}
						<div class="playedwithholderholder">
							<div class="playedwithinfo">
								<a class="nonowordtimestamp loglink" href={`/${personresults.steam64}`}>
									{personresults.currentusername} has played with {playedwithdata.totalplayedwith} people
								</a>
							</div>
							<div class="playedwithholderbig playedwithholder">
								{#each playedwithdata.playedwith as data, index (index)}
								<Miniprofile data={data} biggestplayedwith={playedwithdata.biggestplayedwith}/>
								
								{/each}
							</div>
						</div>
					{/if}
		

		{:catch error}
			<h2>realy weird error loading data: {error.message}</h2>
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
		<meta name="description" content={`playedwithdata for ${personresults.currentusername}`} />
		<meta
			property="og:description"
			content={`playedwithdata for ${personresults.currentusername}`}
		/>
		<meta property="og:image" content={`${page.url.origin}/api/wordcloud/${personresults.steam64}`} />
		<meta
			name="twitter:description"
			content={`playedwithdata for ${personresults.currentusername}`}
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
