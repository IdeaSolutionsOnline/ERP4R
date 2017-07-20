%setdefault('logotipo', '')
%setdefault('favicon', '')
%setdefault('window_id', '')
%setdefault('servicos', [])
%setdefault('title','')
<!doctype html>
<html lang="pt">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{{title}}</title>
        <link rel="stylesheet" href="/static/css/foundation.css" />
        <link rel="stylesheet" href="/static/css/gap.css" />
        <link rel="shortcut icon" href="/static/{{favicon}}">
    </head>
    <body>
        <input name="window_id" type="hidden" id="window_id" value="{{window_id}}"></input>
        <div id='myloadingDiv' style='position:absolute; top:0px; left:0px; z-index: 100; height: 100%; width: 100%; display:flex; vertical-align:middle; text-align:center; background: #fff; filter:alpha(opacity=55); opacity:.55;
             color: #000;'>
             <div style="display:block; margin:auto;">
              Aguarde ...  <br><br>
              <img style="height: 50%; width: 50%" src='/static/images/loading-animation.gif'/>
              </div>
        </div>
        <div class="row">
            <div id="CabeçalhoQuiosque" class="panel large-12 medium-12 small-12">
                <h6 id="TextoSenha"><img src="/static/{{!logotipo}}"/></h6>
            </div>
        </div>
        <div class="row">
            <div class="large-12 medium-12 small-12 columns">
                 <div data-alert  id="ModalQSmessage_container" style="display:none" class="alert-box info radius">
                    <div id="ModalQSmessage" style="color:black;"></div>
                    <a href="#" class="close">&times;</a>
                 </div>
                <ul class="accordion" data-accordion role="tablist">
                    %count = 0
                    %for servico in servicos:
                        %servico = str(servico).split(";")
                        %if str(servico[3])=='None':
                            %servicoID = servico[0]
                            %hassubservico = False
                            %for subservico in servicos:
                                  %subservico = str(subservico).split(";")
                                  %if subservico[3] == servicoID:
                                        %hassubservico = True
                                        %break
                                  %end
                              %end
                          <li id="linha" class="accordion-navigation">
                            % if hassubservico == True:
                                    <a href="#panel{{count}}d" role="tab" id="option{{count}}" onClick="hideQuiosqueButton('{{count}}');" aria-controls="panel{{count}}d" style="background: #2196f3;-webkit-box-shadow: 0px 1px 15px -3px rgba(0,0,0,0.72); -moz-box-shadow: 0px 1px 15px -3px rgba(0,0,0,0.72);box-shadow: 0px 1px 15px -3px rgba(0,0,0,0.72);"><h4 id="FontCategoria"><b>{{servico[1]}} - {{servico[2]}}</b></h4></a>
                                    <div id="panel{{count}}d" class="content button-group" role="tabpanel" aria-labelledby="panel{{count}}d-heading">
                                     %for subservico in servicos:
                                          %subservico = str(subservico).split(";")
                                            %if subservico[3] == servicoID:
                                                <a id="FontSubservico" class="expand button" onClick="retiraSenha('{{subservico[2]}}','{{servico[1]}}');">{{subservico[2]}}</a>
                                            %end
                                    %end
                                   <a class="expand button" onClick="window.location.href=window.location.href" id="botaoVoltar">Voltar Menu Principal</a>
                                   </div></li>
                           %end
                           %if hassubservico == False:
                                <a href="#panel{{count}}d" style="background: #2196f3;-webkit-box-shadow: 0px 1px 15px -3px rgba(0,0,0,0.72);-moz-box-shadow: 0px 1px 15px -3px rgba(0,0,0,0.72);box-shadow: 0px 1px 15px -3px rgba(0,0,0,0.72);"
                                 id="option{{count}}" onClick="retiraSenha('{{servico[2]}}','{{servico[1]}}');"><h4 id="FontCategoria"><b>{{servico[1]}} - {{servico[2]}}</b></h4></a>
                                </li>
                           %end
                           %count+=1
                           <li id="espaço">
                                <h6 id="espaço"></h6>
                           </li>
                        %end
                    %end
                </ul>
                <input  name="quiosqueElement"  id="quiosqueElement" type="hidden" value="{{count}}" ></input>
            </div>
        </div>
        <br>
       </div>
        <script src="/static/js/jquery.js"></script>
        <script src="/static/js/foundation.min.js"></script>
        <script src="/static/js/modernizr.js"></script>
        <script src="/static/js/erp.js"></script>
        <script src="/static/js/gap.js"></script>
        <script>
             $(document).foundation();

             window.onload = $(document).ready(function () {
                    hideQuiosqueLoad();
              });

        </script>
    </body>
</html>