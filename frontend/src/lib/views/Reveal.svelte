<script lang="ts">
  import { view, playerState } from "../../stores";
  import { roleRevealModes } from "../../eventData";
  import GameScreenHeader from "../components/GameScreenHeader.svelte";
  import SmallPill from "../components/SmallPill.svelte";
  import Error from "./Error.svelte";
</script>

<div class="game">
  <GameScreenHeader header="Role Reveal">
    <SmallPill>
      {$view.data.data.progress}
    </SmallPill>
  </GameScreenHeader>
  {#if $view.data.mode in roleRevealModes}
    <svelte:component this={roleRevealModes[$view.data.mode]} />
  {:else}
    <Error>Unknown mode.</Error>
  {/if}
</div>

<style>
</style>
