/* JS for Add Attendee field:
- If no attendee can be found then it should ask if you want to add an email
  for the person
TO DO:
- Add in event listener for unfocus on field (difficult, as focus is lost on clicking name)
- Make all names in json lower case
- OR change the code to use a regex that ignores case (BETTER)
- Pressing enter will add name to list (if selected, or if not just add the words in the box)
*/

(function() {
  var attendees_form = document.getElementById("attendees"),
      name_selector = document.getElementById("name-selector"),
      names_added = document.getElementById("attendees-added"),
      submit_button = document.getElementById("submit"),
      num_attendees_input = document.getElementById("id_attendees-TOTAL_FORMS");
  num_attendees_input.value = 0;

  // submit_button.addEventListener("click", function(e){submitForm(e)}, false);

  /* Gets the contacts from db using a promise. Once promise is fulfilled, adds various
     event listeners on keyup/down */
  get('/meetings/return-names/').then(function(response) {
    return JSON.parse(response);
  }, function(error) {
    console.error("Failed!", error);
  }).then(function(response) {
    var names_json = [];
    for (var i = 0; i < response.length; i++) {
      var full_name = response[i].fields.firstName + " " + response[i].fields.secondName;
      var person_id = response[i].pk;
      var person_json = {"full_name": full_name, "id": person_id}
      names_json.push(person_json)
    }
    attendees_form.addEventListener('keydown', function(e){
      if(e.keyCode == 13) {
        e.preventDefault();
        return false;
      }
    });
    // THIS DOESN'T WORK AS CLICKING ON THE NAMES LIST MOVE FOCUS
    // attendees_form.addEventListener('focusout', function(e){
    //   var name_selector_list = document.getElementById('name-selector-list');
    //   if (name_selector_list) {
    //     name_selector_list.parentNode.removeChild(name_selector_list);
    //   }
    // });
    attendees_form.addEventListener("keyup", function(e){
      keyPress(this, e, names_json, name_selector, names_added)
    });
  });

})();

function keyPress(form_field, evt, names, name_selector, names_added) {

  // If down arrow is pressed
  if (evt.keyCode == 40) {
    if (name_selector.childNodes.length > 0) {
      selectName(name_selector, "down");
    }
    else {
      console.log("NO NAMES")
    }
  }
  // If up arrow is pressed
  else if (evt.keyCode == 38) {
    if (name_selector.childNodes.length > 0) {
      selectName(name_selector, "up");
    }
    else {
      console.log("NO NAMES")
    }
  }
  // If up enter key is pressed
  else if (evt.keyCode == 13) {
    var name_selector_list = document.getElementById('name-selector-list');
    if (name_selector_list) {
      var available_names = name_selector_list.childNodes;
      current_selected = getCurrentSelected(available_names);
      console.log(current_selected)
      if (current_selected >= 0) {
        changeName(available_names[current_selected], form_field, names_added, name_selector);
      }
    }
  }
  // if any other key is pressed. TO DO: look at why shift or other keys multiplies results
  else if (form_field.value) {
    var new_ul = document.createElement("ul");
    new_ul.id = "name-selector-list";
    for (var i = 0; i < names.length; i++) {
      var person = names[i];
      if (~person.full_name.indexOf(form_field.value)) {
        var new_name_li = document.createElement("li");
        new_name_li.id = "person-" + person.id;
        new_name_li.innerHTML = person.full_name;
        new_name_li.addEventListener('click', function(){
          changeName(this, form_field, names_added, name_selector)},
          false
        );
        new_ul.appendChild(new_name_li);
      }
      else {
        var existing_ul = document.getElementById("name-selector-list");
        if (existing_ul) {
          existing_ul.parentNode.removeChild(existing_ul);
        }
      }
    }
    name_selector.appendChild(new_ul);
  }
  else {
    var existing_ul = document.getElementById("name-selector-list");
    if (existing_ul) {
      existing_ul.parentNode.removeChild(existing_ul);
    }
  }
}


