// const videos = [
//     {
//         title: 'How to Install Visual Studio Code on Windows 11 (VS Code) (2024)',
//         src: './Youtube-Clone/videos/How Install Visual Studio Code on Windows 11 (VS Code) (2024).mp4',
//         thumbnail: './Youtube-Clone/thumbnails/vscode.jpeg',
//     },
//     // You can add more videos here if needed
// ];

const videoContainer = document.getElementById('video-container');

function loadVideos() {
    videos.forEach(video => {
        const videoElement = document.createElement('div');
        videoElement.className = 'video';
        videoElement.innerHTML = `
            <img src="${video.thumbnail}" alt="${video.title}" onclick="playVideo('${video.src}')">
            <h3>${video.title}</h3>
        `;
        videoContainer.appendChild(videoElement);
    });
}

function playVideo(src) {
    document.getElementById('video-source').src = src;
    document.getElementById('video-element').load();
    document.getElementById('video-player').style.display = 'block';
}

function closePlayer() {
    document.getElementById('video-player').style.display = 'none';
}

document.getElementById('search').addEventListener('input', function() {
    const query = this.value.toLowerCase();
    console.log("Search query:", query);  // 输出搜索查询
    const filteredVideos = videos.filter(video => video.title.toLowerCase().includes(query));
    videoContainer.innerHTML = '';
    filteredVideos.forEach(video => {
        const videoElement = document.createElement('div');
        videoElement.className = 'video';
        videoElement.innerHTML = `
            <img src="${video.thumbnail}" alt="${video.title}" onclick="playVideo('${video.src}')">
            <h3>${video.title}</h3>
        `;
        videoContainer.appendChild(videoElement);
    });
});

window.onload = loadVideos;
