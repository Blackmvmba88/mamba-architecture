// Script para marcar automáticamente todos los archivos de un Pull Request de GitHub como 'Viewed'.
// Puedes ejecutarlo directamente en la consola del navegador dentro de la página del PR.

(function autoMarkViewed() {
  // Buscar todos los botones con aria-label "Not Viewed" o que contengan el texto "Viewed"
  const buttons = Array.from(document.querySelectorAll('button[aria-label="Not Viewed"]'));
  
  // También buscar botones que contengan el texto "Viewed" (sin usar :contains que no es válido)
  const allButtons = Array.from(document.querySelectorAll('button'));
  const viewedButtons = allButtons.filter(btn => 
    btn.innerText.trim().toLowerCase().includes('viewed') || 
    btn.getAttribute('aria-label') === 'Not Viewed'
  );
  
  let count = 0;

  viewedButtons.forEach((btn) => {
    if (btn.getAttribute('aria-label') === 'Not Viewed') {
      btn.click();
      count++;
    }
  });

  console.log(`✅ Marcados ${count} archivos como 'Viewed' automáticamente.`);
})();
