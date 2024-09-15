<script lang="ts">
  import { afterUpdate } from "svelte";
  import { tryDisconnect, view } from "../../stores";

  $: url =
    $view.data.path === undefined
      ? window.location.origin
      : window.location.origin + $view.data.path;

  afterUpdate(() => {
    tryDisconnect();
    window.location.replace(url);
  });
</script>

<div class="container">
  <span
    >If you are not getting redirected automatically, please click <a href={url}
      >here</a
    >.</span
  >
</div>

<style>
  .container {
    flex-grow: 1;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
</style>
