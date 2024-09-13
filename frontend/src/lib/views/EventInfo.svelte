<script lang="ts">
  import { view, playerState, sendMessage } from "../../stores";
  import { eventData } from "../../eventData";
  import BigIcon from "../components/BigIcon.svelte";

  const { icon, header, addCycleNumber, info, moderatorInfo, buttonAction } =
    eventData[$view.data.mode];

  function continueEvent() {
    sendMessage({
      action: buttonAction,
      data: {},
    });
  }

  $: fullHeader = addCycleNumber ? header + " #" + $playerState.cycle : header;
</script>

<div class="game space-between">
  <div class="content">
    <BigIcon name={icon} color="var(--main2)" />
    <h1 class="header">{fullHeader}</h1>
    <div class="info">
      {@html info}
    </div>
    {#if moderatorInfo !== undefined && $playerState.role === "moderator"}
      <div class="additional-info">{moderatorInfo}</div>
    {/if}
  </div>
  {#if $playerState.role === "moderator"}
    <button class="main-button" on:click={continueEvent}>Continue</button>
  {/if}
</div>

<style>
  .content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 2em;
    min-height: 0;
  }

  .header {
    font-size: 2em;
  }

  .info {
    font-style: italic;
    padding: 0 2em;
    text-align: center;
    overflow-y: auto;
    min-height: 3em;
  }
</style>
