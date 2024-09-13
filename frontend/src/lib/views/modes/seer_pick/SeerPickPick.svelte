<script lang="ts">
  import { view } from "../../../../stores";
  import SeerPickPill from "../../../components/modes/seer_pick/SeerPickPill.svelte";
  import PlayerList from "../../../components/PlayerList.svelte";
</script>

<PlayerList players={$view.data.data.players} extra={SeerPickPill} />
