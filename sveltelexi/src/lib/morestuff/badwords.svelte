<script lang="ts">
	import './profile.css';
	import type { BadWordsResponse, Userdetails, Badmessage } from '$lib/morestuff/types';
	import Hover from '$lib/morestuff/followingmouse.svelte';
	import { ClassLogo } from '$lib/morestuff/const.svelte';
	import { playedwithdetails, nonowords, getprofile, getbadcontext } from '$lib/remote/data.remote';
	import { Logo } from './const.svelte';
	import { getsteamurl } from './getstemurl';
     import { onDestroy } from 'svelte';
	import Timelinesnippet from '$lib/morestuff/badtimeline.svelte'

        let leaveTimer: ReturnType<typeof setTimeout> | undefined;
	let { personresults, rendermore = (true && personresults.steam64 != '00000000000000000') as boolean } = $props();

	//   let {steam64, profiledefault = {} as Userdetails, recall = 3600 as number} = $derived(things)
	function getteam(team?: string) {
		// console.log(team)
		if (team === 'red') return 'color:rgb(200,80,80)';
		if (team === 'blue') return 'color:rgb(100,100,200)';
		return '';
	}
	let loading = $state(true)
	let errorcode = $state(null)

	let badwords =  $derived(personresults.steam64 == "00000000000000000" ?  null :  nonowords(personresults.steam64)  );
		$effect(() => {
	
		Promise.resolve(badwords).then((result) => {
			if (result === null) {return}
			badwordstuff = result.badwords.nonowords
			loading = false
		}).catch((error) => {errorcode = error});
	});
	
	// let profilestuff: Userdetails}
	// const coords =  mousePosition()
	let renderhover = $state({} as Record<number, boolean>);
	let newest = $state(-1);
	function updaterenderhover(thing: number, value: boolean) {
		// console.log(thing);
		renderhover[thing] = value;
		if (value) {
			newest = thing;
		}
	}
	let badwordstuff = $state((await nonowords('0')).badwords.nonowords)
</script>

<div class = "outlinethingy">
{#if errorcode == null}

	<div class={loading ? "skellyTheskeleton contents"  : "contents"}>
	
		{@render timelinesnippet(badwordstuff, personresults)}
		{@render nonowordssnip(badwordstuff, personresults, true)}
	</div>
{:else}
failed to load bad messages {errorcode}
{/if}
</div>

{#snippet timelinesnippet(
	badwords: Array<Badmessage>,
	personresults: Userdetails,
)}
	{#if badwords.length}
	<div class="nonowordtimestamp" style = "width: fit-content">Bad word{(badwordstuff.length -1)  && "s" || ""} for {personresults.currentusername}</div>
	<Timelinesnippet badwords={badwords} personresults={personresults}/>
	{/if}
{/snippet}
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
				{#if renderhover[index]  && newest == index && badword.index != null}
					<Hover>
						<div class="contexthoverholder">
						<div class="nonowordtimestamp loadingtext" style = "width: fit-content">Logid: {badword.matchid}</div>
							{#await getbadcontext({ matchid: badword.matchid, index: badword.index })}
								<div class="skellyTheskeleton contents">
									{@render nonowordssnip(
										(await nonowords('0')).badwords.nonowords.slice(0, 11),
										personresults,
										false,
										true
									)}
								</div>
							{:then stuff}
								{@render nonowordssnip(stuff.context.nonowords, personresults, false, true)}
							{:catch error}
							<h2>realy weird error loading messagecontext: {error.body.message}</h2>
							{/await}
						</div>
					</Hover>
				{/if}
				<div 
				role="presentation"
				 onmouseenter={() => {
                if (leaveTimer) clearTimeout(leaveTimer);
                updaterenderhover(index, true);
        }}
        onmouseleave={() => {
                leaveTimer = setTimeout(() => {
                        updaterenderhover(index, false);
                }, 100);
        }}
					class="nonowordbox"
					style={badword.original ? 'background-color:rgba(255,180,180,0.2)' : ''}
				>
					{#if !smol}
						<a
						// style = "z-index: 11"
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
					{#if badword.classes?.length}
						<!-- {@const biggestclassplaytime = Math.max(
                                1,
                                ...badword.classes.map((classinfo) => classinfo.time)
                            )} -->
						{@const biggestclassplaytime = badword.classes.reduce(
							(total, classinfo) => total + classinfo.time,
							0
						)}

						<div class="classholder">
							{#each badword.classes as classinfo, index (index)}
								<div class="woag">
									{@render ClassLogo(classinfo.class)}
									<div class="woag" style="align-items: flex-end;background-color:black">
										<div
											class="playedaspercent"
											style={`height: ${(classinfo.time * 100) / biggestclassplaytime}%`}
										></div>
									</div>
								</div>
							{/each}
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
					<!-- <div
						role="presentation"
						class="hoverplease"
						onmouseenter={() => updaterenderhover(index, true)}
						onmouseleave={() =>
							leaveTimer = setTimeout(() => {
								updaterenderhover(index, false);
							}, 100)}
							
					></div> -->
				</div>
			{/each}
		{:else if rendermore}
			<h2>No bad words found for {personresults.currentusername}</h2>
		{/if}
	</div>
{/snippet}
