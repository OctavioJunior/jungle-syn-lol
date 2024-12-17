export const championService = {
  async fetchChampionSynergy(championName) {
    try {
      const response = await fetch("http://localhost:8000/synergy", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ champion_name: championName.trim() }),
      });

      const data = await response.json();

      if (response.ok) {
        return Object.keys(data.synergies).map((key) => ({
          name: key,
          winRate: parseFloat(data.synergies[key]),
        }));
      } else {
        throw new Error(data.message || "Erro ao buscar os dados");
      }
    } catch (err) {
      throw new Error("Erro de rede, tente novamente mais tarde.");
    }
  }
};