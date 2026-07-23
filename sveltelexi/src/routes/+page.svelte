<script lang="ts">
	import './Page.css';
	// import Search from '$lib/morestuff/Search.svelte';
	import { page } from '$app/state';
	import faviconUrl from '$lib/images/logosmall.png';
	import type { PageData } from './$types';
	const utcDate = new Date('2026-07-23T08:00:00Z');
	import { getwordclouddaily } from '$lib/remote/data.remote';
	import Search from '$lib/morestuff/Search.svelte';
	const localTime = utcDate.toLocaleString()
	// 	undefined, {
	// 	hour: 'numeric',
	// 	minute: '2-digit',

	// 	day: 'numeric'
	// });

	let blurradius = $state(23)

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

<Search
	classNameform="bigsearchform"
	classNameinput="bigsearchinput"
	classnamebutton="bigsearchbutton"
/>

<div class="flexbox" style="gap: 30px; margin-top: 30px">
	<div class="statsholder">
		{#if statuscode == 200}
			{#each Object.entries(stats) as [stat, val]}
			{#if prettynames[stat]}
				<div class="stat">
					<div class="statsname">{getstatprettyname(stat)}:</div>
					<div class="statsstat">{val.toLocaleString()}</div>
				</div>
			{/if}
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
	{#if stats.badrecentmessages}
	<div class = "flexbox worddailybox"  role="presentation" onmouseenter={() => {blurradius = 0}}  onmouseleave={() => {blurradius = 23}}>
		<div class="stat"> <div class="statsname">Bad words sent yesterday: </div><div class="statsstat"> {stats.badrecentmessages.toLocaleString() }</div> </div>
	{#await getwordclouddaily("big")}
	<img style = {`filter: blur(${blurradius}px)`} src={(await getwordclouddaily("smol")).profile} class="wordcloudimage" alt="wordcloud" />
	{:then {profile}}
		<img src={profile} title={`last updated at ${localTime} this morning`} class="wordcloudimage" alt="wordcloud" style = {`filter: blur(${blurradius}px)`}/>
	{/await}
	</div>
	{/if}
	<!-- <div class="whomadethisshowthingy">
		Support on
		<u style="text-decoration-color: rgba(255,180,200,0.8)">
			<a
				href="https://ko-fi.com/dyslexi"
				target="_blank"
				rel="noopener noreferrer"
				style="color: rgba(255,150,150,1)"
			>
				Ko-fi
			</a>
		</u>
	</div> -->
</div>
<svelte:head>
	{#if statuscode == 200}
		<meta
			name="description"
			content={`Tracking bad words in ${stats.totalmessages.toLocaleString()} messages`}
		/>
	{:else}
		<meta name="description" content="Find bad words and maybe slurs sent by people in TF2" />
	{/if}

	<meta property="og:type" content="website" />
	<meta property="og:url" content={page.url.href} />
	<meta property="og:title" content="LexiSlurs" />

	{#if statuscode == 200}
		<meta
			property="og:description"
			content={`Tracking bad words in ${stats.totalmessages.toLocaleString()} messages`}
		/>
	{:else}
		<meta
			property="og:description"
			content="Find bad words and maybe slurs sent by people in TF2"
		/>
	{/if}

	<meta property="og:image" content={`${page.url.origin}/logo.png`} />
	<meta property="og:image:width" content="960" />
	<meta property="og:image:height" content="960" />

	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content="LexiSlurs" />

	{#if statuscode == 200}
		<meta
			name="twitter:description"
			content={`Tracking bad words in ${stats.totalmessages.toLocaleString()} messages`}
		/>
	{:else}
		<meta
			name="twitter:description"
			content="Find bad words and maybe slurs sent by people in TF2"
		/>
	{/if}

	<meta name="twitter:image" content={`${page.url.origin}/logo.png`} />
</svelte:head>
