<script lang="ts">
  import Icon from "../icons/Icon.svelte";

  export let count: number;
</script>

<div class="pill">
  <Icon name="group" />
  <div class="count">{count}</div>
</div>

<style>
  .pill {
    display: flex;
    justify-content: space-between;
    align-items: center;

    gap: 0.8em;

    margin: 0.4rem;
    padding: 0.4em 1em;
    padding-right: 1.1em;

    background-color: var(--main1);
    border-radius: 2rem;
    border: none;

    font-family: "Kanit", sans-serif;
    font-weight: 400;
    font-size: 1em;

    color: var(--main3);
  }
</style>
