<script>
  import GameCodePill from "../components/GameCodePill.svelte";
  import PlayerCountPill from "../components/PlayerCountPill.svelte";
  import { view } from "../../stores";
  import PlayerList from "../components/PlayerList.svelte";

  $: playerCount = $view.data.players.length;
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
    <PlayerList players={$view.data.players} />
  </div>
  <button class="main-button">Let the night begin!</button>
</div>

<style>
  .lobby {
    margin-top: 2em;
    gap: 1em;

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
