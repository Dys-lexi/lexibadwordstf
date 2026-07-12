<script  lang="ts">
	import './profile.css';
	import type { Userdetails } from '$lib/morestuff/types';
	// export { Profile , };
	import {copy} from "./const.svelte"
   import Profile from '$lib/morestuff/profile.svelte'
	import { page } from '$app/state';
	import { getprofile } from '$lib/remote/data.remote';
	// let {steam64:string,profiledefault = {} as Userdetails} = $props();
	import { mousePosition } from './store.js';
	import { onMount } from 'svelte';
	import { readable, type Readable } from 'svelte/store';

	type Coordinates = { x: number; y: number };
	let coords: Readable<Coordinates> = $state(readable({ x: 0 , y: 0 }));

	onMount(() => {
		coords = mousePosition();
	});
	  async function copylink(steam64: string) {
    await navigator.clipboard.writeText(`${page.url.origin}/${steam64}`);
	  }
	  let {steam64,profiledefault = {}}= $props()
	//   let profilestuff = $derived( getprofile({ steam64, recall:0 }) );
	//   let {steam64, profiledefault = {} as Userdetails, recall = 3600 as number} = $derived(things)
    //    profiledefault={(await profilestuff).profile}
	 let renderhover = $state(false)
	// let profilestuff: Userdetails}


let hoverWidth = $state(0)
let hoverHeight = $state(0)
let innerWidth = $state(0)
let innerHeight = $state(0)
const hoverOffset = 12

function clamp(value: number, min: number, max: number) {
	return Math.min(Math.max(value, min), Math.max(min, max))
}

let hoverX = $derived(
	$coords.x === 0 ? -999 :
	clamp($coords.x + hoverOffset, hoverOffset, innerWidth - hoverWidth - hoverOffset)
)
let hoverY = $derived(
	clamp($coords.y + hoverOffset, hoverOffset, innerHeight - hoverHeight - hoverOffset)
)
	  

</script>


<svelte:window bind:innerWidth={innerWidth} bind:innerHeight={innerHeight} />



 <div class = "hoverplease"
    role="presentation"
    onmouseenter={() => {renderhover = true;}}
    onmouseleave={() => renderhover = false}
  >
	<!-- {renderhover} -->
	{#if renderhover}
	<div
		class = "hoverprofile"
		bind:clientWidth={hoverWidth}
		bind:clientHeight={hoverHeight}
		style={`top:${hoverY}px;left:${hoverX}px`}
	>
			<Profile steam64={steam64} profiledefault={profiledefault}  showcopy={false}/> 
		</div>
	{/if}

</div>
