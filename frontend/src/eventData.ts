export const eventData: any = {
  roleRevealInfo: {
    icon: "person_search",
    header: "Role reveal",
    addCycleNumber: false,
    info: "Before the night starts, the roles will be revealed to every player, one-by-one, in random order.<br><br>Everyone has to claim that they're not in the mafia, no matter what their true role is.",
    buttonAction: "startRoleReveal",
  },

  nightInfo: {
    icon: "bedtime",
    header: "Night",
    addCycleNumber: true,
    info: "The night is the time when the hidden roles come into play.<br><br>Members of each role will be woken up by the moderator.<br><br>For now, <b>sleep tight and don't let the bedbugs bite!</b>",
    buttonAction: "startNight",
  },

  dayInfo: {
    icon: "sunny",
    header: "Day",
    addCycleNumber: true,
    info: "Good morning!<br><br>It's time to check if everyone survived this night.",
    moderatorInfo: "Wake the players up.",
    buttonAction: "startDay",
  },

  discussionInfo: {
    icon: "sunny",
    header: "Day",
    addCycleNumber: true,
    info: "The day is the time when the players can share their suspicions, accusations, and evidence with each other. <br><br>After the 5 minute discussion, the vote will begin. The vote's goal is to eliminate one player who is suspected of being a mafia member.",
    buttonAction: "startDiscussion"
  },

  dayVoteInfo: {
    icon: "how_to_vote",
    header: "Vote",
    addCycleNumber: true,
    info: "Now it's time to vote. Every player, one-by-one, in random order will have to pick a person they suspect of being in the mafia or skip the vote.<br><br>If someone gets at least half of the votes, they are eliminated. If there is a tie, no one is eliminated.",
    buttonAction: "startDayVote"
  },
}