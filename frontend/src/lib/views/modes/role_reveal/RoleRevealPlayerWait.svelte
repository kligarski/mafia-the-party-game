<script lang="ts">
  import { roleRevealModes } from "../../../../eventData";
  import { view } from "../../../../stores";

  $: before = $view.data.mode === "playerWaitBefore";
</script>

<div>
  {#if before}
    Wait for your role to be revealed...
  {:else}
    Wait for the role reveal to end...
  {/if}
</div>

<style>
  div {
    flex-grow: 1;
    display: flex;
    justify-content: center;
    align-items: center;

    width: 100%;

    padding: 0 1em;

    font-size: clamp(2.5rem, 8vw, 4rem);
    font-style: italic;
    text-align: center;
  }
</style>
