// DOM Elements
const textInput = document.getElementById('textInput');
const voiceBtn = document.getElementById('voiceBtn');
const submitBtn = document.getElementById('submitBtn');
const resultDiv = document.getElementById('result');
const sentimentSpan = document.getElementById('sentiment');
const promptP = document.getElementById('prompt');
const canvasContainer = document.getElementById('canvasContainer');
const usedStyleSpan = document.getElementById('usedStyle');
const styleSelector = document.getElementById('styleSelector');
const loadingAnimation = document.getElementById('loadingAnimation');
const loadingStyle = document.getElementById('loadingStyle');

// New elements for enhanced features
const saveBtn = document.getElementById('saveBtn');
const shareBtn = document.getElementById('shareBtn');
const regenerateBtn = document.getElementById('regenerateBtn');

// State variables
let selectedStyle = 'realistic';
let currentArtwork = null;
let availableStyles = {};

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    console.log("📄 DOM loaded, initializing Enhanced MoodCanvas...");
    loadAvailableStyles();
    setupVoiceRecognition();
    setupEventListeners();
    setTimeout(initThreeJS, 100);
});

// Load available art styles from backend
async function loadAvailableStyles() {
    try {
        const response = await fetch("http://localhost:5000/styles");
        const data = await response.json();
        
        if (data.status === "success") {
            availableStyles = data.styles;
            renderStyleSelector();
            console.log("🎨 Loaded art styles:", Object.keys(availableStyles));
        }
    } catch (error) {
        console.error("❌ Failed to load styles:", error);
        // Fallback styles
        availableStyles = {
            "realistic": { "name": "Realistic", "icon": "📷" },
            "anime": { "name": "Anime", "icon": "🎌" },
            "abstract": { "name": "Abstract", "icon": "🎨" },
            "oil_painting": { "name": "Oil Painting", "icon": "🖼️" }
        };
        renderStyleSelector();
    }
}

// Render style selection buttons
function renderStyleSelector() {
    styleSelector.innerHTML = '';
    
    Object.entries(availableStyles).forEach(([styleKey, styleData]) => {
        const button = document.createElement('button');
        button.className = `style-btn p-3 rounded-lg border-2 transition duration-300 text-white ${
            styleKey === selectedStyle 
                ? 'border-yellow-400 bg-yellow-400 bg-opacity-20' 
                : 'border-white border-opacity-30 hover:border-yellow-400 hover:bg-white hover:bg-opacity-10'
        }`;
        
        button.innerHTML = `
            <div class="text-2xl mb-1">${styleData.icon}</div>
            <div class="text-sm font-semibold">${styleData.name}</div>
        `;
        
        button.onclick = () => selectStyle(styleKey);
        styleSelector.appendChild(button);
    });
}

// Select art style
function selectStyle(styleKey) {
    selectedStyle = styleKey;
    renderStyleSelector(); // Re-render to update selection
    console.log("🎨 Selected style:", styleKey);
}

// Setup voice recognition
function setupVoiceRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.onresult = (event) => {
            textInput.value = event.results[0][0].transcript;
        };
        recognition.onerror = (event) => {
            console.log('Speech recognition error:', event.error);
        };
        voiceBtn.addEventListener('click', () => {
            recognition.start();
        });
    } else {
        voiceBtn.disabled = true;
        voiceBtn.innerHTML = '<span class="text-sm">Voice Not Supported</span>';
    }
}

// Setup event listeners
function setupEventListeners() {
    submitBtn.addEventListener('click', generateArt);
    saveBtn.addEventListener('click', saveCurrentArtwork);
    shareBtn.addEventListener('click', shareCurrentArtwork);
    regenerateBtn.addEventListener('click', regenerateArt);
}

// Three.js Setup (same as before but with some enhancements)
let scene, camera, renderer;
let plane, particles;

