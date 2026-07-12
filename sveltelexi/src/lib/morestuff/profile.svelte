<script lang="ts">
	import './profile.css';
	import type { Userdetails } from '$lib/morestuff/types';
	// export { Profile , };
	import { copy } from './const.svelte';
	import { page } from '$app/state';
	import { getprofile } from '$lib/remote/data.remote';
	import { getsteamurl } from '$lib/morestuff/config';

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

<div class="woag">
	<div class="nameholderbad">
		<div class="nonowordavatarholder">
			{#if !profiledefault.avatar && profilestuff}
				{#await profilestuff}
					<img
						src={`https://avatars.fastly.steamstatic.com/fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb_full.jpg`}
						class="nonowordavatar"
						alt=""
					/>
				{:then { personresults, statuscode }}
					{#if personresults.frame}
						<img src={personresults.frame} class="avatarholder" alt="" />
					{/if}
					<img
						src={`https://avatars.fastly.steamstatic.com/${personresults.avatar}_full.jpg`}
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
		{#if !profiledefault.avatar && profilestuff}
			{#await profilestuff then { personresults, statuscode }}
				<img
					src={`https://avatars.fastly.steamstatic.com/${personresults.avatar}_full.jpg`}
					class="bigblur"
					alt=""
				/>
			{:catch error}
				<!-- could not load profile for {steam64} {error.message} -->
			{/await}
		{:else}
			<img
				src={`https://avatars.fastly.steamstatic.com/${profiledefault.avatar}_full.jpg`}
				class="bigblur"
				alt=""
			/>
		{/if}
		{' '}
		<div class="profileitems">
			{#if showcopy}
				<button onclick={() => copylink(steam64)} class="copyimage"> {@render copy()} </button>
			{/if}
			<a class="nonowordcurrentusername underlineme" href={getsteamurl(steam64)}>
				{#if !profiledefault.currentusername && profilestuff}
					{#await profilestuff}
						Loading Profile
					{:then { personresults, statuscode }}
						{personresults.currentusername}
					{:catch error}
						<!-- Could not load name -->
					{/await}
				{:else if profiledefault.currentusername}
					{profiledefault.currentusername}
				{/if}
			</a>

			{#if !profiledefault.stats && profilestuff}
				{#await profilestuff}
					<div class="badwordcounterw">Loading stats</div>
				{:then { personresults, statuscode }}
					{#each Object.values(personresults.stats) as data, index (index)}
						{#if data && index == 0}
							<a class="badwordcounterw underlineme" href={`/${steam64}/aliases`}>{data}</a>
						{:else if data && index == 1}
							<a class="badwordcounterw underlineme" href={getsteamurl(steam64)}>{data}</a>
						{:else if data}
							<div class="badwordcounterw">{data}</div>
						{/if}
					{/each}
				{:catch error}
					<!-- could not load profile for {steam64} {error.message} -->
				{/await}
			{:else}
				{#each Object.values(profiledefault.stats ?? []) as data, index (index)}
					{#if data && index == 0}
						<a class="badwordcounterw underlineme" href={`/${steam64}/aliases`}>{data}</a>
					{:else if data && index == 1}
						<a class="badwordcounterw underlineme" href={getsteamurl(steam64)}>{data}</a>
					{:else if data}
						<div class="badwordcounterw">{data}</div>
					{/if}
				{/each}
			{/if}
			{#if !profiledefault.mostrecentmatchtimestamp && profilestuff}
				{#await profilestuff then { personresults, statuscode }}
					{#if personresults.mostrecentmatchtimestamp}
						<div class="badwordcounterw">
							Last seen
							{new Date(personresults.mostrecentmatchtimestamp * 1000).toLocaleDateString()}
						</div>
					{/if}
				{:catch error}
					<!-- could not load profile for {steam64} {error.message} -->
				{/await}
			{:else}
				<div class="badwordcounterw">
					Last seen
					{new Date(profiledefault.mostrecentmatchtimestamp * 1000).toLocaleDateString()}
				</div>
			{/if}
		</div>
	</div>
</div>
