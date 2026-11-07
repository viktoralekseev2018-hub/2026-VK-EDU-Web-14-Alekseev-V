import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

'use strict';

// Три состояния голосования: лайк, дизлайк, без голоса.
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

// Ошибки формы показываются средствами Bootstrap.
document.querySelectorAll('.demo-form').forEach(form => {
  form.addEventListener('input', event => {
    event.target.classList.remove('is-invalid');
    event.target.removeAttribute('aria-invalid');
    const password = form.querySelector('[name="password"]');
    const confirmation = form.querySelector('[name="password-repeat"]');
    if (password && confirmation) {
      confirmation.setCustomValidity(
        password.value === confirmation.value ? '' : 'Пароли не совпадают'
      );
    }
  });

  form.addEventListener('submit', event => {
    event.preventDefault();
    form.classList.add('was-validated');
    const message = form.querySelector('[data-form-message]');
    const valid = form.checkValidity();
    message.hidden = false;
    message.className = valid ? 'alert alert-info' : 'alert alert-danger';
    message.textContent = valid
      ? 'Форма заполнена. Это статический макет: данные не отправляются.'
      : 'Проверьте правильность заполнения полей.';
    if (!valid) form.querySelector(':invalid')?.focus();
  });
});

// Поиск, теги и две страницы одного статического списка.
const questionList = document.querySelector('[data-question-list]');
if (questionList) {
  const params = new URLSearchParams(location.search);
  const tag = params.get('tag');
  const query = (params.get('q') || '').trim().toLowerCase();
  const cards = [...questionList.querySelectorAll('article')];
  const filtered = cards.filter(card =>
    (!tag || card.dataset.tags.split(' ').includes(tag)) &&
    (!query || card.textContent.toLowerCase().includes(query))
  );
  const totalPages = Math.max(1, Math.ceil(filtered.length / 3));
  const page = Math.min(totalPages, Math.max(1, parseInt(params.get('page'), 10) || 1));
  cards.forEach(card => { card.hidden = true; });
  filtered.slice((page - 1) * 3, page * 3).forEach(card => { card.hidden = false; });

  if (tag || query) {
    document.querySelector('h1').textContent = tag ? `Вопросы с тегом «${tag}»` : 'Результаты поиска';
  }
  document.querySelector('[data-empty]').hidden = filtered.length > 0;
  document.querySelectorAll('[data-page-link]').forEach(link => {
    const number = Number(link.dataset.pageLink);
    link.parentElement.hidden = number > totalPages;
    link.parentElement.classList.toggle('active', number === page);
    if (number === page) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
    params.set('page', number);
    link.href = `index.html?${params}`;
  });
}

// Пагинация демонстрационных ответов.
const answerPages = document.querySelectorAll('[data-answer-page]');
if (answerPages.length) {
  const page = new URLSearchParams(location.search).get('answers') === '2' ? '2' : '1';
  answerPages.forEach(block => { block.hidden = block.dataset.answerPage !== page; });
  document.querySelectorAll('[data-answer-link]').forEach(link => {
    const active = link.dataset.answerLink === page;
    link.parentElement.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
}
