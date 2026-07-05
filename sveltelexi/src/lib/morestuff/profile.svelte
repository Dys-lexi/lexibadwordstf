<script  lang="ts">
	import './profile.css';
	import type { Userdetails } from '$lib/morestuff/types';
	// export { Profile , };
	import {copy} from "./const.svelte"
	import { page } from '$app/state';
	import { getprofile } from '$lib/remote/data.remote';
	// let {steam64:string,profiledefault = {} as Userdetails} = $props();
	// import { mousePosition } from './store.js';
	  async function copylink(steam64: string) {
    await navigator.clipboard.writeText(`${page.url.origin}/${steam64}`);
	  }
	  let {steam64, profiledefault = {} as Userdetails, recall = 3600 as number}= $props()
	  let profilestuff = $derived(!profiledefault.stats  ? getprofile({ steam64, recall }) : undefined);
	//   let {steam64, profiledefault = {} as Userdetails, recall = 3600 as number} = $derived(things)

	 
	// let profilestuff: Userdetails}
// const coords =  mousePosition()
  
	  

</script>

	


	<div class="woag">
	
		<a class="nameholderbad" href={`/${steam64}`}>
			<div class="nonowordavatarholder">
				{#if profilestuff}
					{#await profilestuff}
					
						Loading Profile
					{:then { profile, statuscode }}
					{#if profile.frame}
						<img src={profile.frame} class="avatarholder" alt="" />
						{/if }
						<img
							src={`https://avatars.fastly.steamstatic.com/${profile.avatar}_full.jpg`}
							class="nonowordavatar"
							alt=""
						/>
					{:catch error}
						could not load profile for {steam64} {error.message}
					{/await}
				{:else}
					{#if profiledefault.frame}
					<img src={profiledefault.frame} class="avatarholder" alt="" />
					{/if}
					<img
						src={`https://avatars.fastly.steamstatic.com/${profiledefault.avatar}_full.jpg`}
						class="nonowordavatar"
						alt=""
					/>
				{/if}
			</div>

			{' '}
			<div class="profileitems">
					<button  onclick={() => copylink(steam64)} class="copyimage"> {@render copy()} </button>
				<div class="nonowordcurrentusername">
		
					{#if profilestuff}
						{#await profilestuff then { profile, statuscode }}
							{profile.currentusername}
						{:catch error}
							Could not load name
						{/await}
					{:else if profiledefault.currentusername}
						{profiledefault.currentusername}
					{/if}
				</div>

				{#if profilestuff}
				{#await profilestuff then  { profile, statuscode }}
					
		
					{#each Object.values(profile.stats) as data, index (index)}
						{#if data}
						<div class="badwordcounterw">{data}</div>
						{/if}
					{/each}
				{:catch error}
					<!-- could not load profile for {steam64} {error.message} -->
				{/await}
				{:else}
					{#each Object.values(profiledefault.stats ?? []) as data, index (index)}
						{#if data}
						<div class="badwordcounterw">{data}</div>
						{/if}
					{/each}
				{/if}
			</div>
		</a>
	</div>
