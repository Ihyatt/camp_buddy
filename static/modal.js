function showNote(results){
 
  location.reload(true);
}

function submitNote(){
  var title = $("#note-title").val()
  var note = $("#note").val()

  $("#note-title").val("")
  $("#note").val("")

  var fullNote = { 
    "title": title,
    "note": note
  };
  $.post("/write_note", fullNote, showNote)
  $('#myModal2').modal('hide');
}

$("#note-submit").click(submitNote)

// Update question

function showQuestion(results){
 
  var questionCount = parseInt($("#question-count").text());
  questionCount += 1
  $("#question-count").text(questionCount)
  location.reload(true);
}

function submitQuestion(){
  var title = $("#question-title").val()
  var question = $("#question").val()
  
  $("#question-title").val("")
  $("#question").val("")

  var fullQuestion = { 
    "title": title,
    "question": question
  };
  $.post("/ask_question", fullQuestion, showQuestion)
  $('#myModal').modal('hide');
}


$("#question-submit").click(submitQuestion)
