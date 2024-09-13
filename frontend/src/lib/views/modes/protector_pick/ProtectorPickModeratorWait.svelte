<script lang="ts">
  import { view } from "../../../../stores";
  import WakeUp from "../../../components/WakeUp.svelte";

  $: players = [$view.data.data.protector];
</script>

<WakeUp
  roleName="protector"
  {players}
  waitMessage="Wait for the protector to pick someone..."
/>
