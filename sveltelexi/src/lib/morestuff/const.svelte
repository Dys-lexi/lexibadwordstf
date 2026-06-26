<script module lang="ts">
  import logoUrl from "$lib/images/logosmall.png";
  export { Logo };
</script>

{#snippet Logo()}
<div>
      <a href="/">
        <img src={logoUrl} height={64} width={64} alt="logo" />
      </a>
    </div>
{/snippet}
