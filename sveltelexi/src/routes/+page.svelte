<script lang="ts">
	import './Page.css';
	// import Search from '$lib/morestuff/Search.svelte';
	import { page } from '$app/state';
	import faviconUrl from '$lib/images/logosmall.png';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	const { stats, statuscode } = $derived(data);

	const prettynames: Record<string, string> = {
		uniquepeople: 'Unique Players',
		totalmessages: 'Total Messages',
		totalmatches: 'Logs Searched',
		badmessages: 'Flagged messages',
		flaggedplayers: 'Flagged Players'
	};

	function getstatprettyname(name: string): string {
		return prettynames[name] || name;
	}
</script>

<div class="flexbox" style="gap: 30px; margin-top: 30px">

	<div class="statsholder">
		{#if statuscode == 200}
			{#each Object.entries(stats) as [stat, val]}
				<div class="stat">
					<div class="statsname"> {getstatprettyname(stat)}: </div>
					<div class="statsstat"> {val.toLocaleString()} </div>
				</div>
			{/each}
		{:else}
			<div class="stat" style="color: red">
				Backend is probably down :( {statuscode}
			</div>
		{/if}
	</div>
	<div class="whomadethisshowthingy">
		Made by
		<u style="text-decoration-color: rgba(255,180,200,0.8)">
			<a
				href="https://discord.gg/uR7KwhedfK"
				target="_blank"
				rel="noopener noreferrer"
				style="color: rgba(255,180,200,1)"
			>
				@dyslexi
			</a>
		</u>
		on discord
	</div>
</div>

      <svelte:head>
	<title>LexiSlurs</title>
  <link rel="icon" href={faviconUrl} />
  <meta name="description" content={  `Tracking bad words in ${stats.totalmessages.toLocaleString()} messages`} />

  <meta property="og:type" content="website" />
  <meta property="og:url" content={page.url.href} />
  <meta property="og:title" content="LexiSlurs" />
  <meta property="og:description" content={  `Tracking bad words in ${stats.totalmessages.toLocaleString()} messages`} />
  <meta property="og:image" content={`${page.url.origin}/logo.png`} />
  <meta property="og:image:width" content="960" />
  <meta property="og:image:height" content="960" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="LexiSlurs" />
  <meta name="twitter:description" content={  `Tracking bad words in ${stats.totalmessages.toLocaleString()} messages`} />
  <meta name="twitter:image" content={`${page.url.origin}/logo.png`} />
</svelte:head>