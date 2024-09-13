<script lang="ts">
  import type { ComponentType, SvelteComponent } from "svelte";
  import { type Player, playerState } from "../../stores";
  import PlayerPill from "./PlayerPill.svelte";

  export let players: Player[];
  export let extra: ComponentType<
    SvelteComponent<{ playerId: number }>
  > | null = null;

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
  {#each sortedPlayers as player (player.id)}
    {#if extra === null}
      <PlayerPill {player} />
    {:else}
      <PlayerPill {player}>
        <svelte:component this={extra} playerId={player.id} />
      </PlayerPill>
    {/if}
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
