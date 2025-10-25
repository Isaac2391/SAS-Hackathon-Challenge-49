const activities = [
  {
    name: "Potluck",
    description: "Everyone brings a dish to share for a cozy evening in.",
    image: "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Eat_Alberta_Potluck_%287072671637%29.jpg/1200px-Eat_Alberta_Potluck_%287072671637%29.jpg",
    tags: ["Social", "cheap", "Casual"]
  },
  {
    name: "Karaoke Kingdom",
    description: "Sing your heart out with friends at this fun karaoke spot!",
    image: "https://images.unsplash.com/photo-1556745753-b2904692b3cd",
    tags: ["karaoke", "fun", "group"]
  },

  {
    name: "Quiz & Sip",
    description: "Trivia night every Thursday — test your smarts over pints!",
    image: "https://thebigfatquiz.com/wp-content/uploads/2021/06/Quiz_Night-41-1024x602.jpeg",
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
