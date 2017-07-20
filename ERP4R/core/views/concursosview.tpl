% setdefault('dadosrespEsclare', '')
% setdefault('dadosconcursView', '')

<!doctype html>
<!--[if IE 9]><html class="lt-ie10" lang="en" > <![endif]-->
<html class="no-js" lang="en" data-useragent="Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)">
  <head>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <link rel="shortcut icon" href="/static/images/iconcp.png" />
    <title> Compras Públicas | Ministério das Finanças</title>

    <link rel="stylesheet" href="/static/css/normalize.css">
    <link rel="stylesheet" href="/static/css/foundation.css"/>
    <script src="/static/js/modernizr.js"></script>

    <link href="/static/css/cp_foundation.min.css" rel="stylesheet">
    <link href="/static/css/foundation.min.css" rel="stylesheet">
    <link href="/static/css/normalize.css" rel="stylesheet">
    <link href="/static/css/foundation-icons.css" rel="stylesheet">
    <link href="/static/css/cp_app.css" rel="stylesheet">
  </head>
  <body>
    <nav class="top-bar" data-topbar role="navigation">
      <ul class="title-area">
        <li class="name">
          <a href="#"><img src="/static/images/LogoMFP.png" alt="Loga" /></a>
        </li>
         <!-- Remove the class "menu-icon" to get rid of menu icon. Take out "Menu" to just have icon alone -->
        <li class="toggle-topbar menu-icon"><a href="#"><span>Menu</span></a></li>
      </ul>

      <div class="middle tab-bar-section">
        <h1 class="titulo">Compras Públicas</h1>
      </div>

      <section class="top-bar-section">
        <ul class="right" style="margin-right:50px;">
          <!--<li><a href="#">Calendário</a></li> <li class="divider"></li>
          <li><a href="#">Sobre CP</a></li> <li class="divider"></li>-->
          <li><a href="#">Contatos</a></li> <li class="divider"></li>
          <!--<li><a href="#" data-toggle="modal" data-target="#myModalRegisto">Registrar</a></li> <li class="divider"></li>-->
          <li><a href="/login" target="_blank" >Entrar</a></li>
          <!--
          <li><a href="#"><i class="fi-social-facebook medium"></i></a></li>
          <li><a href="#"><i class="fi-social-twitter medium"></i></a></li>
          <li><a href="#"><i class="fi-social-linkedin large"></i></a></li>
          <li><a href="#"><i class="fi-social-dribbble medium"></i></a></li>
        -->
        </ul>
      </section>
    </nav>

    <nav>
      <div class="twelve columns header_nav">
        <div class="row">
          <ul id="menu-header" class="nav-bar horizontal">
            <li class="active"><a href="/cms">Início</a></li>
            <li class=""><a href="/Fornecedores">Fornecedores</a></li>
            <li class=""><a href="/Entidade_publica">Entidade pública</a></li>
            <li class=""><a href="/Contratos">Contratos</a></li>
            <li class="has-flyout">
             <a href="#" data-options="align:left" data-dropdown="drop">Documentos de Apoio</a><a href="#" class="flyout-toggle"></a>
              <ul id="drop" class="flyout"><!-- Flyout Menu -->
                <li class="has-flyout"><a href="/Legislacao">Legislação</a></li>
                <li class="has-flyout"><a href="/Directiva">Directivas</a></li>
                <li class="has-flyout"><a href="/Mapa_do_site">Mapa do site</a></li>
                <li class="has-flyout"><a href="/Manual">Manuais</a></li>
                <li class="has-flyout"><a href="/DocEstandarizados">Documentos Estandarizados</a></li>
                <li class="has-flyout"><a href="/DeclaracoesFornecedores">Declarações dos Fornecedores</a></li>
                <!--li class="has-flyout"><a href="/Faq">FAQ</a></li-->
              </ul>
            </li><!-- END Flyout Menu -->
          </ul>
          <script type="text/javascript">
           //<![CDATA[
           $('ul#menu-header').nav-bar();
            //]]>
          </script>
        </div>
      </div>
    </nav>

    % for ddcv in dadosconcursView:
    %   varIdconcur = ddcv['id']
    %   varNumero = ddcv['numero']
    %   varCodig = ddcv['codigoprocediment']
    %   varDesgn = ddcv['desgn']
    %   varAdjudic = ddcv['adjudicantenome']
    %   varDataInicio = ddcv['data_inicio']
    %   varDataEsclareciment = ddcv['data_limit_esclar']
    %   varDataEnteDoc = ddcv['data_ente_doc']
    %   varDataAtoPublic = ddcv['data_acto_publico']
    %   varTipoContt = ddcv['tipo_contt']
    %   varTipoConcurso = ddcv['tipo_c']
    %   varDescricao = ddcv['textomotivocancelar']
    %   varAcessodoc = ddcv['acessodoc']
    %   varTextoacessodoc = ddcv['textoacessodoc']
    %   varLeiAplicavel = ddcv['leiaplicavel']
    %   varEstado = ddcv['estado']
    %   break
    % end

    <div class="row">
      <div class="large-12 columns">
        <div class="row">
          <ul class="breadcrumbs">
            <li><a href="#">Início</a></li>
            <li><a href="#">Concursos</a></li>
            <!--<li class="unavailable"><a href="#">Gene Splicing</a></li>-->
            <li class="current"><a href="#">ver&{{varDesgn}}</a></li>
          </ul>
        </div>
      </div>
    </div>


    <div class="row">
      <div class="large-12 columns">
        <div class="row">

          <div class="row">
            <div class="large-6 columns">
              <!--<img src="http://placehold.it/500x500&text=Image"><br>-->
              <div class="panel">
                <h6>Objeto do Contrato:</h6>
                <h7 class="subheader">{{varDesgn}}</h7>
              </div>
              <div class="panel">
                <h6>Entidade Adjudicante:</h6>
                <h7 class="subheader">{{varAdjudic}}</h7>
              </div>
              <div class="row">
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Tipo Procedimento:</h6>
                    <h7 class="subheader">{{varTipoConcurso}}</h7>
                  </div>
                </div>
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Código Procedimento:</h6>
                    <h7 class="subheader">{{varCodig}}</h7>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Tipo Contrato:</h6>
                    <h7 class="subheader">{{varTipoContt}}</h7>
                  </div>
                </div>
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Data Publicação:</h6>
                    <h7 class="subheader">{{varDataInicio}}</h7>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Prazo Esclarecimento:</h6>
                    <h7 class="subheader">{{varDataEsclareciment}}</h7>
                  </div>
                </div>
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Data Entrega das Propostas:</h6>
                    <h7 class="subheader">{{varDataEnteDoc}}</h7>
                  </div>
                </div>
              </div>
              <div class="row">
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Data Acto Público:</h6>
                    <h7 class="subheader">{{varDataAtoPublic}}</h7>
                  </div>
                </div>
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Lei Aplicável:</h6>
                    <h7 class="subheader">{{varLeiAplicavel}}</h7>
                  </div>
                </div>
              </div>
            </div>

            <div class="large-6 columns">
              <div class="panel">
                <h6>Financiado Por:</h6>
                % for df in dadosrespFinaciadProced:
                <h7 class="subheader">{{df['financiadornome']}}</h7><br/>
                % end
              </div>
              <h3 class="show-for-small">Observação</h3>
              <div class="panel">
                <h4 class="hide-for-small" style="margin-bottom:20px;">Observação</h4><hr/>
                  % if(varEstado == 'cancelado'):
                    <h5 class="subheader">{{varDescricao}}</h5>
                  % else:
                  %   for do in dadosrespObservaProced:
                        <h5 class="subheader">{{do['observacao']}}</h5>
                  %     break
                  %   end
                  % end
              </div>
            </div>
          </div>

          <div class="large-12 columns">
            <div class="row">
              <div class="title">
                <span class="content-title">Documentos do Concurso</span>
                <hr />
              </div>
              <div class="large-12 columns">
                 <table class="large-12 columns">
                      <thead>
                        <tr>
                          <th></th>
                          <th>Tipo Documento</th>
                          <th>Data de publicação</th>
                        </tr>
                      </thead>
                      <tbody>

                        % i = 0
                        % for ddoc in dadosrespDocProced:
                        %   alterBackg = ''
                        %   i +=1
                        %   resto = i % 2
                        %   if(resto == 0):
                        %     alterBackg = 'background-color: #EEEEEE'
                        %   end
                        %   print(">>>>>>>>>>>>>>>>>>>>>>>>> "+varAcessodoc+" <<<<<<<<<<<<<<<<<<<<")
                        %   if(((varAcessodoc == 'Pago') and (ddoc['nomedocument'] == 'Anuncio do Concurso')) or ((varAcessodoc == 'Pago') and (ddoc['nomedocument'] == 'Anexo de Anuncio')) or ((varAcessodoc == 'Pago') and (ddoc['nomedocument'] == 'Documento Retificado'))):
                        <tr style="{{alterBackg}}">

                            <td>
                              <a href="{{ddoc['doc_ficheiro']}}" onclick="openPdf(event, '{{ddoc['doc_ficheiro']}}', 'newpage.html');" style="background: none !important;">
                                %   if(ddoc['tipo'] == "Pdf"):
                                <img src="/static/images/PdfLogo.jpg" width="24" height="24"/>
                                %   end
                                %   if(ddoc['tipo'] == "Word"):
                                <img src="/static/images/WordLogo.png" width="24" height="24"/>
                                %   end
                                %   if (ddoc['tipo'] == "Excel"):
                                <img src="/static/images/ExcelLogo.png" width="24" height="24"/>
                                %   end
                              </a>
                            </td>
                            <td>{{ddoc['nomedocument']}}</td>
                            <td>{{ddoc['date_create']}}</td>
                        </tr>
                        %   elif(varAcessodoc == 'Gratuito'):
                        <tr style="{{alterBackg}}">
                            <td>
                              <a href="{{ddoc['doc_ficheiro']}}" onclick="openPdf(event, '{{ddoc['doc_ficheiro']}}', 'newpage.html');" style="background: none !important;">
                                %   if(ddoc['tipo'] == "Pdf"):
                                <img src="/static/images/PdfLogo.jpg" width="24" height="24"/>
                                %   end
                                %   if(ddoc['tipo'] == "Word"):
                                <img src="/static/images/WordLogo.png" width="24" height="24"/>
                                %   end
                                %   if (ddoc['tipo'] == "Excel"):
                                <img src="/static/images/ExcelLogo.png" width="24" height="24"/>
                                %   end
                              </a>
                            </td>
                            <td>{{ddoc['nomedocument']}}</td>
                            <td>{{ddoc['date_create']}}</td>
                        </tr>
                        %   end
                        % end
                      </tbody>
                    </table>
              </div>
            </div>
              %   if(varAcessodoc == 'Pago'):
              <div data-alert class="alert-box warning round">
                {{varTextoacessodoc}}
                <a href="#" class="close">&times;</a>
              </div>
              <br />
              %   end
          </div>

          <!--
          <div class="row">
            <div class="large-12 columns">
              <div class="radius panel">
                <form>
                  <div class="row collapse">
                    <div class="large-10 small-8 columns">
                      <input type="text"/>
                    </div>
                    <div class="large-2 small-3 columns">
                      <a href="#" class="postfix button expand"><i class="fi-magnifying-glass"></i>