function changeName(new_li, form_field, names_added, name_selector) {
  console.log(new_li);
  var person_id = new_li.id.split('-')[1];

  form_field.value = "";
  var existing_ul = document.getElementById("name-selector-list");
  if (existing_ul) {
    existing_ul.parentNode.removeChild(existing_ul);
  }
  if (!document.getElementById(new_li.id)) {
    var name_to_add = new_li.cloneNode(true);
    name_to_add.removeAttribute('class');
    name_to_add.removeEventListener('click', function(){
      changeName(this, form_field, names_added)},
      false
    );
    names_added.appendChild(name_to_add);
    var delete_button = document.createElement("button"),
        name_to_append_to = document.getElementById(new_li.id);
    delete_button.id = new_li.id + "-delete";
    delete_button.innerHTML = ' X';
    name_to_append_to.appendChild(delete_button);
    var hidden_input = addNameToHiddenForm(names_added, form_field, person_id, name_selector);
    delete_button.addEventListener('click', function(){
      deleteName(name_to_append_to, hidden_input, name_selector)},
      false
    );
  }
  else {
    console.log("FAIL");
  }
}

// function submitForm(e) {
//   e.preventDefault();
//   form = document.getElementById("form");
//   console.log(form);
//   var data = new FormData(form);
//   data["book"] = "book";
//   console.log(data.entries())
// }

function selectName(name_selector, direction) {
  var available_names = document.getElementById('name-selector-list').childNodes;
  current_selected = getCurrentSelected(available_names)
  if (current_selected >= available_names.length-1 && direction == "up") {
    available_names[current_selected].removeAttribute("class");
    var next_selection = current_selected-1;
    available_names[next_selection].setAttribute("class", "selected");
  }
  else if (current_selected >= available_names.length-1 || current_selected < 0) {
    available_names[current_selected].removeAttribute("class");
    available_names[0].setAttribute("class", "selected");
  }
  else if (current_selected == 0 && direction == "up") {
    available_names[current_selected].removeAttribute("class");
    available_names[available_names.length-1].setAttribute("class", "selected");
  }
  else if (current_selected >= 0) {
    available_names[current_selected].removeAttribute("class");
    if (direction == "up"){
      var next_selection = current_selected-1;
    }
    else {
      var next_selection = current_selected+1;
    }
    available_names[next_selection].setAttribute("class", "selected");
  }
  else {
    available_names[0].setAttribute("class", "selected");
  }
}

function addNameToHiddenForm(names_added, form_field, person_id, name_selector) {
  var num_attendees_input = document.getElementById("id_attendees-TOTAL_FORMS"),
      num_attendees = num_attendees_input.value,
      hidden_input = document.createElement("input");
  hidden_input.type = "hidden";
  hidden_input.name = "attendees-"+num_attendees+"-person";
  hidden_input.id = "id_attendees-"+num_attendees+"-person";
  hidden_input.value = person_id;
  name_selector.appendChild(hidden_input);
  num_attendees_input.value = parseInt(num_attendees)+1;
  return hidden_input;
}

function deleteName(name_to_delete, hidden_input, name_selector) {
  name_to_delete.parentNode.removeChild(name_to_delete);
  hidden_input.parentNode.removeChild(hidden_input);
  renameHiddenInputs(name_selector);
}

function renameHiddenInputs(name_selector) {
  var num_attendees_input = document.getElementById("id_attendees-TOTAL_FORMS"),
      remaining_inputs = name_selector.childNodes;
  num_attendees_input.value = parseInt(num_attendees_input.value)-1;
  if (remaining_inputs) {
    var num_attendees = parseInt(num_attendees_input.value)- 1;
    for (var i = 0; i < remaining_inputs.length; i++) {
        remaining_inputs[i].name = "attendees-"+num_attendees+"-person";
        remaining_inputs[i].id = "id_attendees-"+num_attendees+"-person";
    }
  }
}

function getCurrentSelected(available_names) {
  for (var i = 0; i < available_names.length; i++) {
      if (available_names[i].className == "selected") {
        var current_selected = i;
      }
  }
  return current_selected;
}

function get(url) {
  // Return a new promise.
  return new Promise(function(resolve, reject) {
    // Do the usual XHR stuff
    var req = new XMLHttpRequest();
    req.open('GET', url);
    req.onload = function() {
      // This is called even on 404 etc
      // so check the status
      if (req.status == 200) {
        // Resolve the promise with the response text
        resolve(req.response);
      }
      else {
        // Otherwise reject with the status text
        // which will hopefully be a meaningful error
        reject(Error(req.statusText));
      }
    };
    // Handle network errors
    req.onerror = function() {
      reject(Error("Network Error"));
    };
    // Make the request
    req.send();
  });
}
