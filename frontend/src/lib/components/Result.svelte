<script lang="ts">
  import { type Player, sendMessage, view } from "../../stores";
  import BigRole from "./BigRole.svelte";
  import PlayerList from "./PlayerList.svelte";

  export let roleName: string;
  export let players: Player[];
  export let onClickMessage: string =
    "end" + $view.view.charAt(0).toUpperCase() + $view.view.slice(1);

  function endEvent() {
    sendMessage({
      action: onClickMessage,
      data: {},
    });
  }
</script>

<div class="result">
  <BigRole {roleName} pick={true} />
  <PlayerList {players} />
  <div class="additional-info">
    Make sure player{players.length > 1 ? "s" : ""}
    from this phase go{players.length > 1 ? "" : "es"} back to sleep.
  </div>
  <button class="main-button" on:click={endEvent}>Continue</button>
</div>

<style>
  .result {
    flex-grow: 1;
    flex-shrink: 1;

    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    gap: 1.5em;
    min-height: 5em;
  }
</style>
