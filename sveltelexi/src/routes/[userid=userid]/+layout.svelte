<script lang="ts">

	import { page } from '$app/state';
	import '../Layout.css';
	import { Logo } from "$lib/morestuff/const.svelte";
  import Search from "$lib/morestuff/Search.svelte";
	import faviconUrl from "$lib/images/logosmall.png";
	let { children } = $props();


</script>
  
<style>
	
</style>

      <div
        class="mainthing"
      >

          <Search classNameform="bigsearchform" classNameinput="bigsearchinput" classnamebutton="bigsearchbutton" />
        {@render children()}
      </div>
 


  