function initThreeJS() {
    console.log("🎬 Initializing Enhanced Three.js...");
    
    const containerWidth = canvasContainer.clientWidth || 600;
    const containerHeight = canvasContainer.clientHeight || 500;
    
    scene = new THREE.Scene();
    scene.background = null;
    
    camera = new THREE.PerspectiveCamera(75, containerWidth / containerHeight, 0.1, 1000);
    camera.position.set(0, 0, 4);
    camera.lookAt(0, 0, 0);
    
    renderer = new THREE.WebGLRenderer({ 
        alpha: true, 
        antialias: true,
        preserveDrawingBuffer: true
    });
    
    renderer.setSize(containerWidth, containerHeight);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x000000, 0);
    
    canvasContainer.innerHTML = '';
    canvasContainer.appendChild(renderer.domElement);
    
    // Enhanced lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);
    
    const pointLight = new THREE.PointLight(0xffffff, 1.0);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);
    
    // Add a second light for better illumination
    const pointLight2 = new THREE.PointLight(0xffffff, 0.5);
    pointLight2.position.set(-5, -5, 5);
    scene.add(pointLight2);
    
    createParticles();
    animate();
    
    console.log("✅ Enhanced Three.js setup complete!");
}

function createParticles() {
    const particleGeometry = new THREE.BufferGeometry();
    const vertices = [];
    
    for (let i = 0; i < 1500; i++) {
        vertices.push(
            Math.random() * 30 - 15,
            Math.random() * 30 - 15,
            Math.random() * 30 - 15
        );
    }
    
    particleGeometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
    const particleMaterial = new THREE.PointsMaterial({ 
        color: 0xcccccc, 
        size: 0.05, 
        transparent: true, 
        opacity: 0.6 
    });
    
    particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);
}

function createPlane(imageBase64, sentiment = 'neutral', style = 'realistic') {
    console.log(`🖼️ Creating ${style} image plane...`);
    
    if (plane) {
        scene.remove(plane);
    }

    const imageUrl = imageBase64.startsWith('data:image') ? imageBase64 : `data:image/png;base64,${imageBase64}`;

    const loader = new THREE.TextureLoader();
    
    loader.load(
        imageUrl,
        (texture) => {
            console.log("✅ Texture loaded successfully");
            
            const geometry = new THREE.PlaneGeometry(6, 4.5);
            const material = new THREE.MeshBasicMaterial({ 
                map: texture, 
                side: THREE.DoubleSide,
                transparent: false
            });
            
            plane = new THREE.Mesh(geometry, material);
            plane.position.set(0, 0, 0);
            
            // Enhanced frame with style-based colors
            const frameColor = getFrameColorForStyle(sentiment, style);
            const frameGeometry = new THREE.EdgesGeometry(new THREE.PlaneGeometry(6.2, 4.7));
            const frameMaterial = new THREE.LineBasicMaterial({ 
                color: frameColor, 
                linewidth: 4
            });
            const frame = new THREE.LineSegments(frameGeometry, frameMaterial);
            plane.add(frame);

            scene.add(plane);
            canvasContainer.classList.add('loaded');
            
            console.log(`🎨 ${style} artwork displayed successfully!`);
        },
        (progress) => {
            console.log("📊 Loading progress:", Math.round((progress.loaded / progress.total) * 100) + "%");
        },
        (error) => {
            console.error('❌ Texture load failed:', error);
            createFallbackPlane(sentiment, style);
        }
    );
}

function getFrameColorForStyle(sentiment, style) {
    // Base color from sentiment
    const sentimentColors = {
        'positive': 0x00ff00,
        'negative': 0xff4444,
        'neutral': 0x4444ff
    };
    
    // Style modifications
    const styleModifiers = {
        'anime': 0xff69b4,      // Pink
        'cyberpunk': 0x00ffff,  // Cyan
        'oil_painting': 0xffd700, // Gold
        'watercolor': 0x87ceeb,  // Sky blue
        'vintage': 0xdaa520,     // Goldenrod
        'abstract': 0x9370db,    // Medium purple
        'sketch': 0xc0c0c0      // Silver
    };
    
    return styleModifiers[style] || sentimentColors[sentiment] || 0xffffff;
}

