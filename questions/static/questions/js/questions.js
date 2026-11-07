'use strict';

// Демонстрация состояний голосования из ДЗ1. Сервер их пока не сохраняет.
document.querySelectorAll('.vote-widget').forEach(widget => {
  const buttons = widget.querySelectorAll('button');
  const counter = widget.querySelector('[data-counter]');
  const base = Number(counter.textContent) - Number(widget.dataset.vote);

  buttons.forEach(button => button.addEventListener('click', () => {
    const vote = Number(button.dataset.vote);
    const next = Number(widget.dataset.vote) === vote ? 0 : vote;
    widget.dataset.vote = next;
    counter.textContent = base + next;
    buttons.forEach(item => {
      const selected = Number(item.dataset.vote) === next;
      item.setAttribute('aria-pressed', String(selected));
      item.classList.toggle('active', selected);
    });
  }));
});
