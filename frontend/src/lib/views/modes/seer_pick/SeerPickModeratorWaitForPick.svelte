<script lang="ts">
  import { view } from "../../../../stores";
  import WakeUp from "../../../components/WakeUp.svelte";

  $: players = [$view.data.data.seer];
</script>

<WakeUp
  roleName="seer"
  {players}
  waitMessage="Wait for the seer to pick someone."
/>
