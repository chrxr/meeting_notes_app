/* JS for Add Attendee field:

- As user types into the box the page checks to see if there are any
  attendees who's names include those letters

- Should check for letters in any part of the name, as long as they are together

- Names should appear below the entry field. Clicking a name, or clicking down
  with the arrow keys and pressing enter should add the attendee to the list

- If no attendee can be found then it should ask if you want to add an email
  for the person

-
*/

(function() {
  var attendees_form = document.getElementById("attendees"),
      name_selector = document.getElementById("name-selector-list");
  var names = ["Chris Rogers", "Jenny Rogers", "Bob Hope"];
  attendees_form.addEventListener("keyup", function(e){keyPress(this, e, names, name_selector)});
})();

function keyPress(form_field, evt, names, name_selector) {
  console.log(evt.keyCode, form_field.value)
  if (evt.keyCode == 40) {
    if (name_selector.childNodes.length > 1) {
      console.log(name_selector.childNodes);
    }
  }
  else if (evt.keyCode == 38) {
    console.log("up!");
  }

  /* Dedupe the names that are returned in the list */
  else if (form_field.value) {
    for (var i = 0; i < names.length; i++) {
      if (~names[i].indexOf(form_field.value)) {
        new_name_li = document.createElement("li");
        new_name_li.innerHTML = names[i];
        name_selector.appendChild(new_name_li);
      }
      else {
        /* Change the above so that the <ul> is created as well, allowing it to be easily cleared by removing the elements */
      }
    }
  }
}
