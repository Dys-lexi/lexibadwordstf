<script lang="ts">
	import './profile.css';
	import type { BadWordsResponse, Userdetails, Badmessage } from '$lib/morestuff/types';
	import { string } from 'valibot';
	import Hover from '$lib/morestuff/followingmouse.svelte';
	let { badwords, personresults }: { badwords: Array<Badmessage>; personresults: Userdetails } =
		$props();

	//   let {steam64, profiledefault = {} as Userdetails, recall = 3600 as number} = $derived(things)
	const { binnings, barheight } = $derived.by(() => {
		const binnings: Record<number, Badmessage[]> = {};
		let biggestnumber = 0;
		let smallestnumber = 0;
		let barheight = 10;
		for (const badword of badwords) {
			const year: number = new Date(badword.timestamp * 1000).getFullYear() % 100;

			(binnings[year] ??= []).push(badword);
			biggestnumber = Math.max(biggestnumber, year);
			smallestnumber = (smallestnumber && Math.min(year, smallestnumber)) || biggestnumber;
		}
		for (let i = smallestnumber; i <= new Date().getFullYear() % 100; i++) {
			binnings[i] ??= [];
			barheight = Math.max(barheight, binnings[i].length);
		}

		return { binnings, barheight };
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
		{#each Object.entries(binnings) as [year, stuff], index (index)}
			<div
				class="yearholder"
				role="presentation"
				onmouseenter={() => {
					renderhover = index;
				}}
				onmouseleave={() => {
					renderhover = null;
				}}
			>
				<div class="barholder">
					<div class="bar" style={`height: ${(stuff.length * 100) / barheight}%; background-color: rgb(${(stuff.length * 150) / barheight+100},100,100)`}></div>
				</div>
				{year}
			</div>
			{#if renderhover == index}
				<Hover>
					{stuff.length} bad word{(stuff.length - 1 && 's') || ''}
				</Hover>
			{/if}
		{/each}
		{@render bar(Math.floor(barheight * 0.34), barheight)}
		{@render bar(Math.floor(barheight * 0.67), barheight)}
		{@render bar(Math.floor(barheight * 1), barheight)}
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
