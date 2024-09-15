<script lang="ts">
  import { afterUpdate } from "svelte";
  import { playerState, sendMessage, view } from "../../stores";
  import BigIcon from "../components/BigIcon.svelte";
  import PlayerList from "../components/PlayerList.svelte";
  import Timer from "../components/Timer.svelte";

  let timer: Timer;

  function extend() {
    sendMessage({
      action: "extendDiscussion",
      data: {},
    });
  }

  function skip() {
    timer.skipTimer();
  }

  function continueEvent() {
    sendMessage({
      action: "endDiscussion",
      data: {},
    });
  }
</script>

<div class="game space-between">
  <BigIcon name="sunny" color="var(--main2)" />
  <div class="header-and-timer">
    <h1 class="header">Discussion</h1>
    <Timer bind:this={timer} />
  </div>
  <PlayerList players={$view.data.data.players} />
  {#if $playerState.role === "moderator"}
    <div class="buttons">
      {#if $view.data.mode === "ongoing"}
        <button class="main-button" on:click={extend}>+2 min</button>
        <button class="main-button" on:click={skip}>Skip</button>
      {:else if $view.data.mode === "finished"}
        <button class="main-button" on:click={continueEvent}>Continue</button>
      {/if}
    </div>
  {/if}
</div>

<style>
  .header-and-timer {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
  }

  .header {
    font-size: clamp(1.8rem, 10vw, 3rem);
    margin: 0;
    margin-bottom: -0.7em;
  }

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
