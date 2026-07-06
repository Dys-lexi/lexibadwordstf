<script lang="ts">
	import type { Userdetails } from '$lib/morestuff/types';

	import { page } from '$app/state';
	import Profile from '$lib/morestuff/profile.svelte'
	import '../Page.css';
	import './Page.css';
	import Hoverprofile from '$lib/morestuff/hoverprofile.svelte'
	let { data } = $props();
	let { personresults, statuscode } = $derived(data);
</script>

{#if statuscode == 200}
	<div class="nonoresultsholder">

			<!-- {@render Profile(personresults.steam64)} -->
			<Profile steam64={personresults.steam64}/>
			<!-- <div class="playedwithperson playedwithpersonpersonal">
							
								<img
									class="playedwithphoto"
									src={personresults.avatarurl}
									alt="avatar"
								/>
								<div class = "playedwithname" >Plays With</div>
							</div> -->
	
		{#await personresults.playedwith}
			Loading playedwith data
		{:then playedwith}
			{#await personresults.biggestplayedwith then biggestplayedwith}
				{#await personresults.totalplayedwith then totalplayedwith}
					{#if playedwith.length}
						<div class="playedwithholderholder">
							<div class="playedwithinfo">
								<a class="nonowordtimestamp loglink" href={`/${personresults.steam64}`}>
									{personresults.currentusername} has played with {totalplayedwith} people
								</a>
							</div>
							<div class="playedwithholderbig playedwithholder">
								{#each playedwith as data, index (index)}
									<a class="playedwithpersonsamey" href={`/${data.steam64}`}>
									
										<div class=" playedwithperson">
										
											<div class="playedwithpercent playedwithbad"></div>
											<div
												class="playedwithpercent"
												style={`height: ${(data.commonmatches * 100) / biggestplayedwith}%`}
											></div>
											<img
												class="playedwithphoto"
												src={`https://avatars.fastly.steamstatic.com/${data.avatar}.jpg`}
												alt="avatar"
											/>

											<div class="goawayoverflow playedwithname">{data.currentusername}</div>
											
										</div>
											<Hoverprofile steam64={data.steam64} profiledefault={data}/>
									</a>
								
								{/each}
							</div>
						</div>
					{/if}
				{/await}
			{/await}
		{:catch error}
			<h2>realy weird error loading data: {error.message}</h2>
		{/await}
	</div>
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
