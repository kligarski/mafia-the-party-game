<script lang="ts">
  import { teams } from "../../../../roles";
  import BigIcon from "../../BigIcon.svelte";

  export let teamName: string;

  $: team = teamName in teams ? teams[teamName] : teams["players"];
</script>

<div class="big-team" style:color={team.color}>
  <BigIcon name={team.icon} />
  <div class="team-header">{team.name + " wins!"}</div>
</div>

<style>
  .big-team {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1em;
  }

  .team-header {
    font-family: "Playfair Display", serif;
    font-size: clamp(2.5rem, 8vw, 4rem);
    font-weight: 700;
    margin-top: -0.5em;
    margin-bottom: -0.2em;
    text-align: center;
  }
</style>
