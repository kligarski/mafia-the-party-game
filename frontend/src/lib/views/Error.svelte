<script type="ts">
  // TODO: for development
  import { view, playerState } from "../../stores";
</script>

<div class="outer">
  <div class="content">
    <h1>Error</h1>
    <slot>Unknown view.</slot>
    <p>{JSON.stringify($view, null, 2)}</p>
    <p>{JSON.stringify($playerState, null, 2)}</p>
  </div>
</div>

<style>
  .outer {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .content {
    width: 100%;
  }

  h1 {
    color: var(--red);
  }
</style>
