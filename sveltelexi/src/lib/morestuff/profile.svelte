<script module lang="ts">
	import './profile.css';
	import type { Userdetails } from '$lib/morestuff/types';
	export { Profile };

	import { getprofile } from '$lib/remote/data.remote';
</script>

{#snippet Profile(steam64: string, profilestuffdefault = {} as Userdetails)}
	{@const profilestuff = getprofile(steam64)}
	
	<div class="woag">
		<a class="nameholderbad" href={`/${steam64}`}>
			<div class="nonowordavatarholder">
				{#if !profilestuffdefault.avatar}
					{#await profilestuff}
					
						Loading Profile
					{:then { profile, statuscode }}
					
						<img src={profile.frame} class="avatarholder" alt="" />
						<img
							src={`https://avatars.fastly.steamstatic.com/${profile.avatar}_full.jpg`}
							class="nonowordavatar"
							alt="avatar"
						/>
					{:catch error}
						could not load profile for {steam64} {error.message}
					{/await}
				{:else}
					<img src={profilestuffdefault.frame} class="avatarholder" alt="" />
					<img
						src={`https://avatars.fastly.steamstatic.com/${profilestuffdefault.avatar}_full.jpg`}
						class="nonowordavatar"
						alt="avatar"
					/>
				{/if}
			</div>

			{' '}
			<div class="profileitems">
				<div class="nonowordcurrentusername">
					{#if !profilestuffdefault.currentusername}
						{#await profilestuff then { profile, statuscode }}
							{profile.currentusername}
						{:catch error}
							Could not load name
						{/await}
					{:else}
						{profilestuffdefault.currentusername}
					{/if}
				</div>

				{#await profilestuff}
					Loading status
				{:then { profile, statuscode }}
					{#each Object.values(profile.stats) as data, index (index)}
						{#if data}
						<div class="badwordcounterw">{data}</div>
						{/if}
					{/each}
				{:catch error}
					<!-- could not load profile for {steam64} {error.message} -->
				{/await}
			</div>
		</a>
	</div>
{/snippet}