function animate() {
    requestAnimationFrame(animate);
    
    // Only subtle particle movement
    if (particles) {
        particles.rotation.y += 0.0005;
    }
    
    renderer.render(scene, camera);
}

// Enhanced art generation
async function generateArt() {
    const input = textInput.value.trim();
    if (!input) {
        alert('Please enter or record your feelings.');
        return;
    }

    // Show loading animation
    showLoading();
    
    try {
        console.log("🚀 Generating art with style:", selectedStyle);
        
        const response = await fetch("https://moodcanvas.onrender.com/", {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json' 
            },
            body: JSON.stringify({ 
                prompt: input,
                style: selectedStyle 
            })
        });

        if (!response.ok) {
            throw new Error(`Server responded with status: ${response.status}`);
        }

        const data = await response.json();
        console.log("📦 Received enhanced data:", {
            sentiment: data.sentiment,
            style: data.style,
            hasImage: !!data.image
        });

        if (data.error) {
            throw new Error('Server error: ' + data.error);
        }

        // Store current artwork
        currentArtwork = {
            prompt: input,
            sentiment: data.sentiment,
            style: data.style,
            image: data.image,
            timestamp: new Date().toISOString()
        };

        // Update UI
        sentimentSpan.textContent = data.sentiment;
        usedStyleSpan.textContent = availableStyles[data.style]?.name || data.style;
        promptP.textContent = input;
        
        // Display the generated image
        if (data.image) {
            createPlane(data.image, data.sentiment, data.style);
        } else {
            createFallbackPlane(data.sentiment, data.style);
        }
        
        resultDiv.classList.remove('hidden');
        console.log("✅ Enhanced art generation completed!");

    } catch (error) {
        console.error('❌ Error details:', error);
        alert(`Failed to generate art: ${error.message}\n\nPlease check if your backend server is running.`);
        
    } finally {
        hideLoading();
    }
}

// Loading animation functions
function showLoading() {
    submitBtn.innerText = 'Generating...';
    submitBtn.disabled = true;
    loadingStyle.textContent = availableStyles[selectedStyle]?.name.toLowerCase() || 'artistic';
    loadingAnimation.classList.remove('hidden');
    canvasContainer.classList.remove('loaded');
}

function hideLoading() {
    submitBtn.innerText = '🎨 Generate Art';
    submitBtn.disabled = false;
    loadingAnimation.classList.add('hidden');
}

// Save artwork functionality
async function saveCurrentArtwork() {
    if (!currentArtwork) {
        alert('No artwork to save!');
        return;
    }
    
    try {
        // Save to localStorage for now (later we'll implement database)
        const savedArtworks = JSON.parse(localStorage.getItem('moodcanvas_artworks') || '[]');
        savedArtworks.push(currentArtwork);
        localStorage.setItem('moodcanvas_artworks', JSON.stringify(savedArtworks));
        
        // Visual feedback
        saveBtn.innerHTML = '✅ Saved!';
        setTimeout(() => {
            saveBtn.innerHTML = '💾 Save Artwork';
        }, 2000);
        
        console.log('💾 Artwork saved locally');
        
    } catch (error) {
        console.error('❌ Save failed:', error);
        alert('Failed to save artwork!');
    }
}

// Share artwork functionality  
async function shareCurrentArtwork() {
    if (!currentArtwork) {
        alert('No artwork to share!');
        return;
    }
    
    try {
        // Create shareable text
        const shareText = `Check out my MoodCanvas artwork! 🎨\n\nMood: ${currentArtwork.sentiment}\nStyle: ${currentArtwork.style}\nPrompt: "${currentArtwork.prompt}"\n\nGenerated with MoodCanvas - AI Art from Emotions!`;
        
        // Try to use Web Share API if available
        if (navigator.share) {
            await navigator.share({
                title: 'My MoodCanvas Artwork',
                text: shareText,
                url: window.location.href
            });
            console.log('🔗 Shared successfully via Web Share API');
        } else {
            // Fallback: Copy to clipboard
            await navigator.clipboard.writeText(shareText);
            
            // Visual feedback
            shareBtn.innerHTML = '📋 Copied!';
            setTimeout(() => {
                shareBtn.innerHTML = '🔗 Share';
            }, 2000);
            
            console.log('📋 Share text copied to clipboard');
        }
        
    } catch (error) {
        console.error('❌ Share failed:', error);
        
        // Final fallback: Show share text in alert
        alert(`Share this:\n\n${shareText}`);
    }
}

