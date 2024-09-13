<script lang="ts">
  export let message: string;
</script>

<div>
  {message}
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
