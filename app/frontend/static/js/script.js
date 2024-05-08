window.addEventListener('load', function() {
    document.getElementById('loading').style.display = 'none';
    Array.from(document.body.children).forEach(function(child) {
        if (child.id !== 'loading') {
            child.style.display = 'block';
        }
    });
});

