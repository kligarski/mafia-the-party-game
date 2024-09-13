<script lang="ts">
  import { view, playerState, sendMessage } from "../../../../stores";
  import BigRole from "../../../components/BigRole.svelte";

  function revealToPlayer() {
    sendMessage({
      action: "revealToPlayer",
      data: {},
    });
  }

  function revealContinue() {
    sendMessage({
      action: "revealContinue",
      data: {},
    });
  }
</script>

<div class="content">
  <BigRole roleName={$view.data.data.role} description={true} />
  {#if $view.data.mode === "moderatorInfo" || $view.data.mode === "moderatorWait"}
    <h1>{$view.data.data.username}</h1>
  {:else}
    <div class="additional-info">
      Don't tell the city anything except that you're not part of the mafia.
    </div>
  {/if}
  {#if $view.data.mode === "moderatorInfo"}
    <button class="main-button" on:click={revealToPlayer}
      >Reveal to the player</button
    >
  {:else if $view.data.mode === "moderatorWait"}
    <div class="info-text">Wait for the player to reveal themselves.</div>
  {:else if $view.data.mode === "playerReveal"}
    <button class="main-button" on:click={revealContinue}>Continue</button>
  {/if}
</div>

<style>
  .content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
  }
</style>
