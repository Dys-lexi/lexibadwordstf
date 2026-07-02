<script lang="ts">
	import type { Userdetails } from '../types';
	import { page } from '$app/state';
	import '../Page.css';
	import './Page.css';
	let { data } = $props();
	let { personresults, statuscode } = $derived(data);
</script>

{#if statuscode == 200}
	<div class="nonoresultsholder">
	<div class="expandednameholder">
			<a class="nameholderbad" href={`https://steamcommunity.com/profiles/${personresults.steam64}`} target="_blank">
				<div class="nonowordavatarholder">
					<img src={personresults.frame} class="avatarholder" alt="" />
					<img src={`https://avatars.fastly.steamstatic.com/${personresults.avatar}_full.jpg`} class="nonowordavatar" alt="avatar" />
				</div>
				<div>
					{' '}
					<div class="nonowordcurrentusername">
						{' '}
						{personresults.currentusername}
					</div>
					<div class = "badwordcounter">
					I'll put cool data here soon</div>
				</div>
			</a>
			
			<!-- <div class="playedwithperson playedwithpersonpersonal">
							
								<img
									class="playedwithphoto"
									src={personresults.avatarurl}
									alt="avatar"
								/>
								<div class = "playedwithname" >Plays With</div>
							</div> -->
			
		</div>
			{#await personresults.playedwith}
					Loading playedwith data
				{:then playedwith}
				{#await personresults.biggestplayedwith then biggestplayedwith}
				{#await personresults.totalplayedwith then totalplayedwith}
				{#if playedwith.length}
				<div class = "playedwithholderholder">
				<div class="playedwithinfo">
					<a class="loglink" href={`/${personresults.steam64}`}>  {personresults.currentusername} has played with {totalplayedwith} people </a>
					

				</div>
				<div class="playedwithholderbig playedwithholder">
					{#each playedwith as data, index (index)}
						<a class = "playedwithpersonsamey" href={`/${data.steam64}`}>
							<div class=" playedwithperson">
										<div class="playedwithpercent playedwithbad" ></div>
								<div class="playedwithpercent" style={`height: ${(data.commonmatches*100)/biggestplayedwith}%`}></div>
								<img
									class="playedwithphoto"
									src={`https://avatars.fastly.steamstatic.com/${data.avatar}.jpg`}
									alt="avatar"
								/>

								<div class = "goawayoverflow playedwithname" >{data.currentname}</div>
								
							</div>
						</a>
					{/each}
					</div></div>
			
				
					
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
		<meta
			name="description"
			content={`playedwithdata for ${personresults.currentusername}`}
		/>
		<meta
			property="og:description"
			content={`playedwithdata for ${personresults.currentusername}`}
		/>
		<meta property="og:image" content={personresults.avatar} />
		<meta
			name="twitter:description"
			content={`playedwithdata for ${personresults.currentusername}`}
		/>
		<meta name="twitter:image" content={personresults.avatar} />
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
	<meta property="og:url" content={page.url.href} />
	<meta property="og:title" content="LexiSlurs" />

	<meta property="og:image:width" content="184" />
	<meta property="og:image:height" content="184" />

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="LexiSlurs" />
</svelte:head>
