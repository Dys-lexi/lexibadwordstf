<script lang="ts">
	import { page } from '$app/state';
	import Profile from '$lib/morestuff/profile.svelte';
	import Miniprofile from '$lib/morestuff/miniprofile.svelte';
	import { playedwithdetails, nonowords } from '$lib/remote/data.remote';
	import { onMount } from 'svelte';
	// import {replaceState} from "$app/navigation"
	// onMount(() => {
	// 	if (page.url.searchParams.get('asyncload') === '1') {
	// 		const url = new URL(page.url);
	// 		url.searchParams.delete('asyncload');
	// 		replaceState( '', url.toString());
	// 	}
	// });
	import './Page.css';
	import { getsteamurl } from '$lib/morestuff/config';
	let { data } = $props();
	let { personresults, statuscode } = $derived(data);
</script>

{#if statuscode == 200}
	<div class="nonoresultsholder">
		<Profile steam64={personresults.steam64} profiledefault={personresults} />

		<!-- <div class="playedwithperson playedwithpersonpersonal">
							
								<img
									class="playedwithphoto"
									src={personresults.avatarurl}
									alt="avatar"
								/>
								<div class = "playedwithname" >Plays With</div>
							</div> -->

		<div class="externalwebsiteholder">
			<a
				class="externalwebsite loglink"
				href={`/${personresults.steam64}/wordcloud`}
				target="_blank"
				>Wordcloud <img
					src={`https://avatars.fastly.steamstatic.com/${personresults.avatar}_full.jpg`}
					class="bigblurext"
					alt=""
				/></a
			>
			<a
				class="externalwebsite loglink"
				href={`https://steamcommunity.com/profiles/${personresults.steam64}`}
				target="_blank">Steam</a
			>
			<a
				class="externalwebsite loglink"
				href={`https://logs.tf/profile/${personresults.steam64}`}
				target="_blank">Logs.tf</a
			>
			<a
				class="externalwebsite loglink"
				href={`https://etf2l.org/search/${personresults.steam64}/`}
				target="_blank">ETF2L</a
			>
			<a
				class="externalwebsite loglink"
				href={`https://tf2center.com/profile/${personresults.steam64}/`}
				target="_blank">TF2Center</a
			>
			<a
				class="externalwebsite loglink"
				href={`https://ozfortress.com/users/steam_id/${personresults.steam64}/`}
				target="_blank">OZFortress</a
			>
			<a
				class="externalwebsite loglink"
				href={`https://rgl.gg/Public/PlayerProfile?p=${personresults.steam64}/`}
				target="_blank">RGL</a
			>
		</div>
		{#await playedwithdetails({steam64: personresults.steam64, more: false})}
			<div>Loading playedwith data</div>
		{:then { playedwithdata }}
			{#if playedwithdata.playedwith.length}
				<div class="playedwithholderholder">
					<div class="playedwithinfo">
						<a class="nonowordtimestamp loglink" href={`/${personresults.steam64}/playedwith`}>
							{personresults.currentusername} has played with {playedwithdata.totalplayedwith} people
						</a>
					</div>
					<div class="playedwithholder">
						{#each playedwithdata.playedwith as data, index (index)}
							<Miniprofile {data} biggestplayedwith={playedwithdata.biggestplayedwith} />
						{/each}
					</div>
				</div>{/if}
		{:catch error}
			<h2>realy weird error loading data: {error.message}</h2>
		{/await}
		{#await nonowords(personresults.steam64)}
			<div>Loading Bad words</div>
		{:then { badwords }}
			<div class="nonowordsholder">
				{#if badwords.nonowords.length}
					<!-- {console.log( personresults.badwords,"PANTS")} -->
					{#each badwords.nonowords as badword, index (index)}
						<div class="nonowordbox">
							<a
								class="nonowordtimestamp loglink"
								target="_blank"
								href={`https://logs.tf/${badword.matchid}`}
							>
								log
							</a>
							<div class="nonowordtimestamp">
								{new Date(badword.timestamp * 1000).toLocaleDateString()}{' '}
								<div class="nonowordname">
									{new Date(badword.timestamp * 1000).toLocaleTimeString()}
								</div>
							</div>

							{' '}
							<div class="nonowordname">
								{badword.name}<span style="color: #eee">:</span>
							</div>
							{' '}
							<div class="nonowordmessage">
								{badword.message}
							</div>
						</div>
					{/each}
				{:else}
					<h2>No bad words found for {personresults.currentusername}</h2>
				{/if}
			</div>
		{:catch error}
			<h2>could not load bad words: {error.message}</h2>
		{/await}
	</div>
{:else if statuscode == 404}
	<h2>could not find user "{page.params.userid}"</h2>
{:else if statuscode == 429}
	<h2>the server is being rate limited by steam, don't search by vanity url atm :(</h2>
{:else}
	<h2>the server broke (or is down), sorry :(</h2>
{/if}

<svelte:head>
	<title>{statuscode === 200 ? personresults.currentusername : 'LexiSlurs'}</title>

	{#if statuscode === 200}
		<meta
			name="description"
			content={`${personresults.currentusername} has sent ${personresults.badwords || 'no'} bad words`}
		/>
		<meta
			property="og:description"
			content={`${personresults.currentusername} has sent ${personresults.badwords || 'no'} bad words`}
		/>
		<meta
			property="og:image"
			content={`${page.url.origin}/api/wordcloud/${personresults.steam64}`}
		/>
		<meta
			name="twitter:description"
			content={`${personresults.currentusername} has sent ${personresults.badwords || 'no'} bad words`}
		/>
		<meta
			name="twitter:image"
			content={`${page.url.origin}/api/wordcloud/${personresults.steam64}`}
		/>
	{:else if statuscode === 404}
		<meta name="description" content="User not found" />
		<meta property="og:description" content="User not found" />
		<meta property="og:image" content={`${page.url.origin}/logo.png`} />
		<meta name="twitter:description" content="User not found" />
		<meta name="twitter:image" content={`${page.url.origin}/logo.png`} />
	{:else}
		<meta name="description" content="Error finding information" />
		<meta property="og:description" content="Error finding information" />
		<meta property="og:image" content={`${page.url.origin}/logo.png`} />
		<meta name="twitter:description" content="Error finding information" />
		<meta name="twitter:image" content={`${page.url.origin}/logo.png`} />
	{/if}

	<meta property="og:type" content="website" />
	<meta property="og:url" content={getsteamurl(page.url.href, false)} />
	<meta property="og:title" content="LexiSlurs" />

	<!-- <meta property="og:image:width" content="184" />
	<meta property="og:image:height" content="184" /> -->

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="LexiSlurs" />
</svelte:head>
