<script lang="ts">
  import { view } from "../../../../stores";
  import WakeUp from "../../../components/WakeUp.svelte";

  $: players = $view.data.data.mafia;
</script>

<WakeUp roleName="mafia" {players} />
