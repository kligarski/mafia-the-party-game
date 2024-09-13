<script lang="ts">
  import { view } from "../../../../stores";
  import Result from "../../../components/Result.svelte";

  $: players = [$view.data.data.seer];
</script>

<Result roleName="seer" {players} />
