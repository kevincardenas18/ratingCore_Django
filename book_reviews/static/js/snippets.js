// Espera a que el documento esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
  // Verifica si el mensaje de error está presente en el modal
  var errorAlert = document.getElementById('error-alert');
  
  // Si el mensaje de error está presente, muestra el modal
  if (errorAlert) {
    var modal = new bootstrap.Modal(document.getElementById('newCategoria'));
    modal.show();
  }
});

