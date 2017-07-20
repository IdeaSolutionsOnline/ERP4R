//funcao de paginacao
function callPage(page,pagelimit, numForPage){  
    var maxnumpage = parseInt(pagelimit / numForPage) + 1; 
    
    for(i=1;i<=maxnumpage;i++){
      if(i==page){
        document.getElementById('ativo'+page).className = 'current';
      }else{
        document.getElementById('ativo'+i).className = '';
      }          
    }

    var strURL = '/get_pageSNIIDeia/'+page+'/'+pagelimit+'/'+numForPage;

    $.ajax({type: 'GET', url: strURL
        }).done(function(r) {
            $('#pagup').html(r);
        }).fail(function(r) {
            $('#pagup').html('Erro');
    });                  
}



//chamar pela proxima senha em espera
  function chamar_senha(ws){
      var strURL = '/chamar';
      $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
       }).done(function(r) {
            get_servicoAtendimento(ws, r);
       }).fail(function(r){
            showMSG('warning', "Actualmente não temos nenhuma senha em espera","#message","#message_container");
       });
 }

//chamar por uma senha especifica
function chamar_por_senha(ws)  {
        var numero_senha = $('#numero_senha').val();
        if(numero_senha == null || numero_senha == ""){
             showMSG('warning', "Por favor introduza a senha","#ModalCSmessage","#ModalCSmessage_container");
        }else{
            var strURL = '/chamar_por_senha/'+numero_senha;
            $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
            }).done(function(r) {
                closeModel();
                get_servicoAtendimento(ws, r);
            }).fail(function(r) {
                $('#numero_senha').val('');
                showMSG('warning', "Senha Invalida","#ModalCSmessage","#ModalCSmessage_container");
            });
        }
 }

//Chamar por uma senha especifica em espera pelo atendedor xpto
function chamar_senhaEspera(ws, senha_id,tagID) {
    var strURL = '/chamar_senhaEspera/'+senha_id;
    $.ajax({type: 'POST', url: strURL,data: $('#erpForm').serialize()
        }).done(function(r) {
            if(r == 'atendedor_ocupado'){
                showMSG('warning', "Por favor termine o atendimento actual e efectue novamente essa operação","#message","#message_container");
             }else{
                get_servicoAtendimento(ws, r);
                refreshListaEspera();
                setTime(getTime(tagID),"timer");
             }
        }).fail(function(r) {
             showMSG('alert', "Senha Invalida","#message","#message_container");
        });
}

//Chamar novamente pela senha xpto
function chamar_senhaNovamente(ws){
        sendToTv(ws);
}

//coloca uma senha em espera
function espera_senha() {
    if($('#comentario').val()){
        var strURL = '/esperar/'+$('#senha').val()+'/'+getTime("timer")+'/'+$('#comentario').val();
        $.ajax({type: 'POST', url: strURL,data: $('#erpForm').serialize()
            }).done(function(r) {
                 clickBtComentario();
                 refreshListaEspera();
                 startEsperaTime();
                 endchamada('warning','As Senha '+getSenha()+" foi adicionada a sua lista de espera");
            }).fail(function(r) {
                 showMSG('warning', "Não foi possivel colocar essa senha em espera","#ModalEsperamessage","#ModalEsperamessage_container");
            });
    }else{
         showMSG('warning', "Por favor introduza um comentario","#ModalEsperamessage","#ModalEsperamessage_container");
    }
}


//guarda/actualiza o tempo em espera na base de dados
function saveTime(tagID){
    var strURL = '/saveTime/'+$('#senha'+tagID).val()+'/'+getTime("timer"+tagID);
    $.ajax({type: "POST", url: strURL,});
}

//faz com que as senhas inicializem apartir de 1 no respectivo dia





function resetTicket(){
    var strURL = '/resetTicket';
    $.ajax({type: "POST", url: strURL,});
}



//incia uma chamada
function startchamada(r){
     refreshContent();
     set_userEstado();
     setSenha(r);
     startTime();
     showFields();
}