// Regenerate artwork with same prompt but different seed
async function regenerateArt() {
    if (!currentArtwork) {
        alert('No artwork to regenerate!');
        return;
    }
    
    // Use the same prompt and style
    textInput.value = currentArtwork.prompt;
    selectedStyle = currentArtwork.style;
    renderStyleSelector();
    
    // Generate new artwork
    await generateArt();
}

// Fallback plane creation
function createFallbackPlane(sentiment, style) {
    console.log(`🔄 Creating fallback display for ${style} style...`);
    
    const canvas = document.createElement('canvas');
    canvas.width = 512;
    canvas.height = 512;
    const ctx = canvas.getContext('2d');
    
    // Style-specific gradients
    const styleGradients = {
        'anime': ['#FF69B4', '#87CEEB'],
        'cyberpunk': ['#00FFFF', '#FF00FF'],
        'oil_painting': ['#8B4513', '#DAA520'],
        'watercolor': ['#87CEEB', '#E0E6FF'],
        'vintage': ['#DEB887', '#F5DEB3'],
        'abstract': ['#9370DB', '#BA55D3'],
        'sketch': ['#696969', '#C0C0C0'],
        'realistic': ['#4682B4', '#87CEEB']
    };
    
    const colors = styleGradients[style] || ['#9370DB', '#8A2BE2'];
    
    // Create gradient
    const gradient = ctx.createRadialGradient(256, 256, 0, 256, 256, 256);
    gradient.addColorStop(0, colors[0]);
    gradient.addColorStop(1, colors[1]);
    
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 512, 512);
    
    // Add style-specific decorative elements
    ctx.globalAlpha = 0.7;
    for (let i = 0; i < 15; i++) {
        ctx.fillStyle = `hsl(${Math.random() * 360}, 70%, 70%)`;
        ctx.beginPath();
        ctx.arc(Math.random() * 512, Math.random() * 512, Math.random() * 30, 0, Math.PI * 2);
        ctx.fill();
    }
    
    // Add text
    ctx.globalAlpha = 1;
    ctx.fillStyle = 'white';
    ctx.font = 'bold 32px Arial';
    ctx.textAlign = 'center';
    ctx.fillText(`${style.charAt(0).toUpperCase() + style.slice(1)} Art`, 256, 240);
    ctx.font = '24px Arial';
    ctx.fillText(`Mood: ${sentiment}`, 256, 280);
    ctx.font = '16px Arial';
    ctx.fillText('Generated Offline', 256, 320);
    
    const dataUrl = canvas.toDataURL();
    createPlane(dataUrl, sentiment, style);
}

// Window resize handler
window.addEventListener('resize', () => {
    if (renderer && camera) {
        const containerWidth = canvasContainer.clientWidth || 600;
        const containerHeight = canvasContainer.clientHeight || 500;
        
        camera.aspect = containerWidth / containerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(containerWidth, containerHeight);
        
        console.log("📐 Canvas resized to:", containerWidth, "x", containerHeight);
    }
});

// Debug functions
function debugScene() {
    console.log("🔍 === ENHANCED SCENE DEBUG ===");
    console.log("📦 Scene children:", scene.children.length);
    console.log("🎨 Selected style:", selectedStyle);
    console.log("💾 Current artwork:", currentArtwork ? 'Available' : 'None');
    console.log("📐 Canvas size:", renderer.getSize(new THREE.Vector2()));
    
    if (plane) {
        console.log("🖼️ Plane details:", {
            position: plane.position,
            visible: plane.visible,
            material: plane.material.type
        });
    }
    
    console.log("===============================");
}