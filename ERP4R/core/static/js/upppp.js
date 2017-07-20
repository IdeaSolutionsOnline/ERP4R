
function callPageDossiers(page, pagelimit, numForPage){  
    document.getElementsByClassName('current')[0].className='';
    document.getElementById('ativo'+page).className = 'current';
    var strURL = '/get_pageUPPPPDossiers/'+page+'/'+numForPage;
    $.ajax({type: 'GET', url: strURL
        }).done(function(r) {
            $('#pagDossiers').html(r);
        }).fail(function(r) {
            $('#pagDossiers').html('Erro');
    });                  
}

function callPageConcurso(page, pagelimit, numForPage){  
    document.getElementsByClassName('current')[0].className='';
    document.getElementById('ativo'+page).className = 'current';
    var strURL = '/get_pageUPPPPConcurso/'+page+'/'+numForPage;
    $.ajax({type: 'GET', url: strURL
        }).done(function(r) {
            $('#pagConcurso').html(r);
        }).fail(function(r) {
            $('#pagConcurso').html('Erro');
    });                  
}

function callPageEstudo(page, pagelimit, numForPage){  
    document.getElementsByClassName('current')[0].className='';
    document.getElementById('ativo'+page).className = 'current';
    var strURL = '/get_pageUPPPPEstudo/'+page+'/'+numForPage;
    $.ajax({type: 'GET', url: strURL
        }).done(function(r) {
            $('#pagEstudo').html(r);
        }).fail(function(r) {
            $('#pagEstudo').html('Erro');
    });                  
}

function callPageFaqs(page, pagelimit, numForPage){      
    document.getElementsByClassName('current')[0].className='';
    document.getElementById('ativo'+page).className = 'current';
    var strURL = '/get_pageUPPPPFaqs/'+page+'/'+numForPage;
    $.ajax({type: 'GET', url: strURL
        }).done(function(r) {
            $('#pagFaqs').html(r);
        }).fail(function(r) {
            $('#pagEstudo').html('Erro');
    });                  
}

//chamar por uma senha especifica
function registarPergunta()  {
    var pergunta = $('#pergunta_duvida').val();
    if(pergunta == null || pergunta == ""){
         alert("Por favor digite a sua pergunta ou duvida!");
    }else{
        $.ajax({type: 'POST', url: '/registarPergunta/' + pergunta
        }).done(function(r) {
            closeModel();
        }).fail(function(r) {
            //$('#pergunta_duvida').val('');
            alert("Erro no envio!");
        });            
    }
 }
 //fecha o model
 function closeModel(){
    $('#pergunta_duvida').val('');
    $('#myModalPergunta').foundation('reveal', 'close');
}