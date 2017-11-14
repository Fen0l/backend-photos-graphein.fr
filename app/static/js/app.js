Dropzone.autoDiscover = false;

function hide_all_events(){
  $('#post-error, #post-success, #post-warning').hide();
}

function empty_all_fields(){
  $('#title-photo').val("");
  $('#desc-photo').val("");
  $('#tags-photo').val("");
}


function empty_form(){
  if(!$('#title-photo').val() || !$('#desc-photo').val() || !$('#tags-photo').val()){
    return true
  } else {
    return false
  }
}
hide_all_events();

var myDropzone = new Dropzone("div#droparea", {
  url: "/uploadajax",
  method: "POST",
  maxFilesize: 50,
  params: { foo: "bar" },
  paramName: "file",
  uploadMultiple: false,
  addRemoveLinks: true,
  previewsContainer: ".dropzone-previews",
  createImageThumbnails: true,
  maxFiles: 1,
  acceptedFiles: "image/png, image/jpeg",
  autoProcessQueue: false,
  forceFallback: false,

  init: function() {
  },
  resize: function(file) {
    return {"srcX":0, "srcY":0, "srcWidth":300, "srcHeight":300}
  },
  success: function(file, responseText) {
    $('#post-success').show()
    $('#post-warning, #post-error').hide()
    empty_all_fields();

    if (file.previewElement) {
      return file.previewElement.classList.add("dz-success");
    }
  },
  error: function(){
    console.log("error");
    $('#post-error').val("Server error").show();
  },
  accept: function(file, done) {
    console.log("accept");
    done();
  },
  fallback: function() {
    console.log("fallback");
  },
  sending: function(file, xhr, formData) {
    formData.append("title-photo", $('#title-photo').val());
    formData.append("desc-photo", $('#desc-photo').val());
    formData.append("tags-photo", $('#tags-photo').val());
    $('#post-error, #post-success').hide()
    $('#post-warning').show()

  },
  removedfile: function removedfile(file) {
    if (file.previewElement != null && file.previewElement.parentNode != null) {
      file.previewElement.parentNode.removeChild(file.previewElement);
    }

    return this._updateMaxFilesReachedClass();
  }
});

  $('#fileSubmit').click(function(){       
    $('#post-error').html("Oh snap! It seems that the ").hide();

    let missings = [];
    if(!$('#title-photo').val()){
      missings.push("the title");
    } 
    if(!$('#desc-photo').val()){
      missings.push("the description");
    } 
    if(!$('#tags-photo').val()){
      missings.push("the tags");
    } 

    $(missings).each(function() {
      $('#post-error').html($('#post-error').html() + this + " and ");
    });
    $('#post-error').html($('#post-error').html().substr(0,($('#post-error').html().length -4)));

    $('#post-error').html($('#post-error').html() + (missings.length > 1 ? "are missing" : 'is missing'));

    $('#post-error').show()

    if(missings === undefined || missings.length == 0) {
      $('#post-error').hide()
      myDropzone.processQueue();
    } else {
      $('#post-error').show()
    }
  });