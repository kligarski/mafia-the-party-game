<script lang="ts">
  import { sendMessage } from "../../../../stores";
  import PlayerListPill from "../../PlayerListPill.svelte";

  export let playerId: number;

  function handleClick() {
    sendMessage({
      action: "protectorPick",
      data: {
        id: playerId,
      },
    });
  }
</script>

<div class="protector-pick-pill">
  <PlayerListPill isClickable={true} on:player-list-pill-click={handleClick}>
    Protect
  </PlayerListPill>
</div>

<style>
  :global(.protector-pick-pill > .protector-pick-pill) {
    background-color: var(--blue);
  }
</style>
