<script lang="ts">
  import { afterUpdate, onDestroy, onMount } from "svelte";
  import { view, playerState, sendMessage } from "../../stores";

  let secondsRemaining: number;
  let interval: number | undefined = 5 * 60;

  $: minutes = Math.floor(secondsRemaining / 60)
    .toString()
    .padStart(2, "0");

  $: seconds = Math.floor(secondsRemaining % 60)
    .toString()
    .padStart(2, "0");

  onMount(() => {
    console.log("ok");
    interval = setInterval(() => {
      console.log(secondsRemaining > 0);
      if (secondsRemaining > 0) {
        secondsRemaining -= 1;
      } else if ($playerState.role === "moderator") {
        skipTimer();
      }
    }, 1000);
  });

  export function setTimer(seconds: number) {
    secondsRemaining = seconds;
  }

  onDestroy(() => {
    disableInterval();
  });

  export function skipTimer() {
    disableInterval();
    sendMessage({
      action: "finishDiscussion",
      data: {},
    });
  }

  function disableInterval() {
    if (interval != undefined) {
      clearInterval(interval);
      interval = undefined;
      secondsRemaining = 0;
    }
  }
</script>

<div class="timer">
  {minutes}:{seconds}
</div>

<style>
  .timer {
    font-size: clamp(2.5rem, min(25vw, 10vh), 8rem);
    font-style: italic;
  }
</style>
