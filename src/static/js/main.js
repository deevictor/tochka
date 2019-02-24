$('#nasdaq').on('click', function(event){
event.preventDefault();
// console.log($('#username').val())
// console.log($('#emailid').val())
// console.log($('#password2').val())
$.ajax({
  type:'GET',
  url:nasdaq_url,
  // dataType: 'json',
  // data: $('#login_form').serialize(),
  success:function(data){
    if (data.success) {
        console.log(data.message)
      } else {
        console.log(data.message)
      }
    }
});
});
