<script lang="ts">

	import { page } from '$app/state';
	import './Layout.css';
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
        <div class="titlebar">
          {@render Logo()}
          <h1 style = "margin: 0px">lexislurs for team fortress 2</h1>
          
        </div>
          <Search classNameform="bigsearchform" classNameinput="bigsearchinput" classnamebutton="bigsearchbutton" />
        {@render children()}
      </div>
 

      <svelte:head>
	<title>LexiSlurs</title>
  <link rel="icon" href={faviconUrl} />
  <meta name="description" content={"find bad words and mabye slurs sent by people in tf2"} />

  <meta property="og:type" content="website" />
  <meta property="og:url" content={page.url.href} />
  <meta property="og:title" content="LexiSlurs" />
  <meta property="og:description" content={"find bad words and mabye slurs sent by people in tf2"} />
  <meta property="og:image" content={`${page.url.origin}/logo.png`} />
  <meta property="og:image:width" content="960" />
  <meta property="og:image:height" content="960" />

  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="LexiSlurs" />
  <meta name="twitter:description" content={"find bad words and mabye slurs sent by people in tf2"} />
  <meta name="twitter:image" content={`${page.url.origin}/logo.png`} />
</svelte:head>