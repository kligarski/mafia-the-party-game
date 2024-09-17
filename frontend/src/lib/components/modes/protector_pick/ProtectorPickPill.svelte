<script lang="ts">
  import { sendMessage } from "../../../../stores";
  import Icon from "../../../icons/Icon.svelte";
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
    <Icon name="verified_user" />
  </PlayerListPill>
</div>

<style>
  :global(.protector-pick-pill > .player-list-pill) {
    background-color: var(--blue);
    color: var(--main1);
  }
</style>
