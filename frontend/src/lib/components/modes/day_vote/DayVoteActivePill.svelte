<script lang="ts">
  import { sendMessage, view, type Player } from "../../../../stores";
  import PlayerListPill from "../../PlayerListPill.svelte";

  export let playerId: number;

  $: playerVotesData = $view.data.data.votes.find(
    (player: Player) => player.id === playerId
  );

  function handleClick() {
    sendMessage({
      action: "dayPlayerVote",
      data: {
        id: playerId,
      },
    });
  }
</script>

<div
  class={playerId === $view.data.data?.choice?.id
    ? "day-vote-active-pill-chosen"
    : "day-vote-active-pill-normal"}
>
  <PlayerListPill isClickable={true} on:player-list-pill-click={handleClick}>
    {playerVotesData.votes}/{$view.data.data.noPlayers}
  </PlayerListPill>
</div>

<style>
  :global(.day-vote-active-pill-chosen > .player-list-pill) {
    background-color: var(--red);
  }

  :global(.day-vote-active-pill-normal > .player-list-pill) {
    background-color: var(--main1);
  }
</style>
