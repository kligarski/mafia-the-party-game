<script lang="ts">
  import { onMount } from "svelte";
  import { connect, playerState, view } from "./stores";
  import { views } from "./viewsMapping";

  import Error from "./lib/views/Error.svelte";

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
{:else}
  <!-- TODO -->
  <Error />
{/if}

<style>
</style>
