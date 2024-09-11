<div class="container">
  <div class="loader"></div>
  Loading...
</div>

<style>
  .container {
    flex-grow: 1;

    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;

    gap: 1rem;

    color: var(--main2);
  }

  .loader {
    width: 32px;
    aspect-ratio: 1;
    --_g: no-repeat radial-gradient(farthest-side, #6d5d6e 90%, #0000);
    background: var(--_g), var(--_g), var(--_g), var(--_g);
    background-size: 40% 40%;
    animation: l46 1s infinite;
  }

  @keyframes l46 {
    0% {
      background-position:
        0 0,
        100% 0,
        100% 100%,
        0 100%;
    }
    40%,
    50% {
      background-position:
        100% 100%,
        100% 0,
        0 0,
        0 100%;
    }
    90%,
    100% {
      background-position:
        100% 100%,
        0 100%,
        0 0,
        100% 0;
    }
  }
</style>
