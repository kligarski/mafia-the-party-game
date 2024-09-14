<script lang="ts">
  import { onDestroy, onMount } from "svelte";
  import { playerState, sendMessage, view } from "../../stores";

  // import { afterUpdate, onDestroy, onMount } from "svelte";
  // import { view, playerState, sendMessage } from "../../stores";

  console.log($view);

  // let secondsRemaining: number;
  // let interval: number | undefined = 5 * 60;

  // $: minutes = Math.floor(secondsRemaining / 60)
  //   .toString()
  //   .padStart(2, "0");

  // $: seconds = Math.floor(secondsRemaining % 60)
  //   .toString()
  //   .padStart(2, "0");

  // onMount(() => {
  //   console.log("ok");
  //   interval = setInterval(() => {
  //     console.log(secondsRemaining > 0);
  //     if (secondsRemaining > 0) {
  //       secondsRemaining -= 1;
  //     } else if ($playerState.role === "moderator") {
  //       skipTimer();
  //     }
  //   }, 1000);
  // });

  let interval: number | undefined = undefined;
  let minutes: string = "00";
  let seconds: string = "00";

  onMount(() => {
    if ($view.data.mode === "ongoing") {
      calculateTime();

      interval = setInterval(() => {
        if (calculateTime() <= 0) {
          if ($playerState.role === "moderator") {
            skipTimer();
          } else {
            disableInterval();
          }
        }
      }, 250);
    }
  });

  onDestroy(() => {
    disableInterval();
  });

  function calculateTime() {
    if ($view.data.mode === "ongoing") {
      let now = new Date();
      let end = new Date($view.data.data.endTime);

      let secondsRemaining: number = Math.floor(
        (end.getTime() - now.getTime()) / 1000
      );

      minutes = Math.floor(secondsRemaining / 60)
        .toString()
        .padStart(2, "0");

      seconds = Math.floor(secondsRemaining % 60)
        .toString()
        .padStart(2, "0");

      return secondsRemaining;
    } else {
      seconds = "00";
      minutes = "00";

      return 0;
    }
  }

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
      seconds = "00";
      minutes = "00";
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
