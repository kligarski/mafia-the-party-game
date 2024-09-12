<div class="sm-pill">
  <slot />
</div>

<style>
  .sm-pill {
    display: flex;
    justify-content: space-between;
    align-items: center;

    gap: 0.8em;

    padding: 0.2em 0.7em;

    background-color: var(--main2);
    border-radius: 2rem;
    border: none;

    cursor: pointer;

    font-family: "Kanit", sans-serif;
    font-weight: 400;
    font-size: 1em;

    color: var(--main3);
  }
</style>
