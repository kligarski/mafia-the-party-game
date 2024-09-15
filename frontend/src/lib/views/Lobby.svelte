<script type="ts">
  import GameCodePill from "../components/GameCodePill.svelte";
  import PlayerCountPill from "../components/PlayerCountPill.svelte";
  import { view, sendMessage, playerState } from "../../stores";
  import PlayerList from "../components/PlayerList.svelte";
  import LobbyActionsButtons from "../components/modes/lobby/LobbyActionsButtons.svelte";
  import { afterUpdate } from "svelte";

  $: playerCount = $view.data.players.length;

  afterUpdate(() => {
    console.log($view);
    console.log($playerState);
  });

  function gameStart() {
    sendMessage({
      action: "startGame",
      data: {},
    });
  }
</script>

<div class="lobby">
  <div class="space-between-box">
    <h1>Game code:</h1>
    <GameCodePill />
  </div>
  <div class="players-box">
    <div class="space-between-box">
      <h1>Players:</h1>
      <PlayerCountPill count={playerCount} />
    </div>
    <PlayerList
      players={$view.data.players}
      extra={$playerState.role === "moderator" ? LobbyActionsButtons : null}
    />
  </div>
  {#if $playerState.role === "moderator"}
    <button class="main-button" on:click={gameStart}
      >Let the night begin!</button
    >
  {/if}
</div>

<style>
  .lobby {
    margin-top: 2em;
    gap: 1.5em;

    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 0;
  }

  .players-box {
    flex-grow: 1;
    flex-shrink: 1;

    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;

    min-height: 0;
  }

  .space-between-box {
    flex-shrink: 0;

    width: 100%;

    display: flex;
    justify-content: space-between;
    align-items: center;
  }
</style>
