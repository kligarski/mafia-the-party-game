<script lang="ts">
  import type { Player } from "../../stores";
  import PlayerPill from "./PlayerPill.svelte";

  export let players: Player[];
</script>

<div>
  {#each players as player}
    <PlayerPill {player} />
  {/each}
</div>

<style>
  div {
    flex-grow: 1;
    flex-shrink: 1;

    display: flex;
    flex-direction: column;
    gap: 0.5em;
    align-items: center;

    margin-top: 1em;
    padding: 0 0.5em;

    width: 100%;
    overflow-y: auto;
  }
</style>
