<script>
  import { playerState, sendMessage, view } from "../../stores";
  import BigRole from "../components/BigRole.svelte";

  import GameScreenHeader from "../components/GameScreenHeader.svelte";

  $: player = $view.data.mode === "someoneDied" ? $view.data.data : null;
  $: {
    if (player !== null) {
      let playerDataFromState = $playerState.playersDiscovered.find(
        (p) => p.id == player.id && p.role !== undefined
      );

      if (playerDataFromState) {
        player.role = playerDataFromState.role;
      } else {
        player.role = "player";
      }
    }
  }

  function nightOutcomeConfirm() {
    sendMessage({
      action: "nightOutcomeConfirm",
      data: {},
    });
  }
</script>

<div class="game space-between">
  <GameScreenHeader header={"Day #" + $playerState.cycle} />
  <div class="outcome">
    {#if player !== null}
      <BigRole roleName={player.role} showHeader={player.role !== "player"} />
    {/if}
    <div class="username-and-desc">
      {#if player !== null}
        <h1 class="username">{player.username}</h1>
      {:else}
        <h1>No one</h1>
      {/if}
      <div class="event-small-desc center">has died.</div>
    </div>
  </div>
  {#if $playerState.role === "moderator"}
    <button class="main-button" on:click={nightOutcomeConfirm}>Continue</button>
  {/if}
</div>

<style>
  .outcome {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;

    gap: 1.5em;
  }

  .username-and-desc {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;

    gap: 0.2em;
  }

  .center {
    justify-content: center;
    text-align: center;
  }
</style>
