<script lang="ts">
  import { sendMessage, view } from "../../../../stores";
  import BigRole from "../../../components/BigRole.svelte";
  import PlayerList from "../../../components/PlayerList.svelte";

  function endEvent() {
    sendMessage({
      action: "seerConfirm",
      data: {},
    });
  }
</script>

<div class="result">
  <BigRole roleName={$view.data.data.pick.role} />
  <h1>{$view.data.data.pick.username}</h1>
  <button class="main-button" on:click={endEvent}>Continue</button>
</div>

<style>
  .result {
    flex-grow: 1;
    flex-shrink: 1;

    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    gap: 1.5em;
    min-height: 5em;
  }
</style>
