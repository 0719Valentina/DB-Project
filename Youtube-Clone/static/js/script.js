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

// 订阅按钮逻辑
function handleDelete() {
    const deleteBtn = document.getElementById('delete-btn');
    deleteBtn.addEventListener('click', function(event) {
        event.stopPropagation(); // 阻止事件冒泡
        // 切换文本和背景颜色
        this.textContent = this.textContent === '已订阅' ? 'Subscribe' : '已订阅';
        this.style.backgroundColor = this.style.backgroundColor === '#808080' ? '#00b1fd' : '#808080';
        this.disabled = false; // 启用按钮，允许重复点击
    });
}

// 点赞按钮逻辑
function handleLike() {
    const likeBtn = document.getElementById('like-btn');
    likeBtn.addEventListener('click', function(event) {
        event.stopPropagation(); // 阻止事件冒泡
        this.textContent = this.textContent === '已点赞' ? 'Like' : '已点赞';
        this.style.backgroundColor = this.style.backgroundColor === '#ff0000' ? '#c0c0c0' : '#ff0000';
        this.disabled = false; // 启用按钮，允许重复点击
    });
}

function onPlayerShow() {
    handleDelete();
    handleLike();
}

function playVideo(src, videoId) {
    document.getElementById('video-source').src = src;
    document.getElementById('video-element').load();
    //document.getElementById('video-title').textContent = title;
    //document.getElementById('author-name').textContent = author.name;
    document.getElementById('video-player').style.display = 'block';

    // 将 videoId 存储在隐藏的 input 中
    document.getElementById("current-video-id").value = videoId;

    console.log("Playing video with ID:", videoId);
    onPlayerShow(); // 显示播放器时，添加事件监听器
}

function closePlayer() {
    const videoElement = document.getElementById('video-element');
    // 暂停视频播放
    videoElement.pause();
    // 重置视频播放时间
    videoElement.currentTime = 0;
    // 隐藏视频播放器模态框
    document.getElementById('video-player').style.display = 'none';
    // 重新启用订阅和点赞按钮
    const deleteBtn = document.getElementById('delete-btn');
    const likeBtn = document.getElementById('like-btn');
    // 移除订阅和点赞按钮的事件监听器，避免重复添加
    deleteBtn.removeEventListener('click', handleSubscribe);
    likeBtn.removeEventListener('click', handleLike);
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

window.onload = function() {
    closePlayer();
};