//termina uma chamada
function endchamada(type,message){
      refreshContent();
      defaultDocs();
      hideFields();
      stopTime();
      setTime("00:00:00","timer");
      showMSG(type,message,"#message","#message_container");
}

function getSenha(){
    senha = $('#senha').val().split(";");
    return senha[1];
}


function getIDSenha(){
    senha = $('#senha').val().split(";");
    return senha[0];
}

function getServico(){
    senha = $('#senha').val().split(";");
    return senha[2];
}

function setSenha(senha){
        $('#senha').val(senha);
        senha = senha.split(";");
        document.getElementById("Divsenha").innerText = "Senha Actual: "+senha[1];
}


function set_userEstado(){
    if($('#user_estado').val()=="terminado" || $('#user_estado').val()=="intervalo"){
          setEstado('em_servico');
          showMSG("warning","O teu estado foi Alterado para em Serviço","#message","#message_container");
    }
}

//faz o set do estado do utilizador
function setEstado(estado){
    $('#user_estado').val(estado);
}

//faz o get do numero do balcao do atendedor
function getBalcao(){
    return $('#user_balcao').val();
}

//funçao responsavel por mostrar as mensagens
function showMSG(type,content,message,message_container){
    var mymessage_container = $(message_container);
    showMessage(type, content, $(message), mymessage_container);
    mymessage_container.delay(2000).slideUp();
}

//tranferir uma senha para um servico xpto
function transferir_senha(keyservico,servico) {
    var strURL = '/transferir/'+$('#senha').val()+'/'+keyservico+'/'+servico;
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
              endchamada("warning","A Senha  "+getSenha()+" foi transferida para o Serviço "+servico);
        }).fail(function(r) {
             showMSG('alert', r.responseText,"#message","#message_container");
        });
  }

//termina uma senha
function terminar_senha() {
    var strURL = '/terminar/'+$('#senha').val()+'/'+getTime("timer");
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
             endchamada("warning","A Senha  "+getSenha()+"  terminado com sucesso");
        }).fail(function(r) {
             showMSG('alert', r.responseText,"#message","#message_container");
        });
  }

  // desistir de uma senha
  function desistir_senha() {
    var strURL = '/desistir/'+$('#senha').val()+'/'+getTime("timer");
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
              endchamada("warning","A Senha  "+getSenha()+" desistiu");
        }).fail(function(r) {
              showMSG('alert', r.responseText,"#message","#message_container");
        });
  }

  // atendedor modo intervalo
  function fazer_intervalo() {
    var strURL = '/fazer_intervalo';
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
                setEstado('intervalo');
                showMSG("warning","O seu estado foi Alterado para o modo intervalo","#message","#message_container");
        }).fail(function(r) {
                showMSG('alert', r.responseText,"#message","#message_container");
        });
  }

  // atendedor modo terminado atendimento
  function terminar_atendimento() {
    var strURL = '/terminar_atendimento';
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
        }).done(function(r) {
               setEstado('terminado');
               showMSG("warning","O seu estado foi Alterado para Atendimento Terminado","#message","#message_container");
        }).fail(function(r) {
                showMSG('alert', r.responseText,"#message","#message_container");
        });
  }

  //faz o refresh das principais divs
  function refreshContent(){
        $('#gap_fluxo').load(document.URL +  ' #gap_fluxo');
        $('#panel0').load(document.URL +  ' #panel0');
        $('#panel1').load(document.URL +  ' #panel1');
        $('#panelEspera').load(document.URL +  ' #panelEspera');
  }

  // faz o refresh apenas da lista de espera
  function refreshListaEspera(){
       $('#panelEspera').load(document.URL +  ' #panelEspera');
  }

  //fecha o model
  function closeModel(){
      $('#numero_senha').val('');
      $('#ModalCS').foundation('reveal', 'close');
  }


 //show time
//Variaveis globais necessarias para o controlo do time
var start;
var startEspera;

//actualiza o tempo de atendimento que aparece na bara do atendedor
function updateTime(){
     setTimeContent("timer");
}


