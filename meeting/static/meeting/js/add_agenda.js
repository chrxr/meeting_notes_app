(function() {
  var addAgendaButton = document.getElementById("add_agenda");
  addAgendaButton.addEventListener('click', addAgenda, false);
})();

function addAgenda() {
  var totalCurrentForms = document.getElementById("id_form-TOTAL_FORMS");
  if (totalCurrentForms == null) {
    totalCurrentForms = document.getElementById("id_agenda_points-TOTAL_FORMS");
  }
  var nextFormNumber = parseInt(totalCurrentForms.value)+1,
      agenda_list = document.getElementById("agenda_list_1"),
      agenda_form = document.getElementById("form_block"),
      new_agenda_item = agenda_list.cloneNode(true),
      new_agenda_item_children = new_agenda_item.childNodes;
  new_agenda_item.id = "agenda_list_" + nextFormNumber
  for (var i = 0; i < new_agenda_item_children.length; i++) {
    new_li = new_agenda_item_children[i]
    for (var ii = 0; ii < new_li.childNodes.length; ii++) {
      if (new_li.childNodes[ii].id) {
        existing_id = new_li.childNodes[ii].id;
        existing_name = new_li.childNodes[ii].name;
        existing_id = existing_id.split('-');
        existing_name = existing_name.split('-');
        existing_id[1] = nextFormNumber-1;
        existing_name[1] = nextFormNumber-1;
        new_id = existing_id.join('-')
        new_name = existing_name.join('-')
        new_li.childNodes[ii].id = new_id;
        new_li.childNodes[ii].name = new_name;
        new_li.childNodes[ii].value = ""
      }
    }
  }
  agenda_form.appendChild(new_agenda_item);
  totalCurrentForms.value = nextFormNumber;
}

  // collect the form data while iterating over the inputs
// var data = {};
// for (var i = 0, ii = form.length; i < ii; ++i) {
//   var input = form[i];
//   if (input.name) {
//     data[input.name] = input.value;
//   }
// }

  // construct an HTTP request
//   var xhr = new XMLHttpRequest();
//   xhr.open(form.method, form.action, true);
//   xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
//
//   // send the collected data as JSON
//   xhr.send(JSON.stringify(data));
//
//   xhr.onloadend = function () {
//     // done
//   };
// };
