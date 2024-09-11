<script lang="ts">
  import { view, playerState, sendMessage } from "../../stores";
  import { eventData } from "../../eventData";
  import Icon from "../icons/Icon.svelte";

  const { icon, header, info, buttonAction } = eventData[$view.data.mode];

  function continueEvent() {
    sendMessage({
      action: buttonAction,
      data: {},
    });
  }
</script>

<div class="game space-between">
  <div class="content">
    <div class="icon-box">
      <Icon name={icon} />
    </div>
    <h1 class="header">{header}</h1>
    <div class="info">
      {@html info}
    </div>
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

  .icon-box {
    flex-shrink: 1;
    font-size: min(8em, 20vh);
    color: var(--main2);
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .info {
    font-style: italic;
    padding: 0 2em;
    text-align: center;
    overflow-y: auto;
    min-height: 3em;
  }
</style>
