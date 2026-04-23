document.addEventListener('DOMContentLoaded', () => {
    const tabBtns = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    const summarizeBtn = document.getElementById('summarize-btn');
    const textArea = document.getElementById('text-area');
    const fileUpload = document.getElementById('file-upload');
    const dropZone = document.getElementById('drop-zone');
    const fileNameDisplay = document.getElementById('file-name');
    const outputSection = document.getElementById('output-section');
    const originalDisplay = document.getElementById('original-display');
    const summaryDisplay = document.getElementById('summary-display');
    const keywordsList = document.getElementById('keywords-list');
    const loader = document.getElementById('loader');
    const btnText = document.querySelector('.btn-text');
    const originalWordCount = document.getElementById('original-word-count');
    const copyBtn = document.getElementById('copy-btn');
    const downloadBtn = document.getElementById('download-btn');
    const lengthSelect = document.getElementById('summary-length');

    let currentTab = 'text-input';
    let selectedFile = null;

    // Tab Switching
    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            const tabId = btn.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
            currentTab = tabId;
        });
    });

    // File Upload Handling
    dropZone.addEventListener('click', () => fileUpload.click());

    fileUpload.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.style.borderColor = 'var(--primary)';
        dropZone.style.background = 'rgba(99, 102, 241, 0.05)';
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.style.borderColor = 'var(--border-color)';
        dropZone.style.background = 'transparent';
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        if (e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });

    function handleFileSelection(file) {
        const allowedTypes = ['.pdf', '.txt'];
        const ext = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!allowedTypes.includes(ext)) {
            alert('Please upload a PDF or TXT file.');
            return;
        }

        selectedFile = file;
        fileNameDisplay.textContent = `Selected: ${file.name}`;
    }

    // Summarize Action
    summarizeBtn.addEventListener('click', async () => {
        if (currentTab === 'text-input' && !textArea.value.trim()) {
            alert('Please enter some text.');
            return;
        }
        if (currentTab === 'file-input' && !selectedFile) {
            alert('Please upload a file.');
            return;
        }

        setLoading(true);

        try {
            let result;
            const lengthType = lengthSelect.value;

            if (currentTab === 'text-input') {
                const response = await fetch('/summarize', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: textArea.value, length_type: lengthType })
                });
                result = await response.json();
            } else {
                const formData = new FormData();
                formData.append('file', selectedFile);
                formData.append('length_type', lengthType);

                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData
                });
                result = await response.json();
            }

            displayResult(result);
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while processing your request.');
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        if (isLoading) {
            loader.style.display = 'block';
            btnText.textContent = 'Processing...';
            summarizeBtn.disabled = true;
            outputSection.classList.add('hidden');
        } else {
            loader.style.display = 'none';
            btnText.textContent = 'Summarize Now';
            summarizeBtn.disabled = false;
        }
    }

    function displayResult(data) {
        outputSection.classList.remove('hidden');
        originalDisplay.textContent = data.original_text;
        summaryDisplay.textContent = data.summary;
        
        const wordCount = data.original_text.split(/\s+/).length;
        originalWordCount.textContent = `${wordCount} words`;

        keywordsList.innerHTML = '';
        data.keywords.forEach(kw => {
            const span = document.createElement('span');
            span.className = 'kw-tag';
            span.textContent = kw;
            keywordsList.appendChild(span);
        });

        // Scroll to output
        outputSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Copy to Clipboard
    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(summaryDisplay.textContent);
        copyBtn.innerHTML = '<i class="fas fa-check"></i>';
        setTimeout(() => {
            copyBtn.innerHTML = '<i class="far fa-copy"></i>';
        }, 2000);
    });

    // Download as TXT
    downloadBtn.addEventListener('click', () => {
        const element = document.createElement('a');
        const file = new Blob([summaryDisplay.textContent], {type: 'text/plain'});
        element.href = URL.createObjectURL(file);
        element.download = "summary.txt";
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    });
});
