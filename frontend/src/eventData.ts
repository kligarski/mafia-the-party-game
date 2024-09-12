import RoleRevealModeratorInfo from "./lib/views/modes/role_reveal/RoleRevealModeratorInfo.svelte"

export const eventData: any = {
  roleRevealInfo: {
    icon: "person_search",
    header: "Role reveal",
    info: `Before the night starts, the roles will be revealed to every player, one-by-one, in random order.<br><br>Everyone has to claim that they're not in the mafia, no matter what their true role is.
    `,
    buttonAction: "startRoleReveal"
  }
}

export const roleRevealModes: any = {
  moderatorInfo: RoleRevealModeratorInfo,
  moderatorWait: null,
  playerReveal: null,
  playerWaitBefore: null,
  playerWaitAfter: null,
}