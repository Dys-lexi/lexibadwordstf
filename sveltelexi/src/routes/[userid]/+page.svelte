<script lang="ts">
	import type { Userdetails } from './types';
	import { page } from '$app/state';
	import './Page.css';


	let { data } = $props();
	let { personresults, statuscode } = $derived(data);
</script>


{#await personresults}
	Loading comments...
{:then comments}
{#if statuscode == 200}
	<div class="nonoresultsholder">
		<a class="nameholderbad" href={personresults.steamprofile} target="_blank">
			<div class="nonowordavatarholder">
				<img src={personresults.frame} class="avatarholder" alt = ""/>
				<img src={personresults.avatarurl} class="nonowordavatar" alt = "avatar"/>
			</div>
			<div>
				{' '}
				<div class="nonowordcurrentusername ">
					{' '}
					{personresults.currentusername}
				</div>
				{#if personresults.nonowords.length == 1}
					<div class="badwordcounter">1 bad word</div>
				{:else if personresults.nonowords.length}
					<div class="badwordcounter">
						{personresults.nonowords.length} bad words
					</div>
				{/if}
			</div>
		</a>
		<div class="nonowordsholder">
			{#if personresults.nonowords != null && personresults.nonowords.length}
				{#each personresults.nonowords as badword, index (index)}
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
						</div>{' '} <div class="nonowordmessage">
							{badword.message}
						</div>
					</div>
				{/each}
			{:else}
				<h2>No bad words found for {personresults.currentusername}</h2>
			{/if}
		</div>
	</div>
{:else if statuscode == 404}
	<h2>could not find user "{page.params.userid}"</h2>
{:else if statuscode == 429}
	<h2>
		the server is being rate limited by steam, don't search by vanity url
		atm :(
	</h2>
{:else}
	<h2>the server broke (or is down), sorry :( </h2>
{/if}

{:catch error}
	<h2>realy weird error loading data: {error.message}</h2>
{/await}


<svelte:head>
	<title>{personresults.currentusername}</title>

    {#if statuscode == 200}
  <meta name="description" content={`${personresults.currentusername} has ${personresults.nonowords.length || "No"} Bad words sent`} />
	{/if}
  <meta property="og:type" content="website" />
  {#if statuscode == 200}
  <meta property="og:url" content={personresults.avatarurl} />
  {/if}
  <meta property="og:title" content="LexiSlurs" />
   {#if statuscode == 200}
  <meta property="og:description" content={`${personresults.currentusername} has ${personresults.nonowords.length || "No"} Bad words sent`} />

  <meta property="og:image" content={personresults.avatarurl} />
  {/if}
  <meta property="og:image:width" content="184" />
  <meta property="og:image:height" content="184" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="LexiSlurs" />
   {#if statuscode == 200}
  <meta name="twitter:description" content={`${personresults.currentusername} has ${personresults.nonowords.length || "No"} Bad words sent`} />
  <meta name="twitter:image" content={personresults.avatarurl} />
  {/if}
</svelte:head>
