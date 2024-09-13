<script lang="ts">
  import { sendMessage, view, type Player } from "../../stores";
  import BigRole from "../components/BigRole.svelte";
  import PlayerList from "../components/PlayerList.svelte";

  export let roleName: string;
  export let players: Player[];
  export let onClickMessage: string =
    "start" + $view.view.charAt(0).toUpperCase() + $view.view.slice(1);
  export let waitMessage: string | null = null;

  function wakeUp() {
    sendMessage({
      action: onClickMessage,
      data: {},
    });
  }

  $: everyoneDead = players.every((player: Player) => !player.alive);
</script>

<div class="wake-up">
  <BigRole {roleName} />
  <PlayerList {players} />
  {#if everyoneDead}
    <div class="additional-info">
      The {players.length > 1 ? "players are" : "player is"} dead, so you have to
      fake it like they are alive. <br /><br />Pretend to wake them up, wait for
      the answer, put them back to sleep and press continue.
    </div>
  {/if}
  {#if waitMessage === null}
    <button class="main-button" on:click={wakeUp}>
      {everyoneDead ? "Continue" : "Wake up!"}
    </button>
  {:else}
    <div class="info-text">{waitMessage}</div>
  {/if}
</div>

<style>
  .wake-up {
    flex-grow: 1;
    flex-shrink: 1;

    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    gap: 1.5em;
    min-height: 2em;
  }
</style>
