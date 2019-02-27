$('#nasdaq').on('click', function(event){
  event.preventDefault();
  alert('Parsing started!')

  $.ajax({
    type:'GET',
    url:nasdaq_url,
    success:function(data){
      alert(data.message);
      console.log(data.message);
    },
    error:function(data){
      alert('Server is not responding');
    }
  });
});
