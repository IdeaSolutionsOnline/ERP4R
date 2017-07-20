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
            <li class=""><a href="/cms">Início</a></li>
            <li class=""><a href="/Fornecedores">Fornecedores</a></li>
            <li class=""><a href="/Entidade_publica">Entidade pública</a></li>
            <li class=""><a href="/Contratos">Contratos</a></li>
            <li class="has-flyout">
             <a href="#" data-options="align:left" data-dropdown="drop">Documentos de Apoio</a><a href="#" class="flyout-toggle"></a>
              <ul id="drop" class="flyout"><!-- Flyout Menu -->
                <li class="has-flyout"><a href="/Legislacao">Legislação</a></li>
                <li class="has-flyout"><a href="/Directiva">Directiva</a></li>
                <li class="has-flyout"><a href="/Mapa_do_site">Mapa do site</a></li>
                <li class="has-flyout"><a href="/Manual">Manual</a></li>
                <li class="has-flyout"><a href="/Faq">FAQ</a></li>
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

    <div class="row">
      <div class="large-12 columns">
        <div class="row">
          <ul class="breadcrumbs">
            <li><a href="#">Início</a></li>
            <li class="unavailable"><a href="#">FAQ</a></li>
          </ul>
        </div>
      </div>
    </div>


    <div class="row">
      <div class="large-12 columns">
        <div class="row">
          <div class="row">
            <div class="large-12 columns">
              <div class="radius panel">
                <form class="search">
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
          <dl class="accordion" data-accordion>
            % numeroPergunt = 0
            % for df in dadosRespFaqs:
            %   numeroPergunt += 1
            %   state = ""
            %   if(numeroPergunt == 1):
            %     state = "active"
            %   end
            <dd class="accordion-navigation">
              <a href="#panel{{numeroPergunt}}a">{{numeroPergunt}} - {{df['pergunta']}}?</a>
              <div id="panel{{numeroPergunt}}a" class="content {{state}}">
               Resposta: {{df['resposta']}}
              </div>
            </dd>
            % end
            <!--
            <dd class="accordion-navigation">
              <a href="#panel2a">2 - Pergunta?</a>
              <div id="panel2a" class="content">
                Panel 2. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel3a">3 - Pergunta?</a>
              <div id="panel3a" class="content">
                Panel 3. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel4a">4 - Pergunta?</a>
              <div id="panel4a" class="content">
                Panel 4. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel5a">5 - Pergunta?</a>
              <div id="panel5a" class="content">
                Panel 5. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel6a">6 - Pergunta?</a>
              <div id="panel6a" class="content">
                Panel 6. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel7a">7 - Pergunta?</a>
              <div id="panel7a" class="content">
                Panel 7. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel8a">8 - Pergunta?</a>
              <div id="panel8a" class="content">
                Panel 8. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel9a">9 - Pergunta?</a>
              <div id="panel9a" class="content">
                Panel 9. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel10a">10 - Pergunta?</a>
              <div id="panel10a" class="content">
                Panel 10. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel11a">11 - Pergunta?</a>
              <div id="panel11a" class="content">
                Panel 11. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel12a">12 - Pergunta?</a>
              <div id="panel12a" class="content">
                Panel 12. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel13a">13 - Pergunta?</a>
              <div id="panel13a" class="content">
                Panel 13. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel14a">14 - Pergunta?</a>
              <div id="panel14a" class="content">
                Panel 14. Resposta.
              </div>
            </dd>
            <dd class="accordion-navigation">
              <a href="#panel15a">15 - Pergunta?</a>
              <div id="panel15a" class="content">
                Panel 15. Resposta.
              </div>
            </dd>
            -->
          </dl>
          <br>
          <hr/>

          <ul class="pagination">
            <li class="arrow unavailable"><a href="">&laquo;</a></li>
            <li class="current"><a href="">1</a></li>
            <li><a href="">2</a></li>
            <li><a href="">3</a></li>
            <li><a href="">4</a></li>
            <li class="unavailable"><a href="">&hellip;</a></li>
            <li><a href="">12</a></li>
            <li><a href="">13</a></li>
            <li class="arrow"><a href="">&raquo;</a></li>
          </ul>

        </div>
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
              <li><a href="#"><i class="fi-telephone"></i> - Telefone (+238) 260 75 07</a></li>
                            <li><a href="#"><i class="fi-telephone"></i> - Telefone (+238) 260 75 07</a></li>
                            <li><a href="#"><i class="fi-telephone"></i> - Fax (+238) 260 75 07</a></li>
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