//actualiza o tempo na lista de espera
function updateTimeEspera() {
    count = $('#countEspera').val();
    for(var i=0; i<count; i++){
            //set Time na lista de espera
            setTimeContent("timer"+i);
            //actualiza o respectivo tempo na base de dados
            saveTime(i);
    }
}


function setTimeContent(tagID){
  var value = String(document.getElementById(tagID).innerText);
  updatedTime = TimeManager(value);
  document.getElementById(tagID).innerText = updatedTime;
}

//Ainda nao e perfeito mas para o que precisamos da conta :)
function TimeManager(value){
  var content = value.split(":");
  var hora = parseInt(content[0]);
  var minuto = parseInt(content[1]);
  var segundos = parseInt(content[2]);

 if(segundos<59)
        segundos=segundos+1;
else if(segundos==59){
      segundos=00;
      if(minuto<59)
          minuto=minuto+1;
      else if(minuto==59){
            minuto=00;
            hora=hora+1;
      }
}

  if(segundos<10)
          segundos = "0"+segundos;
  if(minuto<10)
          minuto =  "0"+minuto;
  if(hora<10)
          hora = "0"+hora;

  return hora+":"+minuto+":"+segundos;
}

  //start time incia o tempo
  function startTime(){
    if(start)
        clearInterval(start);

     start = setInterval(updateTime, 1000); //essa funçao faz o delay em cada 1000 milisegundos actualiza o time
  }


  //stop time para o tempo
  function  stopTime(){
         clearInterval(start);
  }

  //para o tempo das senhas na lista de espera pelo atendedor
  function stopEsperaTime(){
      clearInterval(startEspera);
  }

  // inicia o tempo na lista de espera pelo atendedor
  function startEsperaTime(){
      if(startEspera)
            clearInterval(startEspera);

     startEspera= setInterval(updateTimeEspera, 1000); //essa funçao faz o delay em cada 1000 milisegundos actualiza o time
  }

  //controla o tempo das senhas em espera pelo atendedor
  function EsperaManager(){
      count = parseInt($('#countEspera').val());
      if(count>0){
          startEsperaTime();
      }else{
          stopEsperaTime();
      }
  }

  //get o time actual
  function getTime(tagID){
      return document.getElementById(tagID).innerText
  }

  //setTime faz o set do tempo
  function setTime(value,tagID){
      document.getElementById(tagID).innerText = value;
}



// faz o get do rss das noticias
function getNews(feedUrl){
        $.ajax({
                url: document.location.protocol + '//ajax.googleapis.com/ajax/services/feed/load?v=1.0&output=xml&num=10&callback=?&q=' + encodeURIComponent(feedUrl),
                  dataType : 'json',
                  success  : function (data) {
                    if (data.responseStatus == 200) {
                          var xmlDoc = $.parseXML(data.responseData.xmlString);
                          var $xml = $(xmlDoc);
                          $xml.find('item').each(function(i,p) {
                                $("#footermessage").append($(p).find('title').text()+" - "+$(p).find('description').text()+"  ");
                          });
                      }
                 }
        });
  }

//procura os rss
function searchRSS(){
      try {
              var rssfeed = ['http://www.asemana.publ.cv/spip.php?page=backend&id_mot=1&ak=1'
          ,'http://www.asemana.publ.cv/spip.php?page=backend&id_rubrique=4&ak=1'
          ,'http://www.asemana.publ.cv/spip.php?page=backend&id_rubrique=13&ak=1'
          ,'http://www.asemana.publ.cv/spip.php?page=backend&id_rubrique=5&ak=1'
          ,'http://www.asemana.publ.cv/spip.php?page=backend&id_rubrique=15&ak=1'
          ,'http://www.asemana.publ.cv/spip.php?page=backend&id_rubrique=19&ak=1'];

            for (var i = 0; i < rssfeed.length; i++) {
                         getNews(rssfeed[i]);
            }
      }
      catch(err){}
 }


