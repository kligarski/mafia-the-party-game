<script lang="ts">
  import { getRoleOrTeamData, roles } from "../../roles";
  import type { Player } from "../../stores";
  import BigIcon from "./BigIcon.svelte";

  export let player: Player | null = null;
  export let roleName: string = "";
  export let description: boolean = false;
  export let pick: boolean = false;
  export let showHeader: boolean = true;

  let color: string = "";
  let icon: string = "";
  let header: string = "";
  let descriptionContent: string = "";

  $: {
    let roleOrTeam;
    if (player === null) {
      roleOrTeam = roleName in roles ? roles[roleName] : roles["player"];
    } else {
      roleOrTeam = getRoleOrTeamData(player);
      if (roleOrTeam.name === "Players") {
        showHeader = false;
      }
    }

    color = roleOrTeam.color;
    icon = roleOrTeam.icon;
    descriptionContent = roleOrTeam.description;
    header = pick ? roleOrTeam.name + "'s pick" : roleOrTeam.name;
  }
</script>

<div class="big-role" style:color>
  <BigIcon name={icon} />
  {#if showHeader}
    <div class="role-header">{header}</div>
  {/if}
  {#if description}
    <div class="description">
      {descriptionContent}
    </div>
  {/if}
</div>

<style>
  .big-role {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1em;
  }

  .role-header {
    font-family: "Playfair Display", serif;
    font-size: clamp(2.5rem, 8vw, 4rem);
    font-weight: 700;
    margin-top: -0.5em;
    margin-bottom: -0.2em;
    text-align: center;
  }

  .description {
    font-size: 0.9em;
    padding: 0 0.5em;
    max-width: 500px;
    text-align: center;
    color: var(--main3);
  }
</style>
