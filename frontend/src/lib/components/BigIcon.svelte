<script lang="ts">
  import Icon from "../icons/Icon.svelte";

  export let name: string;
  export let color: string = "inherit";
</script>

<div class="icon-box" style:color>
  <Icon {name} />
</div>

<style>
  .icon-box {
    font-size: min(8em, 15vh);
    display: flex;
    justify-content: center;
    align-items: center;
  }
</style>
