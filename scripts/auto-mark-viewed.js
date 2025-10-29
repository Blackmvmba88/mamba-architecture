// Script para marcar automáticamente todos los archivos de un Pull Request de GitHub como 'Viewed'.
// Puedes ejecutarlo directamente en la consola del navegador dentro de la página del PR.

(function autoMarkViewed() {
  // Buscar todos los botones con aria-label "Not Viewed"
  const notViewedButtons = Array.from(document.querySelectorAll('button[aria-label="Not Viewed"]'));
  
  let count = 0;

  notViewedButtons.forEach((btn) => {
    btn.click();
    count++;
  });

  console.log(`✅ Marcados ${count} archivos como 'Viewed' automáticamente.`);
})();
