<script lang="ts">
  import { view, type Player } from "../../../../stores";
  import PlayerListPill from "../../PlayerListPill.svelte";

  export let playerId: number;

  $: playerVotesData = $view.data.data.votes.find(
    (player: Player) => player.id === playerId
  );
</script>

<div class="mafia-vote-moderator-pill-normal">
  <PlayerListPill>
    {playerVotesData.votes}/{$view.data.data.noMafiosi}
  </PlayerListPill>
</div>

<style>
  :global(.mafia-vote-moderator-pill-normal > .player-list-pill) {
    background-color: var(--main1);
  }
</style>
