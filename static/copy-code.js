// Add copy buttons to all code blocks
document.addEventListener('DOMContentLoaded', function() {
  const codeBlocks = document.querySelectorAll('.codehilite pre, pre code');
  
  codeBlocks.forEach(function(block) {
    // Skip if already has a copy button
    if (block.parentElement.querySelector('.copy-button')) return;
    
    // Create copy button
    const button = document.createElement('button');
    button.className = 'copy-button';
    button.textContent = 'Copy';
    button.setAttribute('aria-label', 'Copy code to clipboard');
    
    // Get the pre element (might be the block itself or its parent)
    const pre = block.tagName === 'PRE' ? block : block.parentElement;
    const wrapper = pre.parentElement;
    
    // Create wrapper if needed
    if (!wrapper.classList.contains('code-wrapper')) {
      const newWrapper = document.createElement('div');
      newWrapper.className = 'code-wrapper';
      pre.parentNode.insertBefore(newWrapper, pre);
      newWrapper.appendChild(pre);
      newWrapper.appendChild(button);
    } else {
      wrapper.appendChild(button);
    }
    
    // Copy functionality
    button.addEventListener('click', function() {
      const code = pre.textContent;
      
      navigator.clipboard.writeText(code).then(function() {
        button.textContent = 'Copied!';
        button.classList.add('copied');
        
        setTimeout(function() {
          button.textContent = 'Copy';
          button.classList.remove('copied');
        }, 2000);
      }).catch(function(err) {
        console.error('Failed to copy:', err);
        button.textContent = 'Failed';
        setTimeout(function() {
          button.textContent = 'Copy';
        }, 2000);
      });
    });
  });
});