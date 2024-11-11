<div id="markdown-content"></div>
<script src="https://cdn.jsdelivr.net/npm/showdown/dist/showdown.min.js"></script>
<script>
    fetch('https://raw.githubusercontent.com/ChaoticRoman/ChaoticRoman/refs/heads/main/README.md')
        .then(response => response.text())
        .then(data => {
            var converter = new showdown.Converter();
            var html = converter.makeHtml(data);
            document.getElementById('markdown-content').innerHTML = html;
        })
        .catch(error => console.error('Error fetching file:', error));
</script>