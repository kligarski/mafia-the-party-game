<script lang="ts">
  import { roles } from "../../roles";
  import { playerState, view } from "../../stores";
  import { mafiaVoteModes } from "../../viewsMapping";
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
        <div class="mafia-icon">
          <Icon name={roles.mafia.icon} />
        </div>
      </GameScreenHeader>
      {#if $view.data.mode === "vote"}
        <div class="event-small-desc">
          As the mafia, you have to choose one person to be killed this night.
        </div>
      {/if}
    </div>
  {/if}
  {#if $view.data.mode in mafiaVoteModes}
    <svelte:component this={mafiaVoteModes[$view.data.mode]} />
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

  .mafia-icon {
    display: flex;
    justify-content: center;
    align-items: center;

    font-size: 2.5em;
    color: var(--red);
  }
</style>
