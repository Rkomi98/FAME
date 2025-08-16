// Configuration for FAME Frontend
// Update this URL when deploying your backend

// For local development
// const BACKEND_URL = 'http://localhost:5000';

// For production (update with your actual backend URL)
const BACKEND_URL = 'https://fame-rkomi98.onrender.com';

// GitHub repository URL (update with your actual repo)
const GITHUB_REPO = 'https://github.com/rkomi98/FAME';

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { BACKEND_URL, GITHUB_REPO };
}
