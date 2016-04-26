(function() {
  var addAttendeeButton = document.getElementById("add_attendee");
  addAttendeeButton.addEventListener('click', addAttendee, false);
})();

function addAttendee() {
  var totalCurrentForms = document.getElementById("id_form-TOTAL_FORMS"),
      nextFormNumber = parseInt(totalCurrentForms.value)+1,
      existingSelect = document.getElementById("id_form-1-person"),
      selectArray = [];
      attendee_list = document.getElementById("attendee_list"),
      list_item = document.createElement('li')
      select = document.createElement('select');
  select.id = "id_form-"+parseInt(totalCurrentForms.value)+'-person';
  select.name = "id_form-"+parseInt(totalCurrentForms.value)+'-person';
  for (i = 0; i < existingSelect.options.length; i++){
      option = document.createElement('option');
      if (i == 0) {
        option.value = ""
        option.setAttribute("selected", "selected");
      }
      else {
        option.value = i
      }
      option.text = existingSelect.options[i].text
      select.appendChild(option);
  }
  select.options[0].selected = 'selected';
  totalCurrentForms.value = nextFormNumber;
  list_item.appendChild(select)
  attendee_list.appendChild(list_item);
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
