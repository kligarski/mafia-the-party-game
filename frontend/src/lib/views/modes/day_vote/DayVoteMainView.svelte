<script lang="ts">
  import { view, sendMessage } from "../../../../stores";
  import DayVoteActivePill from "../../../components/modes/day_vote/DayVoteActivePill.svelte";
  import DayVotePassivePill from "../../../components/modes/day_vote/DayVotePassivePill.svelte";
  import PlayerList from "../../../components/PlayerList.svelte";

  function letPlayerVote() {
    sendMessage({
      action: "letPlayerVote",
      data: {},
    });
  }

  function dayVoteNext() {
    sendMessage({
      action: "dayVoteNext",
      data: {},
    });
  }

  function dayPlayerSkipVote() {
    sendMessage({
      action: "dayPlayerSkipVote",
      data: {},
    });
  }

  let bottomText: string = "";
  $: {
    switch ($view.data.mode) {
      case "moderatorInfo":
        bottomText = `<span class="player-name-day-vote">${$view.data.data.playerVoting.username}</span> is the next person to vote.`;
        break;

      case "playerWaitBefore":
        bottomText = "Wait for your time to vote.";
        break;

      case "playerWaitAfter":
        bottomText = "Wait for the vote to end.";
        break;

      case "moderatorWait":
      case "playerWaitSomebody":
        bottomText = `<span class="player-name-day-vote">${$view.data.data.playerVoting.username}</span> is currently voting.`;
        break;

      case "playerVote":
        bottomText = "";
        break;

      case "moderatorResult":
      case "playerWaitSomebodyResult":
        if ($view.data.data.choice !== null) {
          bottomText = `<span class="player-name-day-vote">${$view.data.data.playerVoting.username}</span> has voted for <span class="player-name-day-vote">${$view.data.data.choice.username}</span>.`;
        } else {
          bottomText = `<span class="player-name-day-vote">${$view.data.data.playerVoting.username}</span> has skipped the vote.`;
        }
        break;

      case "playerVoteResult":
        if ($view.data.data.choice !== null) {
          bottomText = `You have voted for <span class="player-name-day-vote">${$view.data.data.choice.username}</span>.`;
        } else {
          bottomText = `You have skipped the vote.`;
        }
        break;
    }
  }
</script>

<PlayerList
  players={$view.data.data.votes}
  extra={$view.data.mode === "playerVote"
    ? DayVoteActivePill
    : DayVotePassivePill}
/>

<div class="bottom-box">
  {#if bottomText !== ""}
    <span>
      {@html bottomText}
    </span>
  {/if}
  {#if $view.data.mode === "moderatorInfo" || $view.data.mode === "moderatorResult"}
    <button
      class="main-button"
      on:click={$view.data.mode === "moderatorInfo"
        ? letPlayerVote
        : dayVoteNext}>Continue</button
    >
  {:else if $view.data.mode === "playerVote"}
    <button class="main-button" on:click={dayPlayerSkipVote}>
      Skip the vote
    </button>
  {/if}
</div>

<style>
  .bottom-box {
    width: 100%;

    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;

    gap: 1em;
  }

  :global(.player-name-day-vote) {
    font-weight: 700;
    font-style: none;
  }
</style>
