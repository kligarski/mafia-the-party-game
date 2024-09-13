<script lang="ts">
  import { sendMessage, view, type Player } from "../../../../stores";
  import PlayerListPill from "../../PlayerListPill.svelte";

  export let playerId: number;

  $: playerVotesData = $view.data.data.votes.find(
    (player: Player) => player.id === playerId
  );

  console.log($view.data.data.votes);
  console.log(playerId);
  console.log(
    $view.data.data.votes.find((player: Player) => player.id === playerId)
      .chosen
  );

  function handleClick() {
    if (playerVotesData.chosen) {
      sendMessage({
        action: "mafiaUnvote",
        data: {
          id: playerId,
        },
      });
    } else {
      sendMessage({
        action: "mafiaVote",
        data: {
          id: playerId,
        },
      });
    }
  }
</script>

<div
  class={playerVotesData.chosen
    ? "mafia-vote-mafia-pill-chosen"
    : "mafia-vote-mafia-pill-normal"}
>
  <PlayerListPill isClickable={true} on:player-list-pill-click={handleClick}>
    {playerVotesData.votes}/{$view.data.data.noMafiosi}
  </PlayerListPill>
</div>

<!-- svelte-ignore css-unused-selector -->
<style>
  :global(.mafia-vote-mafia-pill-chosen > .player-list-pill) {
    background-color: var(--red);
  }

  :global(.mafia-vote-mafia-pill-normal > .player-list-pill) {
    background-color: var(--main1);
  }
</style>
