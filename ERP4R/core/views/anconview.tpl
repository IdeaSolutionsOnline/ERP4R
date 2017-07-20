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

    
    <style type="text/css">

      .title hr{
        border-width: 3px 0 0;
        padding-top: 0 !important;
        margin-top: 0 !important;
        border-color: #0784a9 !important;
      }
      .content-title {
          width: 100%;
          padding-bottom: 0 !important;
          margin-bottom: 0px !important;
          padding-left: 5px;
          padding-right: 5px;
          padding-top: 3px;
          background: #0784a9;
          color: #FFF;
      }

      .top-bar {
        background: #0784a9 !important;
        height: 35px !important;
        line-height: 35px !important;
      }  

      .top-bar ul {
        height: 35px !important;
        line-height: 35px !important;
      }

      .top-bar-section li:not(.has-form) a:not(.button){
          background: #0784a9 !important;
          line-height: 35px !important;
          padding: 0 5px !important;
      }

      .divider {
          /*color: white;*/
          background: #0784a9 !important;
          /*line-height: 35px !important;*/
      }

      .top-bar-section ul {
          background: #0784a9 !important;
          line-height: 35px !important;
          display: block;
          font-size: 16px;
          height: auto;
          margin: 0;
          
          /**/
      }
      .top-bar-section ul li{
        line-height: 35px !important;

      }

      .top-bar-section > ul > .divider, .top-bar-section > ul > [role="separator"] {
        border-bottom: medium none;
        margin-top: 8px;
        border-top: medium none;
        border-right: 1px solid #FFF;
        clear: none;
        height: 18px;
        background: #0784a9 !important;
      }

      .top-bar-section ul li a > i {
        font-size: 1.2rem;
      }

      .header_nav {
          background: #0d6d96 none repeat scroll 0 0;
          box-shadow: 0 4px 2px -2px rgba(34, 25, 25, 0.6);
          padding: 15px 0 0;
          z-index: 5;
          margin-bottom: 15px;
      }

      .top-bar .title-area {
          
          z-index: 6  !important;
      }

      .name a img{
        width: 112px;
        height: 63px;
        margin: 10px !important;
      }

      .nav-bar {margin-top: 0; background: none}
      .nav-bar > li {border: 0; padding: 0; font-family: 'Open Sans Condensed',sans-serif; letter-spacing: 1px; box-shadow: none}
      .nav-bar > li > a:first-child {font-size: 16px; text-transform: uppercase; padding: 0 25px}
      .nav-bar > li:last-child {border: 0; box-shadow: none}
     /* .nav-bar > li.active:hover { background: #000; cursor: default; }{}*/
      .nav-bar > li:hover { background: #eeeeee; color: #0d6d96;         
              -webkit-transition: all .2s ease-in-out;
              -moz-transition: all .2s ease-in-out;
              -ms-transition: all .2s ease-in-out;
              -o-transition: all .2s ease-in-out;
              transition: all .2s ease-in-out; 
      }

      .nav-bar > li > a { color: #FAFAFA}
      .nav-bar > li > a:hover { color: #0d6d96;}
      .active a {background:#2ba6cb; color: #FFF}

      .nav-bar > li.has-flyout > a:first-child:after { content: ""; display: block; width: 0; height: 0; border: solid 5px; border-color: #e0e0e0 transparent transparent transparent; position: absolute; right: 20px; top: 17px; }

      .nav-bar > li.has-flyout > a:hover:first-child:after { content: ""; display: block; width: 0; height: 0; border: solid 5px; border-color: #e0e0e0 transparent transparent transparent; position: absolute; right: 20px; top: 17px; }


      .flyout {background: #FAFAFA; border-radius: 5px; border: 0; margin-top: -1px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.7);}

      ul.flyout li, .nav-bar li ul li { border-left: 0}
      ul.flyout li a, .nav-bar li ul li a { background: #FAFAFA; color:#0d6d96; border: 0; font-size: 16px;}
      ul.flyout li a:hover, .nav-bar li ul li a:hover { background: #0d6d96; color: #fff; border: 0;         
              -webkit-transition: all .2s ease-in-out;
              -moz-transition: all .2s ease-in-out;
              -ms-transition: all .2s ease-in-out;
              -o-transition: all .2s ease-in-out;
              transition: all .2s ease-in-out; 
          }
          /*
        .panel {
            background: #FFFFFF;
            border-color: #d8d8d8;
            border-style: solid;
            border-width: 1px;
            margin-bottom: 1.25rem;
            padding: 0.15rem !important;
            margin: 0.15rem !important;
            box-shadow: 6px 5px 5px rgba(34, 25, 25, 0.26);
        }
*/

        ul.breadcrumbs li a, ul.breadcrumbs li span {
          font-size: 0.65rem !important;
        }
        #bottom{
          background: #767577; 
          margin: 0;
          padding-top: 20px;
        }

        #bottom h3{
          color: #fff;
          font-size: 22px;
          margin-bottom: 10px;
          margin-top: 0;
          text-transform: uppercase;
        }
        #doclink ul li, #bottom ul li {
            display: block;
            padding: 5px 0;
        }

        #bottom ul li a{
            color: #FFF;
        }

        .panel{
          padding: 0.55rem !important;
        }

      

    </style>

  </head>
  <body>         
    <nav class="top-bar" data-topbar role="navigation">
      <ul class="title-area">
        <li class="name">
          <a href="#"><img src="/static/images/logocpmin.png" alt="Loga" /></a>
        </li>
         <!-- Remove the class "menu-icon" to get rid of menu icon. Take out "Menu" to just have icon alone -->
        <li class="toggle-topbar menu-icon"><a href="#"><span>Menu</span></a></li>
      </ul>
      <section class="top-bar-section">
        <ul class="right" style="margin-right:50px;">
          <!--<li><a href="#">Calendário</a></li> <li class="divider"></li>
          <li><a href="#">Sobre CP</a></li> <li class="divider"></li>-->
          <li><a href="#">Contatos</a></li> <li class="divider"></li>
          <!--<li><a href="#" data-toggle="modal" data-target="#myModalRegisto">Registrar</a></li> <li class="divider"></li>-->
          <li><a href="#" data-toggle="modal" data-target="#myModal">Entrar</a></li>
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
            <li class="active"><a href="/">Início</a></li>
            <li class=""><a href="ter">Fornecedores</a></li>
            <li class=""><a href="lk">Entidade pública</a></li>
            <li class=""><a href="new">Contratos</a></li>      
            <li class="has-flyout">
             <a href="#" data-options="align:left" data-dropdown="drop">Legislação</a><a href="#" class="flyout-toggle"></a>
              <ul id="drop" class="flyout"><!-- Flyout Menu -->
                <li class="has-flyout"><a href="#">Leis</a></li>
                <li class="has-flyout"><a href="#">Decretos</a></li>
                <li class="has-flyout"><a href="#">Resoluções e Portarias</a></li>
                <li class="has-flyout"><a href="#">Regulamentos</a></li>
              </ul> 
            </li><!-- END Flyout Menu -->
            <li class=""><a href="faq">FAQ</a></li>        
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
    %   varDesgn = ddcv['desgn']
    %   varFinanc = ddcv['financ']
    %   varDataInicio = ddcv['data_inicio']
    %   varDataEnteDoc = ddcv['data_ente_doc'] 
    %   varDataPublic = ddcv['data_public'] 
    %   varTipoContt = ddcv['tipo_contt'] 
    %   varTipoConcurso = ddcv['tipo_c'] 
    %   varDescricao = ddcv['descricao'] 
    %   varDocContrat = ddcv['doc_contrat'] 
    %   varDocPrograConc = ddcv['doc_progra_conc'] 
    %   varDocCaderEncargo = ddcv['doc_cader_encargo'] 
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
                <h6>{{varDesgn}}</h6>                               
              </div>
              <div class="panel">
                <h6>Financiado por:</h6> 
                <h7 class="subheader">{{varFinanc}}</h7>               
              </div>
              
              <div class="row">
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Identificação:</h6> 
                    <h7 class="subheader">{{varNumero}}</h7>                   
                  </div>
                </div>
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Tipo Contratos:</h6>
                    <h7 class="subheader">{{varTipoContt}}</h7>
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Tipo Concursos:</h6>  
                    <h7 class="subheader">{{varTipoConcurso}}</h7>                  
                  </div>
                </div>
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Data Abertura:</h6>
                    <h7 class="subheader">{{varDataInicio}}</h7>
                  </div>
                </div>
              </div>

              <div class="row">
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Entrega de Documento:</h6> 
                    <h7 class="subheader">{{varDataEnteDoc}}</h7>                   
                  </div>
                </div>
                <div class="large-6 small-6 columns">
                  <div class="panel">
                    <h6>Publicação de resultado:</h6>
                    <h7 class="subheader">{{varDataPublic}}</h7>
                  </div>
                </div>
              </div>

            </div>
            <div class="large-6 columns">
              <h3 class="show-for-small">Descricao<hr/></h3>
              <div class="panel">
                <h4 class="hide-for-small">Descricao<hr/></h4>
                <h5 class="subheader">{{varDescricao}}</h5>
              </div>
              <div class="row">
                <div class="large-4 small-4 columns">
                  <div class="panel">
                    <h7>Contrato</h7>
                    <img src='/static/images/PdfLogo.jpg'>
                    <a href="{{varDocContrat}}" onclick="openPdf(event, '{{varDocContrat}}', 'newpage.html');" class="small button">Ver</a>
                  </div>
                </div>
                <div class="large-4 small-4 columns">
                  <div class="panel">
                    <h7>Programa de Concurso</h7>
                    <img src='/static/images/PdfLogo.jpg'>
                    <a href="{{varDocPrograConc}}" onclick="openPdf(event, '{{varDocPrograConc}}', 'newpage.html');" class="small button">Ver</a>
                  </div>
                </div>
                <div class="large-4 small-4 columns">
                  <div class="panel">
                    <h7>Caderno de Encargos</h7>
                    <img src='/static/images/PdfLogo.jpg'>
                    <a href="{{varDocCaderEncargo}}" onclick="openPdf(event, '{{varDocCaderEncargo}}', 'newpage.html');" class="small button">Ver</a>
                  </div>
                </div>
              </div>
            </div>
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
                      <a href="#" class="postfix button expand">Search</a>
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
                  
                    <button type="submit" class="radius button" onClick="regist_esclareciment();">Enviar</button>
                  </form>
                </div>
              </section>
              
            </div>
             
            <div class="row">
                   
              <div class="large-3 columns ">
                <div class="panel">            
                  <h5><a href="#">Your Name</a></h5>
                  <div class="section-container vertical-nav" data-section data-options="deep_linking: false; one_up: true">
                    <section class="section">
                      <h5 class="title"><a href="#">Section 1</a></h5>
                    </section>
                    <section class="section">
                      <h5 class="title"><a href="#">Section 2</a></h5>
                    </section>
                    <section class="section">
                      <h5 class="title"><a href="#">Section 3</a></h5>
                    </section>
                    <section class="section">
                      <h5 class="title"><a href="#">Section 4</a></h5>
                    </section>
                    <section class="section">
                      <h5 class="title"><a href="#">Section 5</a></h5>
                    </section>
                    <section class="section">
                      <h5 class="title"><a href="#">Section 6</a></h5>
                    </section>
                  </div>
                </div>
              </div>
             
             
              <div class="large-9 columns">
               
                %   for ddesc in dadosrespEsclare:
                <div class="row">
                  <!--<div class="large-2 columns small-3"><img src="http://placehold.it/80x80&text=[img]"/></div>-->
                  <div class="large-12 columns">
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
                <div class="large-4 columns">
                    <div class="widget">
                        <h3>Compras Públicas</h3>
                        <ul>
                            <li><a href="#">Início</a></li>
                            <li><a href="#">Fornecedores</a></li>
                            <li><a href="#">Entidade pública</a></li>
                            <li><a href="#">Contratos</a></li>
                            <li><a href="#">Legislação</a></li>
                            <li><a href="#">Links</a></li>
                            <li><a href="#">FAQ</a></li>
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

                <div class="large-4 columns">
                    <div class="widget">
                        <h3>Contactos</h3>
                        <ul>
                            <li><a href="#"><i class="fi-telephone"></i> - Telefone +238 265 80 65</a></li>
                            <li><a href="#"><i class="fi-telephone"></i> - Telefone +238 265 80 65</a></li>
                            <li><a href="#"><i class="fi-marker"></i> - Localização</a></li>
                        </ul>
                    </div>
                </div><!--/.col-md-3-->
            </div>
       </section><!--/#bottom-->
         
    <footer style="background: #0784a9; margin: 0;">
      
        
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
      
      var strURL = '/registEsclareciment';

      $.ajax({type: 'POST', url: strURL, data: $('#form_registesclarecimt').serialize()
          }).done(function(r) {
              alert(r);
          }).fail(function(r) {
              alert('False');
          });
      
  }
  </script>    

  </body>
</html>
