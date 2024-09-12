<script lang="ts">
  export let header: string = "";
</script>

<div class="game-header">
  <h1>{header}</h1>
  <slot />
</div>

<style>
  .game-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }
</style>
