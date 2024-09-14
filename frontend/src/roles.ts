export type Role = {
  name: string,
  description: string,
  icon: string,
  color: string;
}

export const teams: any = {
  players: {
    name: "Players",
    icon: "person",
    color: "var(--background)",
  },

  village: {
    name: "Village",
    icon: "person",
    color: "var(--green)",
  },

  mafia: {
    name: "Mafia",
    icon: "domino_mask",
    color: "var(--red)",
  }
}

export const roles: any = {
  player: {
    name: "Player",
    description: "The Player.",
    icon: "person",
    color: "var(--background)",
    team: "players",
  },

  moderator: {
    name: "Moderator",
    description: "The Moderator oversees the game, manages the game's night and day phases without participating as a player.",
    icon: "build",
    color: "var(--background)",
    team: "players",
  }, 

  mafia: {
    name: "Mafia",
    description: "Mafia's goal is to kill regular citizens. Mafia wins, if there are at least as many mafiosi as citizens left in the city.",
    icon: "domino_mask",
    color: "var(--red)",
    team: "mafia",
  }, 

  villager: {
    name: "Villager",
    description: "Villagers' goal is to eliminate the mafia. Villagers win, if there are no mafiosi left in the city.",
    icon: "person",
    color: "var(--green)",
    team: "village",
  }, 

  protector: {
    name: "Protector",
    description: "Every night, Protector can choose one person that will be saved from death.",
    icon: "shield",
    color: "var(--blue)",
    team: "village",
  }, 

  seer: {
    name: "Seer",
    description: "Every night, Seer can learn one person's team.",
    icon: "visibility",
    color: "var(--yellow)",
    team: "village",
  }
}