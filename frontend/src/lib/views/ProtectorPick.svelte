<script lang="ts">
  import { playerState, view } from "../../stores";
  import { protectorPickModes } from "../../viewsMapping";
  import GameScreenHeader from "../components/GameScreenHeader.svelte";
  import Icon from "../icons/Icon.svelte";
  import Error from "./Error.svelte";
</script>

<div class="game">
  {#if $view.data.mode === "moderatorInfo" || $view.data.mode === "moderatorResult"}
    <GameScreenHeader header={"Night #" + $playerState.cycle} />
  {:else}
    <div class="header-box">
      <GameScreenHeader header={"Night #" + $playerState.cycle}>
        <div class="protector-icon">
          <Icon name="shield" />
        </div>
      </GameScreenHeader>
      {#if $view.data.mode === "pick"}
        <div class="event-small-desc">
          As a protector, you have to choose one person to be protected this
          night.
        </div>
      {/if}
    </div>
  {/if}
  {#if $view.data.mode in protectorPickModes}
    <svelte:component this={protectorPickModes[$view.data.mode]} />
  {:else}
    <Error>Unknown mode.</Error>
  {/if}
</div>

<style>
  .header-box {
    width: 100%;

    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .protector-icon {
    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 2.5em;
    color: var(--blue);
  }
</style>
