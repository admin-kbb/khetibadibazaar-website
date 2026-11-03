'use strict';
document.documentElement.classList.add('js');
const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
if (menu && navigation) {
  menu.hidden = false;
  const closeMenu = () => {
    menu.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
  };
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  navigation.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
      closeMenu();
      menu.focus();
    }
  });
  window.matchMedia('(min-width: 901px)').addEventListener('change', closeMenu);
}
const categories = {
  machinery: ['Built for your next season.', 'From your first tractor to your next upgrade. Explore tractors, farm machinery and equipment in one place.', 'Illustrative farm tractor and machinery'],
  crops: ['Fresh opportunities. Every harvest.', 'From grains to fresh produce, discover a dedicated place for the things your farm grows.', 'Illustrative collection of farm produce'],
  cattle: ['Good livestock. New possibilities.', 'Explore cattle and livestock listings, with photos and details to help you take a closer look.', 'Illustrative farm livestock'],
  seeds: ['Every season starts somewhere.', 'Explore seeds and find a starting point for the next chapter of your farm.', 'Illustrative seeds and planting supplies'],
  farming_land: ['Room for your next idea.', 'Discover farming land listings and explore the possibilities for your next agricultural venture.', 'Illustration of cultivated farming land']
};
document.querySelectorAll('[data-category]').forEach((button) => {
  button.addEventListener('click', () => {
    const key = button.dataset.category;
    const data = categories[key];
    if (!data) return;
    document.querySelectorAll('[data-category]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
    document.querySelector('#category-title').textContent = data[0];
    document.querySelector('#category-copy').textContent = data[1];
    const image = document.querySelector('#category-image');
    image.src = `assets/${key}.webp`;
    image.alt = data[2];
  });
});
document.querySelectorAll('[data-year]').forEach((element) => { element.textContent = new Date().getFullYear(); });
