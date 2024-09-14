<script lang="ts">
  import { view } from "../../../../stores";
  import Result from "../../../components/Result.svelte";

  $: players = [$view.data.data.pick];
</script>

<Result roleName="seer" {players} />
