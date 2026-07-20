<script lang="ts">
	import './profile.css';
	import type { BadWordsResponse, Userdetails, Badmessage } from '$lib/morestuff/types';
	import Hover from '$lib/morestuff/followingmouse.svelte';

	import { playedwithdetails, nonowords, getprofile, getbadcontext } from '$lib/remote/data.remote';
	import { Logo } from './const.svelte';
	import { getsteamurl } from './config';

	let { personresults, rendermore = (true && personresults.steam64 != '0') as boolean } = $props();

	//   let {steam64, profiledefault = {} as Userdetails, recall = 3600 as number} = $derived(things)
	function getteam(team?: string) {
		// console.log(team)
		if (team === 'red') return 'color:rgb(200,80,80)';
		if (team === 'blue') return 'color:rgb(100,100,200)';
		return '';
	}
	let badwords = $derived(nonowords(personresults.steam64));
	// let profilestuff: Userdetails}
	// const coords =  mousePosition()
	let renderhover = $state({} as Record<number, boolean>);
	let newest = $state(-1);
	function updaterenderhover(thing: number, value: boolean) {
		console.log(thing);
		renderhover[thing] = value;
		newest = thing;
	}
</script>

{#await badwords}
	<div class="skellyTheskeleton contents">
		{@render nonowordssnip((await nonowords('0')).badwords.nonowords, personresults, false)}
	</div>
{:then { badwords }}
	{@render nonowordssnip(badwords.nonowords, personresults, true)}
{:catch error}
	could not load bad words
{/await}

{#snippet nonowordssnip(
	badwords: Array<Badmessage>,
	personresults: Userdetails,
	rendermore = true as boolean,
	smol = false as boolean
)}
	<div class="nonowordsholder">
		{#if badwords.length}
			<!-- {console.log( personresults.badwords,"PANTS")} -->
			{#each badwords as badword, index (index)}
				
					{#if renderhover[index] && rendermore && newest == index && badword.index != null}
						<Hover>
							<div class="contexthoverholder">
								{#await getbadcontext({ matchid: badword.matchid, index: badword.index })}
									<div class="skellyTheskeleton contents">
										{@render nonowordssnip(
											(await nonowords('0')).badwords.nonowords.slice(0, 10),
											personresults,
											false,
											true
										)}
									</div>
								{:then stuff}
									{@render nonowordssnip(stuff.context.nonowords, personresults, false, true)}
								{/await}
							</div>
						</Hover>
					{/if}
					<div
						class="nonowordbox"
						style={badword.original ? 'background-color:rgba(255,180,180,0.2)' : ''}
					>
						{#if !smol}
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
						{/if}

						{' '}
						<div class="nonowordname" style={getteam(badword.team)}>
							{badword.name}
							<span class="loglinkwhite">:</span>
						</div>
						{' '}
						<div class="nonowordmessage">
							{badword.message}
						</div>
						<div    
					role="presentation"
                    class = "hoverplease"
					onmouseenter={() => (updaterenderhover (index, true))}
					onmouseleave={() => (updaterenderhover (index,false ))}
				></div>
					</div>
				
			{/each}
		{:else if rendermore}
			<h2>No bad words found for {personresults.currentusername}</h2>
		{/if}
	</div>
{/snippet}