//Controla a lista de reproduçao video
function videoManager(){
    var video = document.getElementById("Videotv");
    video.onended = function() {
          playerControler();
    };
}

var startimageTimer; //controla a duraçao da imagem

//Controla as Imagens que aparecem no ecran de espera
function imageManager(){
      if($('#currentTime').val()==$('#targetTime').val()){
              stopImageTime();
              $('#currentTime').val("00:00:00");
              playerControler();
      }else{
            updatedTime = TimeManager($('#currentTime').val());
            $('#currentTime').val(updatedTime);
      }
}

//Inicia a contagem do tempo da imagem
function startImageTime(){
     if(startimageTimer)
           clearInterval(startimageTimer);

     startimageTimer = setInterval(imageManager, 1000); //essa funçao faz o delay em cada 1000 milisegundos actualiza o time
}

//Para a contagem do tempo da imagem
function stopImageTime(){
      clearInterval(startimageTimer);
}

//player controler e necessario para fazer o controlo das imagens e videos a reproduzir
function playerControler() {
      var video = document.getElementById("Videotv");
      var image = document.getElementById("Imagetv");
      var count =0; // conta os elementos
      var toplay; //guarda o url do item a reproduzir :)
      var value = 4;
      var playlistsize = $("#playlistsize").val();
      playlist = String($("#playlist").val()).split(";");
      for(var i=0;i<playlistsize;i++){
             if($("#nextmultimedia").val()==playlistsize || $("#nextmultimedia").val()==0){
                    $("#nextmultimedia").val(1);
                    toplay = playlist[1];
                    break;
              }else{
                      if(count==$("#nextmultimedia").val() && $("#nextmultimedia").val()<playlistsize){
                            toplay = playlist[value-3];
                            $("#nextmultimedia").val(count+1);
                            break;
                        }
              }
              value=value+4;
              count++;
      }
      if(playlist[value-2]=='video'){
          $('#Imagetv').hide();
          $("#Videotv").show();
          video.src = toplay;
          video.play();
          videoManager();
      }else if(playlist[value-2]=='image'){
          $("#Videotv").hide();
          $('#Imagetv').show();
          $('#targetTime').val(playlist[value-1]);
          image.src = toplay;
          startImageTime();
      }
}

//Faz o set dos conteudos que aparecem na tela da tv
function setTvContent(tvcontent){
    tvcontent = tvcontent.split(";");
    for (var i = 0; i < 4; i++) {
        counter = document.getElementById("counter"+(i+1)).innerText ;
        if(counter=="" || counter == tvcontent[2]){
            document.getElementById("service"+(i+1)).innerText = tvcontent[0];
            document.getElementById("ticket"+(i+1)).innerText = tvcontent[1];
            document.getElementById("counter"+(i+1)).innerText = tvcontent[2];
            break;
        }}
}

//envia as informaçoes para a TV
function sendToTv(ws){
       // Enviar as informaçoes para a tela da tv
       ws.send(getServico()+";"+getSenha()+";"+getBalcao());
}


//retira a senha do cliente
function retiraSenha(servico,letra){
    showQuiosqueLoad();
    var strURL = '/printSenha/'+servico+'/'+letra;
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
      }).done(function(r) {
          if(r == "None"){
              hideQuiosqueLoad();
              showMSG('warning', "Serviço Indisponivel no momento","#ModalQSmessage","#ModalQSmessage_container");
          }else{
              imprimir(r);
              location.reload();
          }
      }).fail(function(r) {});
}

//essa funçao vai imprimir a senha do cliente
function imprimir(doc){
    var myTicket = window.open("", "printWindow", "width=100, height=100");
    myTicket.document.write(doc);
    //myTicket.reload();
    //myTicket.print();
    //myTicket.close();
}

//essa funçao vai esconder os buttoes do quiosque
function hideQuiosqueButton(currentButton){
      var count = $("#quiosqueElement").val();
      for(var i=0;i<count;i++){
            if(i!=currentButton){
                 $("#option"+i).css('display', 'none');
            }}
}

