<script lang="ts">
  import { onMount } from "svelte";
  import { connect, playerState, view } from "./stores";

  export let gameCode: string | undefined;

  onMount(() => {
    if (gameCode !== undefined) {
      connect(gameCode);
    }
  })
</script>

<main>
  <div>
    Hello, world!
  </div>
  <p>{JSON.stringify($view, null, 2)}</p>
  <p>{JSON.stringify($playerState, null, 2)}</p>
</main>

<style>
  div {
    font-size: 3rem;
  }
</style>
