<script lang="ts">
  import { playerState, sendMessage } from "../../../../stores";
  import Icon from "../../../icons/Icon.svelte";
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

{#if playerId !== $playerState.id}
  <div class="seer-pick-pill">
    <PlayerListPill isClickable={true} on:player-list-pill-click={handleClick}>
      <Icon name="search" />
    </PlayerListPill>
  </div>
{/if}

<style>
  :global(.seer-pick-pill > .player-list-pill) {
    background-color: var(--yellow);
    color: var(--main1);
  }
</style>
