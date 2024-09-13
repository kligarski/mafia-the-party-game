<script lang="ts">
  import { roles } from "../../roles";
  import { playerState, view } from "../../stores";
  import { seerPickModes } from "../../viewsMapping";
  import GameScreenHeader from "../components/GameScreenHeader.svelte";
  import Icon from "../icons/Icon.svelte";
  import Error from "./Error.svelte";
</script>

<div class="game">
  {#if $view.data.mode !== "pick" && $view.data.mode !== "result"}
    <GameScreenHeader header={"Night #" + $playerState.cycle} />
  {:else}
    <div class="header-box">
      <GameScreenHeader header={"Night #" + $playerState.cycle}>
        <div class="seer-icon">
          <Icon name={roles.seer.icon} />
        </div>
      </GameScreenHeader>
      {#if $view.data.mode === "pick"}
        <div class="event-small-desc">
          As a seer, you have to choose one person to investigate and learn
          their true role.
        </div>
      {/if}
    </div>
  {/if}
  {#if $view.data.mode in seerPickModes}
    <svelte:component this={seerPickModes[$view.data.mode]} />
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

  .seer-icon {
    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 2.5em;
    color: var(--yellow);
  }
</style>
