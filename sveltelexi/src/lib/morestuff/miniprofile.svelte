<script lang="ts">
	import './profile.css';
	import type { Userdetails } from '$lib/morestuff/types';
	// export { Profile , };
	import { copy } from './const.svelte';
	import { page } from '$app/state';
	import { getprofile } from '$lib/remote/data.remote';
	// let {steam64:string,profiledefault = {} as Userdetails} = $props();
	// import { mousePosition } from './store.js';
	async function copylink(steam64: string) {
		await navigator.clipboard.writeText(`${page.url.origin}/${steam64}`);
	}
	let {
		steam64,
		profiledefault = {},
		recall = 3600 as number,
		showcopy = true as boolean
	} = $props();
	let profilestuff = $derived(!profiledefault.stats ? getprofile({ steam64, recall }) : undefined);
	//   let {steam64, profiledefault = {} as Userdetails, recall = 3600 as number} = $derived(things)

	// let profilestuff: Userdetails}
	// const coords =  mousePosition()
</script>