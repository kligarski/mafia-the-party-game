<script lang="ts">
  import { view, type Player } from "../../../../stores";
  import PlayerListPill from "../../PlayerListPill.svelte";

  export let playerId: number;

  $: playerVotesData = $view.data.data.votes.find(
    (player: Player) => player.id === playerId
  );
</script>

<div
  class={playerId === $view.data.data?.choice?.id
    ? "day-vote-passive-pill-chosen"
    : "day-vote-passive-pill-normal"}
>
  <PlayerListPill>
    {playerVotesData.votes}/{$view.data.data.noPlayers}
  </PlayerListPill>
</div>

<style>
  :global(.day-vote-passive-pill-chosen > .player-list-pill) {
    background-color: var(--red);
  }

  :global(.day-vote-passive-pill-normal > .player-list-pill) {
    background-color: var(--main1);
  }
</style>
