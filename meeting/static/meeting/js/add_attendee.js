(function() {
  var addAttendeeButton = document.getElementById("add_attendee");
  addAttendeeButton.addEventListener('click', addAttendee, false);
})();

function addAttendee() {
  var totalCurrentForms = document.getElementById("id_form-TOTAL_FORMS")
  var nextFormNumber = parseInt(totalCurrentForms.value)+1
  var existingSelect = document.getElementById("id_form-1-person")
  var selectArray = [];
  for (i = 1; i < existingSelect.options.length; i++){
      selectArray.push(existingSelect.options[i].text)
  }
  console.log(selectArray)
  var form = document.forms["attendee_form"]
  var input = document.createElement('select')
  input.options = existingSelect.options;
  input.id = "id_form-"+(nextFormNumber)+'-person';
  input.label = "Person";
  totalCurrentForms.value = nextFormNumber;
  form.appendChild(input);
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
