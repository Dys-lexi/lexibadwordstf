<script lang="ts">
  import { goto } from '$app/navigation';
  import { usewsstore } from './websocketsearch';
  import '../../routes/Layout.css';

  let { classNameform = '', classNameinput = '', classnamebutton = '' } = $props();

  const { connect, disconnect, sendsearch } = usewsstore.getState();

  let isFocused = $state(false);
  let matches = $state(usewsstore.getState().matches);
  let inputRef: HTMLInputElement;

  $effect(() => usewsstore.subscribe((s) => (matches = s.matches)));

  async function onSubmit(e: SubmitEvent) {
    e.preventDefault();
    inputRef?.blur();
    disconnect();
    const username = new FormData(e.currentTarget as HTMLFormElement).get('user') as string;
    const match = matches.length && matches[0].n[0].toLocaleLowerCase().includes(username.toLocaleLowerCase());
    const id = match ? matches[0].id : username;
    await goto(`/${encodeURIComponent(id)}`);
  }

  async function onsuggest(id: string) {
    disconnect();
    await goto(`/${encodeURIComponent(id)}`);
  }

  function focused() {
    connect();
    isFocused = true;
  }

  function blurred() {
    setTimeout(() => (isFocused = false), 200);
  }
</script>
<div class = "flexstuff" style = "width:100%">
<div class="flexstuff" onfocusout={blurred}>
  <form class={classNameform} onsubmit={onSubmit}>
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
  <div style="position: relative; width: 100%" >
    {#if isFocused && matches.length}
      <div class="searchsuggestionholder">
        {#each matches as { n, id, a, g }, index (index)}
          <button type="button" class="suggestion{!index ? ' importantsuggestion' : ''}" onclick={() => onsuggest(id)}>
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