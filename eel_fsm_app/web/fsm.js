
let currentState = "splash";

const states = ["splash", "search", "result", "playback"];

function switchState(target) {
  if (!states.includes(target)) return;

  states.forEach(state => {
    document.getElementById(state).classList.add("hidden");
  });

  document.getElementById(target).classList.remove("hidden");
  currentState = target;
}

setTimeout(() => switchState("search"), 1000); // splash to search

function goToResult() {
  switchState("result");
}

function goToPlayback() {
  switchState("playback");
}

function goBack() {
  if (currentState === "playback") switchState("result");
  else if (currentState === "result") switchState("search");
}

async function executeSearch() {
  const search_query = document.getElementById("search_text").value;
  const data = await eel.search_backend(search_query)();
  renderResults(data)
  switchState("result");
}

function playVideo() {
  goToPlayback();
}

function renderResults(data) {
  const container = document.querySelector(".result-list");
  container.innerHTML = ""; // Clear previous content

  data.forEach((item, index) => {
    const div = document.createElement("div");
    div.innerHTML = `
      <span>${item.name}</span>
      <button data-video="${item.video}" class="video">Play Video</button>
    `;
    container.appendChild(div);
  });

  container.querySelectorAll(".video").forEach(btn =>
    btn.addEventListener("click", e => {
      const videoUrl = e.target.dataset.video;
      console.log("Playing video:", videoUrl);
      // store or pass videoUrl for playback use
      showVideo(videoUrl);
    })
  );
}


async function showVideo(videoUrl) {
  //Use the eel function to download the vid and get the filepath back
  const pathToVideo = await eel.get_video(videoUrl)();
  const player = document.querySelector(".video-player");
  const fullPath = 'temp/' + pathToVideo
  player.innerHTML = `
    <video width="100%" controls autoplay>
      <source src="${fullPath}" type="video/mp4">
      Your browser does not support the video tag.
    </video>
  `;
  switchState("playback");
}



