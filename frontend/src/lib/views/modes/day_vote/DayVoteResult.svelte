<script>
  import { fillRoleTeamData } from "../../../../roles";
  import { playerState, sendMessage, view } from "../../../../stores";
  import BigRole from "../../../components/BigRole.svelte";

  $: player = $view.data.data.votedOut;
  $: {
    fillRoleTeamData(player, $playerState.playersDiscovered);
  }

  function endDayVote() {
    sendMessage({
      action: "endDayVote",
      data: {},
    });
  }
</script>

<div class="outcome">
  {#if player !== null}
    <BigRole {player} />
  {/if}
  <div class="username-and-desc">
    {#if player !== null}
      <h1 class="username">{player.username}</h1>
    {:else}
      <h1>No one</h1>
    {/if}
    <div class="event-small-desc center">has been voted out.</div>
  </div>
</div>
{#if $playerState.role === "moderator"}
  <button class="main-button" on:click={endDayVote}>Continue</button>
{/if}

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
