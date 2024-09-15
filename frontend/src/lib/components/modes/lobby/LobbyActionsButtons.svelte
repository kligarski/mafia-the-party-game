<script lang="ts">
  import { playerState, sendMessage } from "../../../../stores";
  import Icon from "../../../icons/Icon.svelte";

  export let playerId: number;

  function makeModerator() {
    sendMessage({
      action: "makeModerator",
      data: {
        id: playerId,
      },
    });
  }

  function kickPlayer() {
    sendMessage({
      action: "kickPlayer",
      data: {
        id: playerId,
      },
    });
  }
</script>

{#if $playerState.role === "moderator" && playerId !== $playerState.id}
  <div class="buttons">
    <button
      class="circular-button green"
      aria-label="Make moderator"
      on:click={makeModerator}
    >
      <Icon name="build" />
    </button>

    <button
      class="circular-button red"
      aria-label="Kick player"
      on:click={kickPlayer}
    >
      <Icon name="person_remove" />
    </button>
  </div>
{/if}

<style>
  .buttons {
    display: flex;
    gap: 0.4em;
    justify-content: center;
    align-items: center;
  }

  .circular-button {
    aspect-ratio: 1;

    border: none;
    border-radius: 50%;

    font-size: 1em;

    display: flex;
    justify-content: center;
    align-items: center;

    color: var(--background);
  }

  .circular-button:focus-visible {
    outline: 0.1rem solid var(--background);
    outline-offset: 0.1rem;
  }

  .red {
    background-color: var(--red);
  }

  .red:hover {
    background-color: var(--red-hover);
  }

  .red:active {
    background-color: var(--red-active);
  }

  .red:focus-visible {
    outline-color: var(--red);
  }

  .green {
    background-color: var(--green);
  }

  .green:hover {
    background-color: var(--green-hover);
  }

  .green:active {
    background-color: var(--green-active);
  }

  .green:focus-visible {
    outline-color: var(--green);
  }
</style>
