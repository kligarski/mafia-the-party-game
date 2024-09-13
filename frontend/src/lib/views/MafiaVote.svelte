<script lang="ts">
  import { playerState, view } from "../../stores";
  import { mafiaVoteModes } from "../../viewsMapping";
  import GameScreenHeader from "../components/GameScreenHeader.svelte";
  import Error from "./Error.svelte";

  $: players = $view.data.data.mafia;
</script>

<div class="game">
  <GameScreenHeader header={"Night #" + $playerState.cycle} />
  {#if $view.data.mode in mafiaVoteModes}
    <svelte:component this={mafiaVoteModes[$view.data.mode]} />
  {:else}
    <Error>Unknown mode.</Error>
  {/if}
</div>
