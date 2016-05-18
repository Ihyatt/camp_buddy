
function showResults(resp) {
    $('#Inas-div').text(resp.age);
}

function submitUpdate(evt) {
    evt.preventDefault();

    var formInputs = {
        "age": $('#age-update').val(),
        "city": $('#city-update').val(),
        "state": $("#state-update").val(),
        "boot_camp_name":$("#boot-camp-name-update").val(),
        "about_me":$("#about-me-update").val()
        "image_url":$("#image-url-update").val()
        "linkedin_url":$("#linkedin-url-update").val()
        "github_url":$("#github-url-update").val()
    };

    $.post('/update-profile', formInputs, showResults);
  
}
// $("#edit_profile").submit(submitUpdate);  

