<script lang="ts">
  import { gameCode } from "../../stores";
  import Icon from "../icons/Icon.svelte";

  let pill: HTMLButtonElement;

  async function copyGameCode(event: MouseEvent) {
    navigator.clipboard.writeText($gameCode);

    pill.style.animationPlayState = "running";
    await new Promise((res) => setTimeout(res, 700));
    pill.style.animationPlayState = "paused";
    pill.style.animationName =
      pill.style.animationName === "copy1" ? "copy2" : "copy1";
  }
</script>

<button class="pill" on:click={copyGameCode} bind:this={pill}>
  <div class="code">{$gameCode}</div>
  <Icon name="content_copy" />
</button>

<style>
  .pill {
    display: flex;
    justify-content: space-between;
    align-items: center;

    gap: 0.8em;

    margin: 0.4rem;
    padding: 0.4em 1em;

    background-color: var(--main1);
    border-radius: 2rem;
    border: none;

    cursor: pointer;

    font-family: "Kanit", sans-serif;
    font-weight: 400;
    font-size: 1em;

    color: var(--main3);

    animation-name: copy1;
    animation-duration: 0.7s;
    animation-play-state: paused;
    animation-iteration-count: infinite;
    animation-timing-function: ease-out;
  }

  .pill:hover {
    background-color: var(--main2-hover);
  }

  .pill:active {
    background-color: var(--main2);
  }

  .pill:focus-visible {
    outline: 0.1rem solid var(--main3);
    outline-offset: 0.1rem;
  }

  @keyframes -global-copy1 {
    0% {
      color: var(--main3);
    }

    50% {
      color: var(--green);
    }

    100% {
      color: var(--main3);
    }
  }

  @keyframes -global-copy2 {
    0% {
      color: var(--main3);
    }

    50% {
      color: var(--green);
    }

    100% {
      color: var(--main3);
    }
  }
</style>
