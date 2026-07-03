<script lang="ts">
	import type { Userdetails } from './types';
	import { page } from '$app/state';
	import './Page.css';
	let { data } = $props();
	let { personresults, statuscode } = $derived(data);
</script>

{#if statuscode == 200}
	<div class="nonoresultsholder">
		<div class="expandednameholder">
			<a class="nameholderbad" href={`/${personresults.steam64}`} >
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
					{#if personresults.badwords == 1}
						<div class="badwordcounter">1 bad word</div>
					{:else if personresults.badwords}
						<div class="badwordcounter">
							{personresults.badwords} bad words
						</div>
					{/if}
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
		<div class="externalwebsiteholder">
			<a class = "externalwebsite loglink" href = {`https://steamcommunity.com/profiles/${personresults.steam64}`} target="_blank">Steam</a>
			<a class = "externalwebsite loglink" href = {`https://etf2l.org/search/${personresults.steam64}/`} target="_blank">ETF2L</a>
			<a class = "externalwebsite loglink" href = {`https://tf2center.com/profile/${personresults.steam64}/`} target="_blank">TF2Center</a>
			<a class = "externalwebsite loglink" href = {`https://ozfortress.com/users/steam_id/${personresults.steam64}/`} target="_blank">OZFortress</a>
			<a class = "externalwebsite loglink" href = {`https://rgl.gg/Public/PlayerProfile?p=${personresults.steam64}/`} target="_blank">RGL</a>

		</div>
			{#await personresults.playedwith}
					<div>Loading playedwith data</div>
				{:then playedwith}
				{#await personresults.biggestplayedwith then biggestplayedwith}
				{#await personresults.totalplayedwith then totalplayedwith}
				{#if playedwith.length}
				<div class = "playedwithholderholder">
				<div class="playedwithinfo">
					<a class="nonowordtimestamp loglink" href={`/${personresults.steam64}/playedwith`}>  {personresults.currentusername} has played with {totalplayedwith} people </a>
					

				</div>
				<div class="playedwithholder">
					{#each playedwith as data, index (index)}
						<a href={`/${data.steam64}`}>
							<div class="playedwithperson">
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
					</div></div>{/if}
					{/await}
					{/await}
				{:catch error}
					<h2>realy weird error loading data: {error.message}</h2>
				{/await}
		{#await personresults.nonowords}
		<div>Loading Bad words</div>
		{:then nonowords}
		<div class="nonowordsholder">
			{#if nonowords != null && personresults.badwords}
			<!-- {console.log( personresults.badwords,"PANTS")} -->
				{#each nonowords as badword, index (index)}
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
		<meta property="og:image" content={`${page.url.origin}/api/wordcloud/${personresults.steam64}`} />
		<meta
			name="twitter:description"
			content={`${personresults.currentusername} has sent ${personresults.badwords || 'no'} bad words`}
		/>
		<meta name="twitter:image" content={`${page.url.origin}/api/wordcloud/${personresults.steam64}`} />
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

	<!-- <meta property="og:image:width" content="184" />
	<meta property="og:image:height" content="184" /> -->

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="LexiSlurs" />
</svelte:head>
