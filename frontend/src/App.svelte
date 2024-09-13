<script lang="ts">
  import { onMount } from "svelte";
  import { connect, playerState, view } from "./stores";
  import { deadAllowedViews, views } from "./viewsMapping";

  import Error from "./lib/views/Error.svelte";
  import Dead from "./lib/views/Dead.svelte";

  export let gameCode: string | undefined;

  onMount(() => {
    if (gameCode !== undefined) {
      connect(gameCode);
    }
  });

  let x = $view.view;
</script>

{#if $playerState.alive}
  {#if $view.view in views}
    <svelte:component this={views[$view.view]} />
  {:else}
    <Error />
  {/if}
{:else if $view.view in deadAllowedViews}
  <svelte:component this={views[$view.view]} />
{:else}
  <Dead />
{/if}

<style>
</style>
