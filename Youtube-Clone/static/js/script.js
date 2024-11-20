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

function playVideo(videoId) {
    // 构建视频播放页面的URL，这里假设视频播放页面名为video-player.html
    var videoUrl = 'video-player.html?videoId=' + videoId;
    window.location.href = videoUrl;
}

document.addEventListener('DOMContentLoaded', function() {
    const videoPlayer = document.getElementById('video-player');
    const videoId = new URLSearchParams(window.location.search).get('videoId');
    const videoTitle = document.getElementById('video-title');
    const videoAuthor = document.getElementById('video-author');
    const videoViews = document.getElementById('video-views');
    const likeButton = document.getElementById('like-button');

    // 假设我们有一个API可以获取视频详情
    // 这里我们使用静态数据来模拟
    const videoDetails = {
        title: 'How to Install Visual Studio Code on Windows 11 (VS Code) (2024)',
        author: 'Channel 1',
        views: '10M'
    };

    videoTitle.textContent = videoDetails.title;
    videoAuthor.textContent = videoDetails.author;
    videoViews.textContent = videoDetails.views;

    // 设置视频源
    videoPlayer.children[0].src = 'path_to_your_video/' + videoId + '.mp4';

    // 点赞按钮逻辑

    if (likeButton) {
        likeButton.addEventListener('click', function() {
            this.classList.toggle('liked'); // 切换 liked 类
        });
    }
    
});

window.onload = loadVideos;