Pesquisa </a>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
          -->

          <!-- ############################################################################################### -->
            <div class="row">
              <div class="large-12 columns">
              <hr/>
                <div class="large-6 columns" style="padding:0px !important; margin:0px !important;">
                  <h1 style="padding:0px !important; margin:0px !important;">Esclarecimento</h1>
                </div>
                <div class="large-6 columns" style="padding:0px !important; margin:0px !important;">
                  <div class="inline-list right" style="padding:0px !important; margin:0px !important;">
                    <a href="#"  class="button radius alert" data-reveal-id="myModal">Pedir esclarecimento</a>
                  </div>
                </div>
                <hr/>
              </div>
            </div>


            <div id="myModal" class="reveal-modal" data-reveal aria-labelledby="modalTitle" aria-hidden="true" role="dialog">

              <div id="mnsconfr" class="row">
              </div>
              <div id="mnsconfr2" class="row">
              </div>
              <h3>Esclarecimento</h3>
              <p>Espaço reservado a reclamação, observação, sugestão e/ou pedido de esclarecimento;</p>

              <section class="section">
                <h5 class="title"><a href="#panel1">Pedido de esclarecimento</a></h5>
                <div class="content" data-slug="panel1">
                  <form id="form_registesclarecimt">

                    <div class="row collapse">
                      <div class="large-4 columns">
                        <label style="margin-right: 20px !important;">Nome
                          <input type="text" id="nomeFornec" name="nomeFornec" placeholder="Nome fornecedor" />
                        </label>
                      </div>
                      <div class="large-4 columns">
                        <label style="margin-right: 10px !important;">NIF
                          <input type="text" id="nifFornec" name="nifFornec" placeholder="NIF fornecedor" />
                        </label>
                      </div>
                      <div class="large-4 columns">
                        <label style="margin-left: 10px !important;">Contato
                          <input type="text" id="contatFornec" name="contatFornec" placeholder="Contato fornecedor" />
                        </label>
                      </div>


                      <div class="large-2 columns">
                        <label class="inline"> Assunto</label>
                      </div>
                      <div class="large-10 columns">
                        <input type="text" id="esclrassunto" name="esclrassunto" placeholder="Assunto" />
                      </div>

                    </div>

                    <div class="row collapse">
                      <label>Esclarecimento:</label>
                      <textarea rows="6" id="esclrtest" name="esclrtest" style="height: 120px !important;"></textarea>
                    </div>
                    <input type="hidden" id="referencProcedimet" name="referencprocedimet" VALUE="{{varIdconcur}}" />

                    <input type="hidden" id="esclrEstado" name="esclrestado" VALUE="Pendente" />

                    <!--<button type="submit" class="radius button" onClick="regist_esclareciment();">Enviar</button>-->
                    <span class="radius button" onClick="regist_esclareciment();">Enviar</span>

                  </form>
                </div>
              </section>
              <a class="close-reveal-modal" aria-label="Close">&#215;</a>
            </div>

            <div class="row">
              <!--
              <div class="large-3 columns ">
                <div class="panel">
                  <h5><a href="#">Titulo do filtro</a></h5>
                  <div class="section-container vertical-nav" data-section data-options="deep_linking: false; one_up: true">
                    <section class="section">
                      <h5 class="title"><a href="#">Filtro 1</a></h5>
                    </section>
                    <section class="section">
                      <h5 class="title"><a href="#">Filtro 2</a></h5>
                    </section>
                    <section class="section">
                      <h5 class="title"><a href="#">Filtro 3</a></h5>
                    </section>
                    <section class="section">
                      <h5 class="title"><a href="#">Filtro 4</a></h5>
                    </section>
                    <section class="section">
                      <h5 class="title"><a href="#">Filtro 5</a></h5>
                    </section>
                    <section class="section">
                      <h5 class="title"><a href="#">Filtro 6</a></h5>
                    </section>
                  </div>
                </div>
              </div>
             -->

              <div class="large-12 columns">

                %   numeroResposta = 0
                %   for ddesc in dadosrespEsclare:
                %     numeroResposta += 1
                <div class="row">
                  <div class="large-1 columns small-3"><h1 style="padding: 1.55rem;">{{numeroResposta}}</h1></div>
                  <div class="large-11 columns">
                    <p style="margin-bottom: 0.25rem !important;"><strong>{{ddesc['assunto']}}:</strong> {{ddesc['pedidoesclarecimento']}}</p>
                     <span style="color:#CCCCCC;">{{ddesc['date_create']}}</span>

                    <h6 style="margin: 0.75rem 0 0 0.75rem !important;"><b>Resposta:</b></h6>
                    <div class="row" style="margin: 0 0 0 0.75rem !important;">
                      <!--<div class="large-2 columns small-3"><img src="http://placehold.it/50x50&text=[img]"/></div>-->
                      <div class="large-12 columns"><p style="margin-bottom: 0.25rem !important;">{{ddesc['respostaesclarecimento']}}</p></div>
                       <span style="color:#CCCCCC;">{{ddesc['respostadate']}}</span>
                    </div>

                  </div>
                </div>

                <hr/>
                %   end
                 <!--
                <div class="row">
                  <div class="large-12 columns">
                    <p><strong>Some Person said:</strong> Bacon ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit, dolore aliqua non est magna in labore pig pork biltong.</p>
                    <ul class="inline-list">
                      <li><a href="">Reply</a></li>
                      <li><a href="">Share</a></li>
                    </ul>
                    <h6><b>Resposta:</b></h6>
                    <div class="row">
                      <div class="large-12 columns"><p>Bacon ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit</p></div>
                    </div>
                  </div>
                </div>

                <hr/>

                <div class="row">
                  <div class="large-12 columns">
                    <p><strong>Some Person said:</strong> Bacon ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit, dolore aliqua non est magna in labore pig pork biltong.</p>
                    <ul class="inline-list">
                      <li><a href="">Reply</a></li>
                      <li><a href="">Share</a></li>
                    </ul>
                    <h6><b>Resposta:</b></h6>
                    <div class="row">
                      <div class="large-12 columns"><p>Bacon ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit</p></div>
                    </div>
                  </div>
                </div>
               -->
              </div>

             <!--
            <aside class="large-3 columns hide-for-small">
            <p><img src="http://placehold.it/300x440&text=[ad]"/></p>
            <p><img src="http://placehold.it/300x440&text=[ad]"/></p>
            </aside>
          -->
            </div>
          <!-- ############################################################################################### -->

        </div>
      </div>
    </div>


    <section id="bottom">

       <div class="row">
          <div class="large-3 columns">
              <div class="widget">
                  <h3>Compras Públicas</h3>
                  <ul>
                      <li><a href="/cms">Início</a></li>
                      <li><a href="/Fornecedores">Fornecedores</a></li>
                      <li><a href="/Entidade_publica">Entidade pública</a></li>
                      <li><a href="/Contratos">Contratos</a></li>
                      <li><a href="#">Documentos de apoio</a></li>
                      <!--<li><a href="#">Links</a></li>
                      <li><a href="#">FAQ</a></li>-->
                  </ul>
              </div>
          </div><!--/.col-md-3-->

          <div class="large-4 columns">
              <div class="widget">
                  <h3>Assine a nossa lista</h3>
                  <p style="color: white;">Regista na nossa newsletter e receba anúncios das compras e contratação publicas</p>
                  <form action="" method="POST" role="form">
                      <div class="form-group">
                          <input type="text" class="form-control" id="" placeholder="Seu email...">
                      </div>
                      <button type="submit" class="btn btn-primary">Registar</button>
                  </form>
              </div>
          </div><!--/.col-md-3-->

          <div class="large-5 columns">
              <div class="widget">
                  <h3>Contactos</h3>
                  <ul>
                     <li><a href="#"><i class="fi-telephone"></i> - Dúvidas do Negócio -(+238) 260 74 71</a></li>
                      <li><a href="#"><i class="fi-telephone"></i> - Dúvidas do Site -(+238) 260 75 59 ou 260 76 07</a></li>
                      <li><a href="#"><i class="fi-telephone"></i> - Fax (+238) 260 75 07</a></li>
                      <li><a href="#"><i class="fi-telephone"></i> - Email - ums-suporte@minfin.gov.cv</a></li>
                      <li><a href="#" data-reveal-id="myModalHelp"><i class="fi-info"></i> - Serviço de helpdesk</a></li>
                      <li><a href="#"><i class="fi-marker"></i> - Av. Amilcar Cabral
                        Cidade da Praia
                        Ilha de Santiago
                        Cabo Verde</a></li>
                  </ul>
              </div>
          </div><!--/.col-md-3-->
      </div>
 </section><!--/#bottom-->

      <div id="myModalHelp" class="reveal-modal" data-reveal aria-labelledby="modalTitle" aria-hidden="true" role="dialog">
        <section class="section">
                <h5 class="title" style="text-align: center;"><a href="#panel1">Serviço de helpdesk</a></h5>
                <hr/>
                <div data-alert class="alert-box info radius">
                  A resposta a este pedido de esclarecimento será enviada para o email indicado!
                  <a href="#" class="close">&times;</a>
                </div>
                <div class="content" data-slug="panel1">
                  <form id="form_registhelp">

                    <div class="row collapse">
                      <div class="large-2 columns">
                        <label class="inline"> Email</label>
                      </div>
                      <div class="large-10 columns">
                        <input type="text" id="emailHelp" name="emailHelp" placeholder="Email" />
                      </div>
                    </div>

                    <div class="row collapse">
                      <div class="large-2 columns">
                        <label class="inline"> Assunto</label>
                      </div>
                      <div class="large-10 columns">
                        <input type="text" id="assuntoHelp" name="assuntoHelp" placeholder="Assunto" />
                      </div>
                    </div>

                    <div class="row collapse">
                      <div class="large-2 columns">
                        <label class="inline"> Tipo </label>
                      </div>
                      <div class="large-10 columns">
                       <select id="tipohelp" name="tipohelp" class="tipohelp">
                        <option value="Microempresa">Negocio</option>
                        <option value="Media Empresa">Informático</option>
                        <option value="Pequena Empresa">Funcionalidades</option>
                        <option value="Grande Empresa">Usabilidade</option>
                      </select>
                      </div>
                    </div>

                    <div class="row collapse">
                      <label>Pedido de esclarecimento:</label>
                      <textarea rows="6" id="testHelp" name="testHelp" style="height: 120px !important;"></textarea>
                    </div>

                    <input type="hidden" id="estadoHelp" name="estadoHelp" VALUE="pendente" />

                    <button type="submit" class="radius button" onClick="regist_help();">Enviar</button>
                  </form>
                </div>
              </section>
        <a class="close-reveal-modal" aria-label="Close">&#215;</a>
      </div>

    <footer class="footer">


        <div class="row">
          <div class="large-6 columns">
            <p style="color: white;">© Copyright - 2015. Compras Públicas.</p>
          </div>
          <div class="large-6 columns">
            <ul class="inline-list right">
              <li>
                <a href="#" style="color: white;">Contatos</a>
              </li>
              <li>
                <a href="#" style="color: white;">Entrar</a>
              </li>
            </ul>
          </div>
        </div>


    </footer>

  <script src="/static/js/foundation.orbit.js"></script>
  <script>
    document.write('<script src=js/vendor/' +
    ('__proto__' in {} ? 'zepto' : 'jquery') +
    '.js><\/script>')
    </script>

  <script src="/static/js/jquery.js"></script>
  <script src="/static/js/foundation.min.js"></script>
  <script src="/static/js/foundation.tab.js"></script>
  <script>
    $(document).foundation();
  </script>

  <script src="/static/js/foundation.js"></script>
  <script>
    $(document).foundation();

    var doc = document.documentElement;
    doc.setAttribute('data-useragent', navigator.userAgent);
  </script>


  <!-- Included JS Files (Compressed) -->
  <script src="/static/js/cp_foundation.min.js" type="text/javascript"></script>
  <!-- Initialize JS Plugins -->
  <script src="/static/js/cp_app.js" type="text/javascript"></script>

  <script type="text/javascript">

    function regist_esclareciment() {

      var Nome = document.getElementById('nomeFornec').value;
      var Nif = document.getElementById('nifFornec').value;
      var Contato = document.getElementById('contatFornec').value;
      var Assunto = document.getElementById('esclrassunto').value;
      var Esclareciment = document.getElementById('esclrtest').value;
      var Estado = document.getElementById('estadoHelp').value;
      var ProcedtId = document.getElementById('referencProcedimet').value;
      
      var strURL = '/registEsclareciment/'+Nome+'/'+Nif+'/'+Contato+'/'+Assunto+'/'+Esclareciment+'/'+Estado+'/'+ProcedtId;
           
      $.ajax({type: "GET", url: strURL
          }).done(function(r) {
           $('#mnsconfr').html('<br /><div data-alert class="alert-box success radius">O seu pedido de esclarecimento foi enviado com sucesso!<a href="#" class="close">&times;</a></div>');
           $('#mnsconfr2').html('<div data-alert class="alert-box info radius">  Para que conste como fornecedor do Estado é favor cadastrar no separador Fornecedores!<a href="#" class="close">&times;</a></div>');

           document.getElementById("form_registesclarecimt").reset();

          //alert(r);
      }).fail(function(r) {
          alert('False');
      });

  }
  </script>

  <script type="text/javascript">
     function regist_newsletter() {
      var strURL = '/registoNewsletter';

      $.ajax({type: 'POST', url: strURL, data: $('#form_newsletter').serialize()
          }).done(function(r) {
              alert(r);
          }).fail(function(r) {
              alert('False');
          });

    }
  </script>

  </body>
</html>
