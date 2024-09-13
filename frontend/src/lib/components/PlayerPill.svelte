<script lang="ts">
  import { playerState, type Player } from "../../stores";
  import { roles } from "../../roles";
  import Icon from "../icons/Icon.svelte";

  export let player: Player;

  $: {
    if (player.role === undefined) {
      let playerDataFromState = $playerState.playersDiscovered.find(
        (p) => p.id == player.id && p.role !== undefined
      );

      if (playerDataFromState) {
        player.role = playerDataFromState.role;
      }
    }
  }

  const alive = player.alive !== undefined ? player.alive : true;

  $: color =
    player.id === $playerState.id ? "var(--main3)" : "var(--background)";

  $: playerDataClass = alive ? "player-data" : "player-data dead";
</script>

<div class="pill">
  <div class={playerDataClass} style:color>
    <Icon
      name={player.role === undefined
        ? roles["player"].icon
        : roles[player.role].icon}
    />
    <span class="username">
      {player.username}
    </span>
  </div>
  <div class="extra">
    <slot />
  </div>
</div>

<style>
  .player-data,
  .extra {
    display: flex;
    align-items: center;

    gap: 0.6em;
  }

  .dead {
    opacity: 50%;
  }

  .player-data {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;

    width: calc(fit-content);
  }

  .username {
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;

    width: calc(fit-content);
  }

  .pill {
    display: flex;
    justify-content: space-between;
    align-items: center;

    gap: 0.8em;

    padding: 0.5em 0.8em;

    width: 100%;

    background-color: var(--main2);
    border-radius: 2rem;
    border: none;

    font-family: "Kanit", sans-serif;
    font-weight: 400;
    font-size: 1.3em;

    color: var(--main3);
  }
</style>
