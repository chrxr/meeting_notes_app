(function() {
  var add_button = document.getElementById('add_points'),
      first_delete_button = document.getElementById('id_agenda_points-0-delete'),
      agenda_list = document.getElementById('id_agenda_points-0-list');
  first_delete_button.addEventListener('click', function(){deleteAgenda(agenda_list)}, false);
  add_button.addEventListener('click', function(){addPoints(agenda_list)}, false);
})();

/* STUFF TO DO:
 */


function addPoints(agenda_list) {

  var total_current_forms = document.getElementById("id_agenda_points-TOTAL_FORMS"),
      next_form_number = parseInt(total_current_forms.value),
      agenda_container = document.getElementById("agenda_container"),
      new_agenda_list = agenda_list.cloneNode(true),
      new_agenda_list_children = new_agenda_list.childNodes;

  new_agenda_list.id = "id_agenda_points-" + next_form_number +"-list";

  for (var i = 0; i < new_agenda_list_children.length; i++) {
    new_li = new_agenda_list_children[i]

    if (new_li.id) {
      var existing_id = new_li.id;
      existing_id = existing_id.split('-');
      existing_id[1] = next_form_number;
      var new_id = existing_id.join('-')
      new_li.id = new_id;
      new_li.addEventListener('click', function(){deleteAgenda(new_agenda_list)},false )
    }

    for (var ii = 0; ii < new_li.childNodes.length; ii++) {
      if (new_li.childNodes[ii].id) {

        var existing_id = new_li.childNodes[ii].id.split('-'),
            existing_name = new_li.childNodes[ii].name.split('-');

        existing_id[1] = next_form_number;
        existing_name[1] = next_form_number;

        var new_id = existing_id.join('-'),
            new_name = existing_name.join('-');

        new_li.childNodes[ii].id = new_id;
        new_li.childNodes[ii].name = new_name;
        new_li.childNodes[ii].value = ""
      }

      if (new_li.childNodes[ii].htmlFor) {
        var existing_for = new_li.childNodes[ii].htmlFor.split('-');
        existing_for[1] = next_form_number;
        var new_for = existing_for.join('-');
        new_li.childNodes[ii].htmlFor = new_for;
      }
    }
  }
  agenda_container.appendChild(new_agenda_list);
  total_current_forms.value = next_form_number+1;
}

function deleteAgenda(agenda_list) {
  var total_current_forms = document.getElementById("id_agenda_points-TOTAL_FORMS"),
      next_form_number = parseInt(total_current_forms.value) - 1,
      agenda_container = document.getElementById("agenda_container");

  total_current_forms.value = next_form_number;
/* Needs to remove agenda point before renaming remaining ones */
  agenda_list.parentNode.removeChild(agenda_list);

  var remaining_uls = agenda_container.childNodes,
      form_number_reset = 0;

  for (var i = 0; i < remaining_uls.length; i++) {
    if (remaining_uls[i].id) {
      var existing_ul_id = remaining_uls[i].id.split('-');
      existing_ul_id[1] = form_number_reset;
      var new_ul_id = existing_ul_id.join('-');
      remaining_uls[i].id = new_ul_id;

      var deeper_lis = remaining_uls[i].childNodes;
      /* deeper_lis.childNodes includes [text] objects. How to get around this? */

      for (var iii = 0; iii < deeper_lis.length; iii++) {
        if (deeper_lis[iii].childNodes) {
          for (var b = 0; b < deeper_lis[iii].childNodes.length; b++) {

            if (deeper_lis[iii].childNodes[b].id){
              input = deeper_lis[iii].childNodes[b];
              var existing_id = input.id.split('-'),
                  existing_name = input.name.split('-');
              existing_id[1] = form_number_reset;
              existing_name[1] = form_number_reset;
              var new_id = existing_id.join('-'),
                  new_name = existing_name.join('-');
              input.id = new_id;
              input.name = new_name;
            }
            if (deeper_lis[iii].childNodes[b].htmlFor) {
              label = deeper_lis[iii].childNodes[b];
              var existing_for = label.htmlFor.split('-');
              existing_for[1] = form_number_reset;
              var new_for = existing_for.join('-');
              label.htmlFor = new_for;
            }
          }
        }
      }
      ++form_number_reset
    }
  }

}
