/*serve para a paginação nas listas*/
function callPage(page){
     
    
    alert(page);   
    
    var strURL = '/get_page' ;
    $.ajax({type: 'POST', url: strURL
        }).done(function(r) {
            $('#pagup').html(r);
        }).fail(function(r) {
            $('#pagup').html('Erro');
        });
    /*$('#message').html('');
    var strURL = '/get_page/' + page ;

    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
            $('#pagup').html(r);
        }).fail(function(r) {
            showMessage('alert', r.responseText, $('#message'), $('#message_container'));
        });
    */
 }

function regist_forneced() {
    
    var strURL = '/registFornecd';
    
    $.ajax({type: 'POST', url: strURL, data: $('#form_registForncd').serialize()
        }).done(function(r) {
            alert(r);
        }).fail(function(r) {
             alert('False');
        });

}

function openPdf(e, path, redirect) {
    // stop the browser from going to the href
    e = e || window.event; // for IE
    e.preventDefault(); 

    // launch a new window with your PDF
    window.open(path, 'somename', ... /* options */);

    // redirect current page to new location
    window.location = redirect;
}

