<script lang="ts">
  import { view } from "../../../../stores";
  import ProtectorPickPill from "../../../components/modes/protector_pick/ProtectorPickPill.svelte";
  import PlayerList from "../../../components/PlayerList.svelte";
</script>

<PlayerList players={$view.data.data.players} extra={ProtectorPickPill} />
