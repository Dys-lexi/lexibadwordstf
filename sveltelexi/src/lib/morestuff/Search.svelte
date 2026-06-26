<script lang="ts">
  import { goto } from '$app/navigation';
  import { usewsstore } from './websocketsearch';
  import '../../routes/Layout.css';

  let { classNameform = '', classNameinput = '', classnamebutton = '' } = $props();

  const { connect, disconnect, sendsearch } = usewsstore.getState();

  let isFocused = $state(false);
  let matches = $state(usewsstore.getState().matches);
  let inputRef: HTMLInputElement;
  let form: HTMLFormElement;
 let steam64: string | null = null;
  let searchsuggestionholder: HTMLDivElement
  $effect(() => usewsstore.subscribe((s) => (matches = s.matches)));

  async function onSubmit(e: SubmitEvent) {
    e.preventDefault();
    inputRef?.blur();
    disconnect();
    const username = (steam64  || new FormData(e.currentTarget as HTMLFormElement).get('user')) as string;
    steam64 = null
    const match = matches.length && matches[0].n[0].toLocaleLowerCase().includes(username.toLocaleLowerCase());
    const id = match ? matches[0].id : username;
    await goto(`/${encodeURIComponent(id)}`);
  }

  async function onsuggest(id: string, name: string) {
    disconnect();
    steam64 = id
    inputRef.value = name
    form.requestSubmit();
    isFocused = false;
  }

  function focused() {
    connect();
    isFocused = true;
  }

function blurred(event: FocusEvent) {
    const next = event.relatedTarget as HTMLElement | null;

    if (next && searchsuggestionholder.contains(next)) {
        return;
    }

    isFocused = false;
}

</script>
<div class = "flexstuff" style = "width:100%">
<div class="flexstuff flexsearchthing" onfocusout={blurred}>
  <form class={classNameform} onsubmit={onSubmit}   bind:this={form}>
    <input
      bind:this={inputRef}
      autocorrect="off"
      spellcheck="false"
      autocomplete="off"
      name="user"
      class={classNameinput}
      placeholder="Enter somones profile link, Steamid or Name"
      onfocus={(e) => { focused(); e.currentTarget.select(); sendsearch(e.currentTarget.value); }}
      oninput={(e) => { focused(); sendsearch(e.currentTarget.value); }}
    />
    <button type="submit" class={classnamebutton}>Search</button>
  </form>
  <div bind:this={searchsuggestionholder} style="position: relative; width: 100%" >
    {#if isFocused && matches.length}
      <div class="searchsuggestionholder">
        {#each matches as { n, id, a, g }, index (index)}
          <button type="button" class="suggestion{!index ? ' importantsuggestion' : ''}" onclick={() => onsuggest(id,n[0])}>
            <img
              style="height: 100%"
              src={`https://avatars.fastly.steamstatic.com/${a ? a : 'fef49e7fa7e1997310d705b2a6158ff8dc1cdfeb'}.jpg`}
              alt=""
            />
            <div class="suggestionname">
              {n[0]} {#each n.slice(1) as name, i}<span class="subsuggestionname{i}">{name}</span>{/each}
            </div>
            {#if g != 0}<span class="logcounter">{g == 1 ? '1 Log' : `${g} Logs`}</span>{/if}
          </button>
        {/each}
        <div class="notice">Log counts are only for usernames that match the search</div>
      </div>
    {/if}
  </div>
</div>
</div>