//get serviço em atendimento
function get_servicoAtendimento(ws,result){
    var strURL = '/servico_em_atendimento';
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
      }).done(function(r) {
           startchamada(result);
           fillDocuments(r);
           sendToTv(ws);
      }).fail(function(r) {});
}


  //mostra os campos
  function showFields(){
      $("#BtChamar").hide();
      $("#BtIntervalo").hide();
      $("#BtTerminar").hide();
      $("#BtChamarPS2").hide();
      $("#BtChamar").hide();
      $("#BtRechamar").show();
      $("#BtTransferir").show();
      $("#BtEspera").show();
      $("#BtDesistir").show();
      $("#Divsenha").show();
      $("#BtTerminarsenha").show();
      $("#DivInformativo").show(1000);
  }

  //esconde os campos
  function hideFields(){
     $("#BtRechamar").hide();
     $("#BtDesistir").hide();
     $("#BtTransferir").hide();
     $("#BtEspera").hide();
     $("#BtTerminarsenha").hide();
     $("#DivInformativo").hide(1000);
     $("#BtChamar").show();
     $("#Divsenha").hide();
     $("#BtChamarPS2").show();
     $("#BtIntervalo").show();
     $("#BtTerminar").show();
     $("#DivTransfSenha").hide(1000);
  }


  $("#BtTransferir").click(function () {
        $("#DivInformativo").hide(1000);
        $("#DivTransfSenha").show(1000);
  });



function clickBtComentario(){
    $('#ModalEspera').foundation('reveal', 'close');
    $('#comentario').val('');
    stopTime();
    hideFields();
}


function fillDocuments(docs){
      docs = String(docs).split("#");
      legislacao = docs[0];
      manual = docs[1];
      outros = docs[2];
      fillDoc(legislacao,0,5,"panel2","legislacao");
      fillDoc(manual,0,5,"panel3","manual");
      fillDoc(outros,0,5,"panel4","outros");
}

function getVoicetv(tvcontent){
    tvcontent = tvcontent.split(";");
    var strURL = '/getvoicetv/'+tvcontent[1]+'/'+tvcontent[2];
    $.ajax({type: 'POST', url: strURL, data: $('#erpForm').serialize()
      }).done(function(r) {
          playAudiotv(r,0);
      }).fail(function(r) {});
}

//essa funçao e responsavel por reproduzir o audio na TV
function playAudiotv(tvcontent,pos) {
    var audio = document.getElementById('audiotv');
    var audiosize;
    var nextaudio;
    content = tvcontent.split(";");
    audiosize= content.length;
    audio.src =  content[pos];
    audio.play();
    audio.onended = function(){
          if(pos<audiosize){
                nextaudio = pos+1;
                playAudiotv(tvcontent,nextaudio);
          }
    };
}

