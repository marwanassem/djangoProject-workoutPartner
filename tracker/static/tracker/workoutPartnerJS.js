function add_exercise_form(){

    var form = document.getElementById("exercise_form");

    var cln = form.cloneNode(true);
    //cln = cln.reset();

    document.body.appendChild(cln);

}

function add_new_set(){

    var x = document.createElement("INPUT");
    var y = document.createElement("INPUT");
    x.setAttribute("type", "text");
    var p = document.createElement('P');
    var note = document.createElement('P');
    p.innerHTML = 'Set';
    note.innerHTML = 'Note';
    document.body.append(p);
    p.name = 'ayhaga';
    //console.log(p.name);
    document.body.append(x);
    document.body.append(note);
    document.body.append(y);


}