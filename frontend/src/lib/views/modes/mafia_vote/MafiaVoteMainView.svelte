<script lang="ts">
  import { sendMessage, view } from "../../../../stores";
  import MafiaVoteMafiaPill from "../../../components/modes/mafia_vote/MafiaVoteMafiaPill.svelte";
  import MafiaVoteModeratorPill from "../../../components/modes/mafia_vote/MafiaVoteModeratorPill.svelte";
  import PlayerList from "../../../components/PlayerList.svelte";

  function toggleConfirm() {
    if ($view.data.data.confirmed) {
      sendMessage({
        action: "mafiaCancel",
        data: {},
      });
    } else {
      sendMessage({
        action: "mafiaConfirm",
        data: {},
      });
    }
  }
</script>

{#if $view.data.mode === "moderatorWait"}
  <PlayerList players={$view.data.data.votes} extra={MafiaVoteModeratorPill} />
{:else if $view.data.mode === "vote"}
  <PlayerList players={$view.data.data.votes} extra={MafiaVoteMafiaPill} />
{/if}

{#if $view.data.mode === "moderatorWait"}
  <div class="info-text">Wait for the mafia to pick someone to kill.</div>
{:else if $view.data.mode === "vote"}
  <button class="main-button" on:click={toggleConfirm}
    >{$view.data.data.confirmed ? "Cancel" : "Confirm"}</button
  >
{/if}
