import Clipboard from 'clipboard';

document.querySelectorAll('.highlight').forEach(block => {
  block.insertAdjacentHTML('afterbegin', '<div class="copy"><button type="button" class="btn-copy" aria-label="Copy code">Copy</button></div>');
});
const clipboard = new Clipboard('.btn-copy', {
  text: trigger => trigger.closest('.highlight').querySelector('code').textContent,
});
clipboard.on('success', event => {
  event.clearSelection();
  event.trigger.textContent = 'Copied';
  setTimeout(() => { event.trigger.textContent = 'Copy'; }, 2000);
});
clipboard.on('error', event => {
  event.trigger.textContent = 'Select and copy';
});
