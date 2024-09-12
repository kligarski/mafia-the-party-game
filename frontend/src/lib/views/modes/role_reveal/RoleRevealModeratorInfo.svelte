<script lang="ts">
  import { view } from "../../../../stores";
  import BigRole from "../../../components/BigRole.svelte";
</script>

<div class="content">
  <BigRole roleName={$view.data.data.role} description={true} />
  <h1>{$view.data.data.username}</h1>
  <button class="main-button">Reveal to the player</button>
</div>

<style>
  .content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
  }
</style>
