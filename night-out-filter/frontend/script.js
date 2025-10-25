const activities = [
  {
    name: "The Tipsy Goat",
    description: "A lively bar with cheap cocktails and great music.",
    image: "https://images.unsplash.com/photo-1504674900247-0877df9cc836",
    tags: ["bar", "cheap", "lively"]
  },
  {
    name: "Karaoke Kingdom",
    description: "Sing your heart out with friends at this fun karaoke spot!",
    image: "https://images.unsplash.com/photo-1556745753-b2904692b3cd",
    tags: ["karaoke", "fun", "group"]
  },
  {
    name: "Zen Lounge",
    description: "A chill cocktail lounge for relaxed vibes and fancy drinks.",
    image: "https://images.unsplash.com/photo-1551024601-bec78aea704b",
    tags: ["cocktail", "fancy", "chill"]
  },
  {
    name: "Quiz & Sip",
    description: "Trivia night every Thursday — test your smarts over pints!",
    image: "https://images.unsplash.com/photo-1601933470928-c0b8e17e3b5b",
    tags: ["quiz", "fun", "pub"]
  }
];

let current = 0;
const likes = [];
const dislikes = [];

const cardContainer = document.getElementById("card-container");

function showCard(index) {
  if (index >= activities.length) {
    showResults();
    return;
  }

  const activity = activities[index];
  cardContainer.innerHTML = `
    <div class="card">
      <img src="${activity.image}" alt="${activity.name}">
      <h2>${activity.name}</h2>
      <p>${activity.description}</p>
    </div>
  `;
}

function showResults() {
  cardContainer.innerHTML = `
    <div class="card">
      <h2>Your Top Picks</h2>
      <p>👍 ${likes.length} liked activities</p>
      <p>👎 ${dislikes.length} skipped</p>
      <p>Reload the page to try again!</p>
    </div>
  `;
  document.querySelector(".buttons").style.display = "none";
}

document.getElementById("like").addEventListener("click", () => {
  likes.push(activities[current]);
  current++;
  showCard(current);
});

document.getElementById("dislike").addEventListener("click", () => {
  dislikes.push(activities[current]);
  current++;
  showCard(current);
});

showCard(current);
