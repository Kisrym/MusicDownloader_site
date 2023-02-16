const trocar = document.querySelector("#trocar");
const submit = document.querySelector("input[type='submit'");
const logo = document.querySelector(".downloader-img");
const span = document.querySelector(".downloader-span");
trocar.addEventListener("click", () => {
    trocar.classList.toggle("youtubeButton");
    trocar.classList.toggle("spotifyButton");

    submit.classList.toggle("youtubeButton");
    submit.classList.toggle("spotifyButton");
    
    logo.classList.toggle("spotify")
    logo.classList.toggle("youtube")

    if(logo.className == "downloader-img youtube"){
        logo.src = "static/img/youtube.png";
        span.innerHTML = "Youtube downloader"
    } else {
        logo.src = "static/img/spotify.png";
        span.innerHTML = "Spotify downloader"
    }
})