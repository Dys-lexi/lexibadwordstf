<script lang="ts">

	import { page, navigating } from '$app/state';
	import './Layout.css';
  import faviconUrl from '$lib/images/logosmall.png';
  	import { onMount } from 'svelte';
	import { Logo } from "$lib/morestuff/const.svelte";
	let { children ,data} = $props();
	let { temp,randomnumber } = $derived(data);
    onMount(() => {
        document.cookie = 'client=true; Path=/; SameSite=Strict;maxAge=604800';
  })
</script>
  
<style>
	
</style>

      <div
        class="mainthing"
      >
        <div class="titlebar">
          {@render Logo(randomnumber)}
          <h1 style = "margin: 0px">lexislurs for team fortress 2</h1>
          
        </div>
        <!-- {#if navigating.to}
          owag
        	{:else} -->
        {@render children()}
        <!-- {/if} -->
      </div>
 
  
      				{#await temp}
 {" "}
				{:then temp}
        {#if temp.statuscode == 200}
        
        <a
          class="Iwantthisinthetopright"
          href="https://sans.xixya.com"
          title={temp.lastupdate
            ? `Last updated at ${new Date(Number(temp.lastupdate) * 1000).toLocaleString()}`
            : undefined}
        >
        It is {temp.temp.toLocaleString()}°C in Allusive's room</a>
        {/if}
        	{:catch error}
          {" "}
				{/await}


  <svelte:head>
	<title>LexiSlurs</title>

	  <link rel="icon" href={faviconUrl} />
  </svelte:head>
