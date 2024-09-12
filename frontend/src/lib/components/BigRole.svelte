<script lang="ts">
  import { roles, type Role } from "../../roles";
  import BigIcon from "./BigIcon.svelte";

  export let roleName: string;
  export let description: boolean = false;
  export let pick: boolean = false;

  $: role = roleName in roles ? roles[roleName] : roles["villager"];
  $: header = pick ? role.name + "'s pick" : role.name;
</script>

<div class="big-role" style:color={role.color}>
  <BigIcon name={role.icon} />
  <div class="role-header">{header}</div>
  {#if description}
    <div class="description">
      {role.description}
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
  }

  .description {
    font-size: 0.9em;
    padding: 0 0.5em;
    max-width: 500px;
    text-align: center;
    color: var(--main3);
  }
</style>
