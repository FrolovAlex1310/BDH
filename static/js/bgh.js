function openPage(pageName, elmnt, color) {
  // Скрыть все элементы class="tabcontent" по умолчанию */
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Удалите цвет фона всех ссылок/кнопок вкладок
  //1
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
  }
  //2
  tablinks = document.getElementsByClassName("tablink2");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
  }

  // Показать содержимое конкретной вкладки
  document.getElementById(pageName).style.display = "block";

  // Добавить конкретный цвет кнопки, используемой для открытия содержимого вкладки
  elmnt.style.backgroundColor = color;
}

// Получите элемент с id="defaultOpen" и нажмите на него
document.getElementById("defaultOpen").click();