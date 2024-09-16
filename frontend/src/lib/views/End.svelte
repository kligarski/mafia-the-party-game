<script lang="ts">
  import { playerState, sendMessage, view } from "../../stores";
  import GameEndBigTeam from "../components/modes/end/GameEndBigTeam.svelte";
  import PlayerList from "../components/PlayerList.svelte";

  $: teamName = $view.data.mode.slice(0, -4);

  function backToMenu() {
    sendMessage({
      action: "backToMenu",
      data: {},
    });
  }

  function newGame() {
    sendMessage({
      action: "newGame",
      data: {},
    });
  }
</script>

<div class="game space-between">
  <GameEndBigTeam {teamName} />
  <PlayerList players={$view.data.data.players} />

  <div class="buttons">
    <button class="main-button" on:click={backToMenu}>Back to menu</button>
    {#if $playerState.role === "moderator"}
      <button class="main-button" on:click={newGame}>New game</button>
    {/if}
  </div>
</div>

<style>
  .buttons {
    display: flex;
    align-items: center;
    flex-wrap: wrap;

    width: 100%;
  }

  .buttons > * {
    margin-left: auto;
    margin-right: auto;
  }
</style>
