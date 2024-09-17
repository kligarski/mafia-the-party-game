<script lang="ts">
  import { createEventDispatcher } from "svelte";

  export let isClickable: boolean = false;

  const dispatch = createEventDispatcher();

  function handleClick() {
    dispatch("player-list-pill-click");
  }
</script>

{#if isClickable}
  <button class="player-list-pill" on:click={handleClick}>
    <slot />
  </button>
{:else}
  <div class="player-list-pill">
    <slot />
  </div>
{/if}

<style>
  .player-list-pill {
    display: flex;
    justify-content: center;
    align-items: center;

    padding: 0.3em 0.7em;

    border-radius: 2rem;
    border: none;

    font-family: "Kanit", sans-serif;
    font-weight: 400;
    font-size: 0.8em;

    min-width: 3em;

    color: var(--main3);
  }
</style>
