<script lang="ts">
  import { sendMessage } from "../../../../stores";
  import PlayerListPill from "../../PlayerListPill.svelte";

  export let playerId: number;

  function handleClick() {
    sendMessage({
      action: "seerPick",
      data: {
        id: playerId,
      },
    });
  }
</script>

<div class="seer-pick-pill">
  <PlayerListPill isClickable={true} on:player-list-pill-click={handleClick}>
    Investigate
  </PlayerListPill>
</div>

<style>
  :global(.seer-pick-pill > .player-list-pill) {
    background-color: var(--yellow);
    color: var(--main1);
  }
</style>
