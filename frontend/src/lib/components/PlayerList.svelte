<script lang="ts">
  import { type Player, playerState } from "../../stores";
  import PlayerPill from "./PlayerPill.svelte";

  export let players: Player[];

  $: sortedPlayers = players.sort((a: Player, b: Player) => {
    if (a.role === "moderator") {
      return -1;
    } else if (b.role === "moderator") {
      return 1;
    } else if (a.id === $playerState.id) {
      return -1;
    } else if (b.id === $playerState.id) {
      return 1;
    } else {
      return a.id - b.id;
    }
  });
</script>

<div>
  {#each sortedPlayers as player}
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

    margin-top: 0.4em;
    padding: 0 0.5em;

    width: 100%;
    overflow-y: auto;
  }
</style>
