<script lang="ts">
  import { view, playerState } from "../../stores";
  import { dayVoteModes } from "../../viewsMapping";
  import GameScreenHeader from "../components/GameScreenHeader.svelte";
  import SmallPill from "../components/SmallPill.svelte";
  import Error from "./Error.svelte";
</script>

<div class="game space-between">
  <div class="header-box">
    {#if $view.data.mode !== "result"}
      <GameScreenHeader header={"Vote #" + $playerState.cycle}>
        <SmallPill>
          {$view.data.data.progress}
        </SmallPill>
      </GameScreenHeader>
    {:else}
      <GameScreenHeader header={"Vote #" + $playerState.cycle} />
    {/if}
    {#if $view.data.mode === "playerVote"}
      <div class="event-small-desc">
        You have to pick one person you suspect of being a part of the mafia.
        You may also skip the vote. Other players will know about your choice.
      </div>
    {/if}
  </div>

  {#if $view.data.mode in dayVoteModes}
    <svelte:component this={dayVoteModes[$view.data.mode]} />
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
</style>
