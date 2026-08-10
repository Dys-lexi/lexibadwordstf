<script lang="ts">
	import './profile.css';
	import type { Userdetails, Badmessage } from '$lib/morestuff/types';

	import { logtimeline } from '$lib/remote/data.remote';
	import Hover from '$lib/morestuff/followingmouse.svelte';
	let { badwords, personresults }: { badwords: Array<Badmessage>; personresults: Userdetails } =
		$props();
		let leaveTimer: ReturnType<typeof setTimeout> | undefined;
	const logtimelinedetails = $derived(
		personresults.steam64 == '00000000000000000' ? null : logtimeline(personresults.steam64)
	);
	let logtimestamps = $state<Array<number> | null>(null);

	$effect(() => {
		const request = logtimelinedetails;
		let cancelled = false;

		logtimestamps = null;
		if (request === null) return;

		Promise.resolve(request)
			.then((timestamps) => {
				if (!cancelled) logtimestamps = timestamps;
			})
			.catch(() => {
				if (!cancelled) logtimestamps = [];
			});

		return () => {
			cancelled = true;
		};
	});

	const { binnings, barheight, logbarheight } = $derived.by(() => {
		const binnings: Record<number, { badmessages: Badmessage[]; logmessages: number | null }> = {};
		let barheight = 10;
		let logbarheight = 10;
		const logsLoaded = logtimestamps !== null;

		for (const badword of badwords) {
			const year: number = new Date(badword.timestamp * 1000).getFullYear();

			(binnings[year] ??= { badmessages: [], logmessages: logsLoaded ? 0 : null }).badmessages.push(
				badword
			);
			barheight = Math.max(barheight, binnings[year].badmessages.length);
		}

		if (logtimestamps !== null) {
			for (const timestamp of logtimestamps) {
				const year = new Date(timestamp * 1000).getFullYear();
				const bin = (binnings[year] ??= { badmessages: [], logmessages: 0 });
				bin.logmessages = (bin.logmessages ?? 0) + 1;
				logbarheight = Math.max(logbarheight, bin.logmessages);
			}
		}

		const populatedYears = Object.keys(binnings).map(Number);
		if (populatedYears.length > 0) {
			const firstYear = Math.min(...populatedYears);
			const lastYear = Math.max(new Date().getFullYear(), ...populatedYears);
			for (let year = firstYear; year <= lastYear; year++) {
				binnings[year] ??= { badmessages: [], logmessages: logsLoaded ? 0 : null };
			}
		}

		return { binnings, barheight, logbarheight };
	});

	let renderhover = $state(null as number | null);

	// let profilestuff: Userdetails}
	// const coords =  mousePosition()
</script>

<div class="timelineholder">
	<div class="barlabelholder">
		<span class="barlabelsizer" aria-hidden="true">{barheight}</span>
		<div class="barlabelplot">
			{@render barlabel(Math.floor(barheight * 0.34), barheight)}
			{@render barlabel(Math.floor(barheight * 0.67), barheight)}
			{@render barlabel(Math.floor(barheight), barheight)}
		</div>
	</div>
	<div class="timelinetimelineholder">
		{#each Object.entries(binnings).sort(([a], [b]) => Number(a) - Number(b)) as [year, { badmessages: stuff, logmessages }], index (year)}
			<div
				class="yearholder"
				role="presentation"
				onmouseenter={() => {
					    if (leaveTimer) clearTimeout(leaveTimer);
					renderhover = index;
				}}
				onmouseleave={() => {
				leaveTimer = 	setTimeout(() => {
                       renderhover = null;
                }, 100);
					
				}}
			>
			
				<div class="barholder">
					<div
						class="bar"
						style={`height: ${(stuff.length * 100) / barheight}%; background-color: rgb(${(stuff.length * 150) / barheight + 100},50,50)`}
					></div>
					<div
						class="bar"
						style={`height: ${((logmessages ?? 1) * 100) / logbarheight}%; background-color: rgb(50,50,${logmessages ? (logmessages * 150) / logbarheight + 100 : 70})`}
					></div>
				</div>
				{Number(year) % 100}
			</div>
			{#if renderhover == index}
				<Hover>
					<span class="badwordhovercount">
						{stuff.length} bad word{(stuff.length - 1 && 's') || ''}
					</span>
					{#if logmessages != null}<span class="loghovercount">
							, {logmessages} log{(logmessages - 1 && 's') || ''}
						</span>{/if}
				</Hover>
			{/if}
		{/each}
		{@render bar(Math.floor(barheight * 0.34), barheight)}
		{@render bar(Math.floor(barheight * 0.67), barheight)}
		{@render bar(Math.floor(barheight * 1), barheight)}
	</div>
	<div
		class={`${logtimestamps !== null ? '' : 'skellyTheskeleton'} barlabelholder logbarlabelholder`}
		aria-label="Log count scale"
	>
		<span class="barlabelsizer" aria-hidden="true">{logbarheight}</span>
		<div class="barlabelplot">
			{@render barlabel(Math.floor(logbarheight * 0.34), logbarheight)}
			{@render barlabel(Math.floor(logbarheight * 0.67), logbarheight)}
			{@render barlabel(Math.floor(logbarheight), logbarheight)}
		</div>
	</div>
</div>

{#snippet barlabel(index: number, barheight: number)}
	<span class="barlabel" style={`bottom: calc(${(index * 100) / barheight}% - 10px)`}>
		{index}
	</span>
{/snippet}

{#snippet bar(index: number, barheight: number)}
	<div class="barplot">
		<div class="barwidth" style={`bottom: calc(${(index * 100) / barheight}% - 2px)`}></div>
	</div>
{/snippet}
