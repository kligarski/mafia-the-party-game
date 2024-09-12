export type Role = {
  name: string,
  description: string,
  icon: string,
  color: string;
}

export const roles: any = {
  moderator: {
    name: "Moderator",
    description: "The Moderator oversees the game, manages the game's night and day phases without participating as a player.",
    icon: "build",
    color: "inherit"
  }, 

  mafia: {
    name: "Mafia",
    description: "Mafia's goal is to kill regular citizens. Mafia wins, if there are at least as many mafiosi as citizens left in the city.",
    icon: "domino_mask",
    color: "var(--red)"
  }, 

  villager: {
    name: "Villager",
    description: "Villagers' goal is to eliminate the mafia. Villagers win, if there are no mafiosi left in the city.",
    icon: "person",
    color: "var(--green)"
  }, 

  protector: {
    name: "Protector",
    description: "Every night, Protector can choose one person that will be saved from death.",
    icon: "shield",
    color: "var(--blue)"
  }, 

  seer: {
    name: "Seer",
    description: "Every night, Seer can learn one person's team.",
    icon: "visibility",
    color: "var(--yellow)"
  }
}