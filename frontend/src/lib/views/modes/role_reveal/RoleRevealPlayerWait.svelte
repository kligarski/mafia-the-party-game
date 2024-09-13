<script lang="ts">
  import { view } from "../../../../stores";
  import BigInfo from "../../../components/BigInfo.svelte";

  $: before = $view.data.mode === "playerWaitBefore";
</script>

{#if before}
  <BigInfo message="Wait for your role to be revealed." />
{:else}
  <BigInfo message="Wait for the role reveal to end." />
{/if}