/*
//Somente para a nossa TV nao ficar fazia preenchemos os campos serviços
function defaultTVServices(services){
    if(services!='None'){
        services = services.split(";");
        var count = 0;
        for (var i = 0; i < services.length; i++) {
                if(count<4){
                    document.getElementById("service"+(i+1)).innerText = services[i];
                }else{
                    break;
                }
              count=count+1;
        }}
}*/

 function fillDoc(documents, page,limit,panel,type){
    var doc = String(documents).split(";");
    var count=0;
    var mylimit=0;
    var pagelength = 0;
    var value = 2;
    var docsize = doc.length-1;
    var final_page = 0;
    var nextpage = 0;
    var pages_count = 0;
    var maxpage = 0;
    var actual_page = page;
    var content;
    if(type == 'legislacao'){
        content="<h4>Introduza o nome de uma legislação: </h4><hr/><div class='row collapse'><div class='large-8 small-9 columns'>";
        content+="<input type='text' placeholder='Ex: Documento'></div><div class='large-3 small-3 columns'>";
        content+="<a href='#' class='button tiny'>Procurar</a></div></div>";
    }else if(type == 'manual'){
        content="<h4>Manuais de Apoio: </h4><hr/>";
    }else{
        content="<h4>Outros: </h4><hr/>";
    }
    content+="<ul class='side-nav'>";
    while(value<=docsize){
        if (count == page && mylimit<limit){
                content+=" <li><a href='#' onclick='window.open(\""+doc[value-1]+"\", \"_blank\", \"fullscreen=yes\"); return false;'>"+doc[value-2]+"</a></li>";
                mylimit=mylimit+1;
        }else{
            mylimit=mylimit+1;
            if(mylimit == limit){
                mylimit=0;
                count=count+1;
            }
        }
        value=value+2;
        pagelength=pagelength+1;
    }
    content+="</ul><ul class='pagination'><li class='arrow'><a href='#' onclick='fillDoc(\""+documents+"\","+0+","+limit+",\""+panel+"\",\""+type+"\")'>&laquo;</a></li>";
    if (actual_page >0){
        var backpage = actual_page-1;
        content+="<li class='arrow'><a href='#' onclick='fillDoc(\""+documents+"\","+backpage+","+limit+",\""+panel+"\",\""+type+"\")'>&lt;</a></li>";
    }
    pages_count = parseInt(pagelength/limit);
    maxpage = actual_page+limit;
    nextpage = actual_page+1;
    if(pages_count>=maxpage){
            final_page = maxpage;
    }else{
        final_page = pages_count;
    }

    for (var p = 0; p < final_page+1; p++) {
            if(p == actual_page){
                content+="<li class='current'><a href='#' onclick='fillDoc(\""+documents+"\","+p+","+limit+",\""+panel+"\",\""+type+"\")'><b>"+p+"</b></a></li>";
            }else{
                content+="<li><a href='#' onclick='fillDoc(\""+documents+"\","+p+","+limit+",\""+panel+"\",\""+type+"\")'>"+p+"</a></li>";
            }
    }
    if (actual_page < pages_count){
              content+="<li><a href='#' onclick='fillDoc(\""+documents+"\","+nextpage+","+limit+",\""+panel+"\",\""+type+"\")'>&gt;</a></li><li class='arrow'><a href='#' onclick='fillDoc(\""+documents+"\","+final_page+","+limit+",\""+panel+"\",\""+type+"\")'>&raquo;</a></li></ul>";
    }else{
        content+="<li><a href='#' onclick='fillDoc(\""+documents+"\","+0+","+limit+",\""+panel+"\",\""+type+"\")'>&gt;</a></li><li class='arrow'><a href='#' onclick='fillDoc(\""+documents+"\","+0+","+limit+",\""+panel+"\",\""+type+"\")'>&raquo;</a></li></ul>";
    }
    $("#"+panel).html(content);
 }


 function defaultDocs(){
        var content;
        content="<h4>Introduza o nome de uma legislação: </h4><hr/><div class='row collapse'><div class='large-8 small-9 columns'>";
        content+="<input type='text' placeholder='Ex: Documento'></div><div class='large-3 small-3 columns'>";
        content+="<a href='#' class='button tiny'>Procurar</a></div></div>";
        $("#panel2").html(content);
        $("#panel3").html("<h4>Manuais de Apoio: </h4><hr/>");
        $("#panel4").html("<h4>Outros: </h4><hr/>");
 }

 //Mostra a imagem de loading no quiosque
 function showQuiosqueLoad(){
      $("#myloadingDiv" ).show();
 }

 //Esconde a imagem do loading no quiosque
 function hideQuiosqueLoad(){
     $("#myloadingDiv" ).hide();
 }

//responsavel pelo controlo da lista de espera
EsperaManager();




//funçao chamada form sni_ideia registro<
function registIdeia(){
  //alert(String($('#formIdeia').serialize()));
    $.ajax({
        type: 'POST',
        url: "/registIdeia",
        data: $('#formIdeia').serialize()
    })
}

//funçao chamada form sni_pessoa registro<
function registPessoa(){
    $.ajax({
        type: 'POST',
        url: "/registPessoa",
        data: $('#formLogin').serialize()
    })
}
