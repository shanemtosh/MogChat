document.addEventListener('DOMContentLoaded', function() {
    const inputText = document.getElementById('input-text');
    const translateBtn = document.getElementById('translate-btn');
    const outputSection = document.getElementById('output-section');
    const outputText = document.getElementById('output-text');
    const directionLabel = document.getElementById('direction-label');
    const copyBtn = document.getElementById('copy-btn');
    const btnText = document.querySelector('.btn-text');
    const btnLoader = document.querySelector('.btn-loader');
    
    // Translate button click handler
    translateBtn.addEventListener('click', async function() {
        const text = inputText.value.trim();
        
        if (!text) {
            alert('Please enter some text to translate');
            return;
        }
        
        // Get selected direction
        const direction = document.querySelector('input[name="direction"]:checked').value;
        
        // Show loading state
        translateBtn.disabled = true;
        btnText.style.display = 'none';
        btnLoader.style.display = 'inline';
        
        try {
            const response = await fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    direction: direction
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                // Display result
                outputText.textContent = data.translated;
                
                // Show direction label
                const directionText = data.direction === 'to_gen_z' 
                    ? 'Translated: Normal → Gen Z' 
                    : 'Translated: Gen Z → Normal';
                directionLabel.textContent = directionText;
                
                // Show output section
                outputSection.style.display = 'block';
                
                // Scroll to output
                outputSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            } else {
                alert('Error: ' + (data.error || 'Translation failed'));
            }
        } catch (error) {
            alert('Error: ' + error.message);
        } finally {
            // Reset button state
            translateBtn.disabled = false;
            btnText.style.display = 'inline';
            btnLoader.style.display = 'none';
        }
    });
    
    // Copy button handler
    copyBtn.addEventListener('click', async function() {
        const text = outputText.textContent;
        
        try {
            await navigator.clipboard.writeText(text);
            
            // Show copied state
            copyBtn.classList.add('copied');
            copyBtn.innerHTML = `
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="20 6 9 17 4 12"></polyline>
                </svg>
            `;
            
            // Reset after 2 seconds
            setTimeout(() => {
                copyBtn.classList.remove('copied');
                copyBtn.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                `;
            }, 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    });
    
    // Allow Enter key to translate (Ctrl+Enter or Cmd+Enter)
    inputText.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            translateBtn.click();
        }
    });
});
