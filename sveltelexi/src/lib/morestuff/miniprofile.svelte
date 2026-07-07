<script lang="ts">
	import './profile.css';
	import type { playedwithitem } from '$lib/morestuff/types';
	// export { Profile , };
	import { copy } from './const.svelte';
	import { page } from '$app/state';
	import Hoverprofile from '$lib/morestuff/hoverprofile.svelte';
	import { getprofile } from '$lib/remote/data.remote';
	// let {steam64:string,profiledefault = {} as Userdetails} = $props();
	// import { mousePosition } from './store.js';
	async function copylink(steam64: string) {
		await navigator.clipboard.writeText(`${page.url.origin}/${steam64}`);
	}
	let { data, biggestplayedwith }: { data: playedwithitem; biggestplayedwith: number } = $props();
	//   let {steam64, profiledefault = {} as Userdetails, recall = 3600 as number} = $derived(things)

	// let profilestuff: Userdetails}
	// const coords =  mousePosition()
</script>

<a href={`/${data.steam64}`} class="playedwithstatsandwhatnot"> 
 <img
    style="filter:blur(5px) brightness(20%) saturate(200%);"

				src={`https://avatars.fastly.steamstatic.com/${data.avatar}_full.jpg`}
				class="bigblur"
				alt=""
			/>
	<div class="playedwithperson">
		<Hoverprofile steam64={data.steam64} profiledefault={data} />
		<div class="playedwithpercent playedwithbad"></div>
		<div
			class="playedwithpercent"
			style={`height: ${(data.commonmatches * 100) / biggestplayedwith}%`}
		></div>
		<img
			class="playedwithphoto"
			src={`https://avatars.fastly.steamstatic.com/${data.avatar}.jpg`}
			alt="avatar"
		/>

		<div class="goawayoverflow playedwithname">{data.currentusername}</div>
	</div>
    <div class="playedwithstats">
        <div class="badwordcounterw">{data.commonmatches} mutual log{!(data.commonmatches - 1)? "" : "s" }</div>
    </div>
   
</a>
