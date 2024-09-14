<script lang="ts">
  import { view } from "../../stores";
  import GameEndBigTeam from "../components/modes/end/GameEndBigTeam.svelte";
  import PlayerList from "../components/PlayerList.svelte";

  $: teamName = $view.data.mode.slice(0, -4);
</script>

<div class="game space-between">
  <GameEndBigTeam {teamName} />
  <PlayerList players={$view.data.data.players} />
</div>

<style>
</style>
