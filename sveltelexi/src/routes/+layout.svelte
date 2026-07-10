<script lang="ts">

	import { page, navigating } from '$app/state';
	import './Layout.css';
	import { Logo } from "$lib/morestuff/const.svelte";
  import Search from "$lib/morestuff/Search.svelte";
	import faviconUrl from "$lib/images/logosmall.png";
	let { children ,data} = $props();
	let { temp,randomnumber } = $derived(data);
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
        <a class="Iwantthisinthetopright" href = "https://sans.xixya.com">
        It is {temp.temp.toLocaleString()}°C in Allusive's room</a>
        {/if}
        	{:catch error}
          {" "}
				{/await}


  