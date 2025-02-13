export async function copyCodeToClipboard(button, highlightDiv) {
	const codeToCopy = highlightDiv.querySelector(':last-child > .chroma > code').innerText;
	try {
		var result = await navigator.permissions.query({ name: 'clipboard-write' });
		if (result.state == 'granted' || result.state == 'prompt') {
			await navigator.clipboard.writeText(codeToCopy);
		} else {
			copyCodeBlockExecCommand(codeToCopy, highlightDiv);
		}
	} catch (_) {
		copyCodeBlockExecCommand(codeToCopy, highlightDiv);
	} finally {
		button.blur();
		button.innerText = 'Copied!';
		setTimeout(function () {
			button.innerText = 'Copy';
		}, 2000);
	}
  }
  
function copyCodeBlockExecCommand(codeToCopy, highlightDiv) {
	const textArea = document.createElement('textArea');
	textArea.contentEditable = 'true';
	textArea.readOnly = 'false';
	textArea.className = 'copyable-text-area';
	textArea.value = codeToCopy;
	highlightDiv.insertBefore(textArea, highlightDiv.firstChild);
	const range = document.createRange();
	range.selectNodeContents(textArea);
	const sel = window.getSelection();
	sel.removeAllRanges();
	sel.addRange(range);
	textArea.setSelectionRange(0, 999999);
	document.execCommand('copy');
	highlightDiv.removeChild(textArea);
}
  