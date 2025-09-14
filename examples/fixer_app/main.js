document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('main-canvas');
    const ctx = canvas.getContext('2d');
    const jointList = document.getElementById('joint-list');
    const submitBtn = document.getElementById('submit-btn');
    const statusMessage = document.getElementById('status-message');

    let characterImage = new Image();
    let skeletonData = null;
    let selectedJoint = null;
    let dragging = false;

    // --- INITIALIZATION ---

    function init() {
        // Fetch the character texture and the default skeleton data
        Promise.all([
            loadImage('/texture.png'),
            fetch('/annotations').then(res => res.json())
        ]).then(([img, data]) => {
            characterImage = img;
            skeletonData = data;
            
            // Resize canvas to fit the image
            canvas.width = characterImage.width;
            canvas.height = characterImage.height;

            populateJointList();
            draw();
            setupEventListeners();
        }).catch(err => {
            statusMessage.textContent = 'Error loading character. Make sure texture.png exists.';
            console.error(err);
        });
    }

    function loadImage(url) {
        return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(img);
            img.onerror = reject;
            img.src = url;
        });
    }

    // --- UI AND DRAWING ---

    function populateJointList() {
        jointList.innerHTML = '';
        for (const jointName in skeletonData.joints) {
            const li = document.createElement('li');
            li.textContent = jointName;
            li.dataset.joint = jointName;
            li.addEventListener('click', () => {
                selectedJoint = jointName;
                populateJointList(); // Re-render to show selection
                draw();
            });
            if (jointName === selectedJoint) {
                li.classList.add('selected');
            }
            jointList.appendChild(li);
        }
    }

    function draw() {
        if (!skeletonData) return;
        
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw character image
        ctx.drawImage(characterImage, 0, 0);

        // Draw skeleton lines
        ctx.strokeStyle = 'rgba(255, 255, 0, 0.7)';
        ctx.lineWidth = 2;
        skeletonData.skeleton.forEach(bone => {
            if (bone.parent) {
                const start = skeletonData.joints[bone.parent];
                const end = skeletonData.joints[bone.name];
                ctx.beginPath();
                ctx.moveTo(start[0], start[1]);
                ctx.lineTo(end[0], end[1]);
                ctx.stroke();
            }
        });

        // Draw joints
        for (const jointName in skeletonData.joints) {
            const [x, y] = skeletonData.joints[jointName];
            ctx.beginPath();
            ctx.arc(x, y, 6, 0, 2 * Math.PI);
            ctx.fillStyle = (jointName === selectedJoint) ? '#007bff' : 'red';
            ctx.fill();
        }
    }

    // --- EVENT LISTENERS ---

    function setupEventListeners() {
        canvas.addEventListener('mousedown', onMouseDown);
        canvas.addEventListener('mousemove', onMouseMove);
        canvas.addEventListener('mouseup', onMouseUp);
        canvas.addEventListener('mouseleave', onMouseUp); // Stop dragging if mouse leaves canvas
        submitBtn.addEventListener('click', submitAnnotations);
    }
    
    function getMousePos(e) {
        const rect = canvas.getBoundingClientRect();
        return {
            x: e.clientX - rect.left,
            y: e.clientY - rect.top
        };
    }

    function onMouseDown(e) {
        const pos = getMousePos(e);
        for (const jointName in skeletonData.joints) {
            const [jx, jy] = skeletonData.joints[jointName];
            const dx = pos.x - jx;
            const dy = pos.y - jy;
            if (dx * dx + dy * dy < 10 * 10) { // Check if click is inside joint radius
                selectedJoint = jointName;
                dragging = true;
                populateJointList();
                draw();
                return;
            }
        }
    }

    function onMouseMove(e) {
        if (!dragging || !selectedJoint) return;
        const pos = getMousePos(e);
        skeletonData.joints[selectedJoint] = [pos.x, pos.y];
        draw();
    }

    function onMouseUp() {
        dragging = false;
    }

    // --- SUBMISSION ---

    async function submitAnnotations() {
        statusMessage.textContent = 'Submitting...';
        try {
            const response = await fetch('/annotations', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(skeletonData)
            });
            if (!response.ok) throw new Error('Server responded with an error.');
            const result = await response.json();
            if(result.success) {
                statusMessage.textContent = 'Annotations saved successfully!';
            } else {
                throw new Error('Save was not successful.');

            }
        } catch (err) {
            statusMessage.textContent = `Error: ${err.message}`;
        }
    }

    // Start the application
    init();
});