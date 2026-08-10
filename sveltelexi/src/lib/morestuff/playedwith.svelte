<script lang="ts">
	import { getprofile, playedwithdetails } from '$lib/remote/data.remote';
		import type { BadWordsResponse, Userdetails, Badmessage } from '$lib/morestuff/types';

	import Miniprofile from './miniprofile.svelte';
	import type { PlayedWithResponse } from './types';
	import { playedwithResponse } from './config';

	let { personresults, more }: { personresults: Userdetails; more: boolean } = $props();

	let playedwithdata = $state((await playedwithdetails({steam64:'0',more:false})))
		let loading = $state(true)
	let errorcode = $state(null)
		let playedwithreal =  $derived(personresults.steam64 == "00000000000000000" ?  null :  playedwithdetails({steam64:personresults.steam64,more})  );
$effect(() => {

		Promise.resolve(playedwithreal).then((result) => {
			if (result === null) {return}
			playedwithdata = result
			loading = false
		}).catch((error) => {errorcode = error});
	});
</script>
{#if playedwithdata.playedwithdata.playedwith.length}
<div class="outlinethingy">

{#if errorcode == null}
<div class={loading ? "skellyTheskeleton contents"  : "contents"}>
		{@render playedWithList(playedwithdata.playedwithdata)}
	</div>
	{:else}
failed to load playedwith {errorcode}
{/if}
</div>
{/if}


{#snippet playedWithList(playedwithdata: PlayedWithResponse)}
	{#if playedwithdata.playedwith.length}
		<div class="playedwithholderholder">
			<div class="playedwithinfo">
				<a class="nonowordtimestamp loglink" href={more ? `/${personresults.steam64}` : `/${personresults.steam64}/playedwith`}>
					{personresults.currentusername} has played with {playedwithdata.totalplayedwith} people
				</a>
			</div>
			<div class:playedwithholderbig={more} class="playedwithholder">
				{#each playedwithdata.playedwith as data,index (index)}
					<Miniprofile {data} biggestplayedwith={playedwithdata.biggestplayedwith} />
				{/each}
			</div>
		</div>
	{/if}
{/snippet}
