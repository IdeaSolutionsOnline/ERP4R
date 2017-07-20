% setdefault('menu2', '')
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
      <div class="twelve columns header_nav cms">
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
    
    <ul class="example-orbit" data-orbit>
      % for dIBn in dadosImgBanner:
      <li>
        <img src="{{dIBn['imagem']}}" alt="slide 1" />
        <div class="orbit-caption">
          Caption One.
        </div>
      </li>
      % end
    </ul>
   
    <div class="row">
              
      <div class="large-12 columns">
        <div class="row">
          <div class="title">
            <span class="content-title">Anúncios e Concursos</span>
          <hr />
          </div>
            
          <div class="large-12 columns">
           <ul class="tabs" data-tab>
                  <li class="tab1 tab-title active"><a href="#panel1">Abertos</a></li>
                  <li class="tab2 tab-title"><a href="#panel2">Em andamento</a></li>
                  <li class="tab3 tab-title"><a href="#panel3">Concluídos</a></li>
                </ul>
                <div class="tabs-content">
                  <div class="content active" id="panel1">
                  % if(dadosconcursAbert == []):

                  <div data-alert class="alert-box secondary">
                    Neste momento não se encontra concursos abertos!
                    <a href="#" class="close">&times;</a>
                  </div>

                  % else:
                    <table class="responsive">
                      <thead>
                        <tr>
                          <th>Código de procedimento</th>
                          <th>Objeto do contrato</th>
                          <th>Entidade Adjudicante</th>
                          <th>Data de publicação</th>
                          <th>Data de entrega das propostas</th>
                          <th></th>
                        </tr>
                      </thead>
                      <tbody id="pagup">
                        % i = 0
                        % for ddc in dadosconcursAbert:
                        %   alterBackg = ''
                        %   i +=1
                        %   resto = i % 2
                        %   if(resto == 0):
                        %     alterBackg = 'background-color: #E6FFE6'
                        %   end
                        <tr style="{{alterBackg}}">
                          <td class="linkConcurso">
                            <a href="View_concursos/{{ddc['id']}}">
                              {{ddc['codigoprocediment']}}
                            </a>
                          </td>
                          <td>{{ddc['desgn']}}</td>
                          <td>{{ddc['adjudicantenome']}}</td>
                          <td>{{ddc['data_inicio']}}</td>
                          <td>{{ddc['data_ente_doc']}}</td>                          
                          
                          <td>
                            <a href="View_concursos/{{ddc['id']}}" style="color: #f0c181 !important; background: none !important;">
                              <i class="fi-eye" style="font-size: 22px;" width="24" height="24"></i> Ver
                            </a>
                          </td>
                        </tr>
                        % end
                      </tbody>
                    </table>
                    % end
                    % restPagCount = 0
                    % for val in pagecountAberto:
                    %   restPagCount = val['vlacount']
                    % end
                    % if(restPagCount > 6):  
                    <ul class="pagination">
                      <li class="arrow unavailable"><a href="">&laquo;</a></li>
                      % tam = restPagCount    
                      % tampg = tam / 6             
                      %  if((tampg).is_integer() == True):
                      %    limt = int(tampg)
                      %  end
                      %  if((tampg).is_integer() == False):
                      %   limt = int(tampg) + 1
                      %  end
                      
                      % for i in range(0, limt):                
                      %   i_temp = i + 1
                      %   if(i_temp == 1):
                      %     ativo = 'current'
                      %   else:
                      %     ativo = ''
                      %   end
                        <li id="ativo{{i_temp}}" class="{{ativo}}">
                          <a onClick="callPageAberto({{i_temp}}, {{restPagCount}});">
                          {{i_temp}}
                          </a>
                        </li>
                      % end
                     
                      <li class="arrow"><a href="">&raquo;</a></li>
                    </ul>
                    % end
                  </div>
                  <div class="content" id="panel2">          

                    % if(dadosconcursEmAndament == []):

                    <div data-alert class="alert-box secondary">
                      Neste momento não se encontra concursos em andamento!
                      <a href="#" class="close">&times;</a>
                    </div>

                    % else:

                    <table>
                      <thead>
                        <tr>
                          <th>Código de procedimento</th>
                          <th>Objeto do contrato</th>
                          <th>Entidade Adjudicante</th>
                          <th>Data de publicação</th>
                          <th>Data de entrega das propostas</th>
                          <!--<th>Observação</th>-->
                          <th></th>
                        </tr>
                      </thead>
                      <tbody id="pagupEA">    
                          % i = 0                  
                          % for ddc2 in dadosconcursEmAndament:      
                          %   alterBackg = ''
                          %   i +=1
                          %   resto = i % 2
                          %   if(resto == 0):
                          %     alterBackg = 'background-color: #FFFFE6'
                          %   end
                          <tr style="{{alterBackg}}">
                            <td class="linkConcurso">
                              <a href="View_concursos/{{ddc2['id']}}">
                                {{ddc2['codigoprocediment']}}
                              </a>
                            </td>
                            <td>{{ddc2['desgn']}}</td>
                            <td>{{ddc2['adjudicantenome']}}</td>
                            <td>{{ddc2['data_inicio']}}</td>
                            <td>{{ddc2['data_ente_doc']}}</td>                            
                            <!--  <td>ddc2['descricao']</td> -->
                            <td>
                              <a href="View_concursos/{{ddc2['id']}}" style="color: #f0c181 !important; background: none !important;">
                                <i class="fi-eye" style="font-size: 22px;" width="24" height="24"></i>Ver
                              </a>
                            </td>
                          </tr>
                          % end 
                          <!--
                          <tr>
                            <td>Content Goes Here</td>
                            <td>This is longer Content Goes Here Donec id elit non mi porta gravida at eget metus.</td>
                            <td>Content Goes Here</td>
                            <td>Content Goes Here</td>
                          </tr>   
                          -->                
                      </tbody>
                    </table>    
                    % end   
                    % restPagCountEA = 0
                    % for val in pagecountEmAndament:
                    %   restPagCountEA = val['vlacount']
                    % end
                    % if(restPagCountEA > 6):
                    <ul class="pagination">
                      <li class="arrow unavailable"><a href=""> &laquo;</a></li>                      
                      % #tam = restPagCountEA    
                      % tampgea = restPagCountEA / 6             
                      %  if((tampgea).is_integer() == True):
                      %    limtea = int(tampgea)
                      %  end
                      %  if((tampgea).is_integer() == False):
                      %   limtea = int(tampgea) + 1
                      %  end
                      
                      % for i in range(0, limtea):                
                      %   i_tempea = i + 1
                      %   if(i_tempea == 1):
                      %     ativoea = 'current'
                      %   else:
                      %     ativoea = ''
                      %   end
                        <li id="ativoea{{i_tempea}}" class="{{ativoea}}">
                          <a onClick="callPageEmAndament({{i_tempea}}, {{restPagCountEA}});">
                          {{i_tempea}}
                          </a>
                        </li>
                      % end
                     
                      <li class="arrow"><a href="">&raquo;</a></li>
                    </ul>
                    % end
                  </div>
                  <div class="content" id="panel3">
                  
                    % if(dadosconcursConcluid == []):

                    <div data-alert class="alert-box secondary">
                      Neste momento não se encontra concursos Concluídos!
                      <a href="#" class="close">&times;</a>
                    </div>

                    % else:

                    <table>
                      <thead>
                        <tr>
                          <th>Código de procedimento</th>
                          <th>Objeto do contrato</th>
                          <th>Entidade Adjudicante</th>
                          <th>Data de publicação</th>
                          <th>Data de entrega das propostas</th>
                          <!--<th>Observação</th>-->
                          <th></th>
                        </tr>
                      </thead>
                      <tbody id="pagupC">      
                          % i = 0                      
                          % for ddc3 in dadosconcursConcluid:
                          %   alterBackg = ''
                          %   i +=1
                          %   resto = i % 2
                          %   if(resto == 0):
                          %     alterBackg = 'background-color: #FFE6E6'
                          %   end
                          <tr style="{{alterBackg}}">                          
                            <td class="linkConcurso">
                              <a href="View_concursos/{{ddc3['id']}}">
                                {{ddc3['codigoprocediment']}}
                              </a>
                            </td>
                            <td>{{ddc3['desgn']}}</td>
                            <td>{{ddc3['adjudicantenome']}}</td>
                            <td>{{ddc3['data_inicio']}}</td>
                            <td>{{ddc3['data_ente_doc']}}</td>   
                            <td>
                              <a href="View_concursos/{{ddc3['id']}}" style="color: #f0c181 !important; background: none !important;">
                                <i class="fi-eye" style="font-size: 22px;" width="24" height="24"></i>Ver
                              </a>
                            </td>
                            </tr>
                          % end              
                      </tbody>
                    </table>
                    % end
                    % restPagCountC = 0
                    % for valc in pagecountConcluido:
                    %   restPagCountC = valc['vlacount']
                    % end   
                    % if(restPagCountC > 6):  
                    <ul class="pagination">
                      <li class="arrow unavailable"><a href="">&laquo;</a></li>
                      % tampgc = restPagCountC / 6             
                      %  if((tampgc).is_integer() == True):
                      %    limtc = int(tampgc)
                      %  end
                      %  if((tampgc).is_integer() == False):
                      %   limtc = int(tampgc) + 1
                      %  end
                      
                      % for i in range(0, limtc):                
                      %   i_tempc = i + 1
                      %   if(i_tempc == 1):
                      %     ativoc = 'current'
                      %   else:
                      %     ativoc = ''
                      %   end
                        <li id="ativoc{{i_tempc}}" class="{{ativoc}}">
                          <a onClick="callPageConcluido({{i_tempc}}, {{restPagCountC}});">
                          {{i_tempc}}
                          </a>
                        </li>
                      % end
                     
                      <li class="arrow"><a href="">&raquo;</a></li>
                    </ul>
                    % end
                  </div>
                </div>

          </div>
                    
        </div>

        
      </div>

      <div class="large-10 columns">
        <div class="row">
          <div class="title">
                <span class="content-title">Plano Anual de Aquisição</span>
              <hr />
              </div>

              <div class="large-12 columns">                
                <p><b>PAA</b> – Plano Anual de Aquisição<br />
                O planeamento anual das aquisições públicas visa a elaboração de um plano onde se reúnem todos os itens
que se pretendem adquirir ao longo do ano económico seguinte, quer sejam agrupáveis ou não.</p>
                    
                    % if(dadosPlanoAA == []):

                    <div data-alert class="alert-box secondary">
                      Neste momento não se encontra Plano publicado!
                      <a href="#" class="close">&times;</a>
                    </div>

                    % else:

                    <ul class="tabs" data-tab>
                      <li class="tab4 tab-title active"><a href="#panel4">Plano Anual de Aquisição</a></li>
                      <li class="tab5 tab-title"><a href="#panel5">Plano Anual de Aquisição Agrupada</a></li>
                    </ul>
                    <div class="tabs-content">
                      <div class="content active" id="panel4"> 
                        <table class="large-12 columns">
                          <thead>
                            <tr>
                              <th>Ano</th>
                              <th>Entidade</th>
                              <th>Documento</th>                       
                            </tr>
                          </thead>
                          <tbody>

                            % i = 0
                            % for d in dadosPlanoAA:
                            %   alterBackg = ''
                            %   i +=1
                            %   resto = i % 2
                            %   if(resto == 0):
                            %     alterBackg = 'background-color: #fcf2e5'
                            %   end
                            <tr style="{{alterBackg}}">
                              <a href="{{d['paa_doc']}}" onclick="openPdf(event, '{{d['paa_doc']}}', 'newpage.html');" style="background: none !important;">
                                <td>{{d['paa_ano']}}</td>
                                <td>{{d['entidade']}}</td>
                                <td class="linkConcurso"> 
                                  <a href="{{d['paa_doc']}}" onclick="openPdf(event, '{{d['paa_doc']}}', 'newpage.html');" style="background: none !important;">
                                    <img src="/static/images/PdfLogo.jpg" width="24" height="24"> 
                                    Plano Anual de Aquisição
                                  </a>
                                </td> 
                              </a>                    
                            </tr>
                            % end                                              
                          </tbody>
                        </table>
                      </div>
                      <div class="content" id="panel5">  
                        <table class="large-12 columns">
                          <thead>
                            <tr>
                              <th>Ano</th>
                              <th>Entidade</th>
                              <th>Documento</th>                       
                            </tr>
                          </thead>
                          <tbody>

                            % i = 0
                            % for da in dadosPlanoAAAgru:
                            %   alterBackg = ''
                            %   i +=1
                            %   resto = i % 2
                            %   if(resto == 0):
                            %     alterBackg = 'background-color: #fcf2e5'
                            %   end
                            <tr style="{{alterBackg}}">
                              <a href="{{da['docpaa']}}" onclick="openPdf(event, '{{da['docpaa']}}', 'newpage.html');" style="background: none !important;">
                                <td>{{da['anopaa']}}</td>
                                <td>{{da['entidade']}}</td>
                                <td class="linkConcurso"> 
                                  <a href="{{da['docpaa']}}" onclick="openPdf(event, '{{da['docpaa']}}', 'newpage.html');" style="background: none !important;">
                                    <img src="/static/images/PdfLogo.jpg" width="24" height="24"> 
                                    Plano Anual de Aquisição Agrupada
                                  </a>
                                </td> 
                              </a>                    
                            </tr>
                            % end                                              
                          </tbody>
                        </table>
                      </div>
                    </div>
                    % end               
              </div>
              
            </div>
          </div>

        <div class="large-2 columns">
          <div class="row">
            <div class="title">
              <span class="content-title">Link útil</span>
              <hr />
            </div>
              <div class="large-12 columns hide-for-small">                
                <aside class="large-12 columns hide-for-small">
                  <p><a href="http://www.minfin.gov.cv/"><img src="static/images/link/Logo_MFP.png"/></a></p>
                  <p><a href="http://www.arap.cv/"><img src="static/images/link/link_arap.png"/></a></p>
                  <p><a href="http://www.governo.cv/"><img src="static/images/link/link_govcv.png"/></a></p>
                  <p><a href="http://www.tribunalcontas.cv/"><img src="static/images/link/link_TC.png"/></a></p>
                  <p><a href="https://www.portondinosilhas.gov.cv/"><img src="static/images/link/link_casacdd.png"/></a></p>
                </aside>
              </div>
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
                        <p style="color: white;">Regista-se na nossa newsletter e receba anúncios das compras e contratação publicas</p>
                        <form id="form_newsletter">
                            <div class="form-group">
                                <input type="text" class="form-control" id="emaiNewsl" name="emaiNewsl" placeholder="Seu email...">
                            </div>
                            <input type="hidden" id="estadoNewsl" name="estadoNewsl" VALUE="activo" />
                            <button type="submit" class="btn btn-primary"  onClick="regist_newsletter();">Registar</button>
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
                <div id="mnsconfr"></div>
                <div id="alert" data-alert class="alert-box info radius">
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
                        <option value="Negocio">Negocio</option>
                        <option value="Informatico">Informático</option>
                        <option value="Funcionalidades">Funcionalidades</option>
                        <option value="Usabilidade">Usabilidade</option>
                      </select>
                      </div>
                    </div>
                    
                    <div class="row collapse">                    
                      <label>Pedido de esclarecimento:</label>
                      <textarea rows="6" id="textHelp" name="textHelp" style="height: 120px !important;"></textarea>
                    </div>
                    
                    <input type="hidden" id="estadoHelp" name="estadoHelp" VALUE="pendente" />
                  
                    <button type="submit" class="radius button" onClick="regist_help();">Enviar</button>
                  </form>
                </div>
              </section>
        <a class="close-reveal-modal" aria-label="Close">&#215;</a>
      </div>
        
    <footer class="footer">
      
        <br>
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

  function callPageAberto(page,pagelimit){     
      
      var maxnumpage = parseInt(pagelimit / 6) + 1;
                  
      var strURL = '/get_pageProcedAbert/'+page+'/'+pagelimit ;
      $.ajax({type: 'GET', url: strURL
          }).done(function(r) {
              $('#pagup').html(r);
          }).fail(function(r) {
              $('#pagup').html('Erro');
          });
      $('#message').html('');

      for(i=1;i<=maxnumpage;i++){
        if(i==page){
          document.getElementById('ativo'+page).className = 'current';
        }else{
          document.getElementById('ativo'+i).className = '';
        }       
      }  
      
   }

   function callPageEmAndament(page,pagelimit){     
      
      var maxnumpage = parseInt(pagelimit / 6) + 1;
                  
      var strURL = '/get_pageProcedEmAndament/'+page+'/'+pagelimit ;
      $.ajax({type: 'GET', url: strURL
          }).done(function(r) {              
              $('#pagupEA').html(r);
          }).fail(function(r) {
              $('#pagupEA').html('Erro');
          });
      $('#message').html('');
      
      for(y=1;y<=maxnumpage;y++){
        if(y==page){
          document.getElementById('ativoea'+page).className = 'current';
        }else{
          document.getElementById('ativoea'+y).className = '';
        }       
      }  
      
   }

   function callPageConcluido(page,pagelimit){     
      
      var maxnumpage = parseInt(pagelimit / 6) + 1;
                
      var strURL = '/get_pageProcedConcluido/'+page+'/'+pagelimit ;
      $.ajax({type: 'GET', url: strURL
          }).done(function(r) {              
              $('#pagupC').html(r);
          }).fail(function(r) {
              $('#pagupC').html('Erro');
          });
      $('#message').html('');
      /*  */
      for(z=1;z<=maxnumpage;z++){
        if(z==page){
          document.getElementById('ativoc'+page).className = 'current';
        }else{
          document.getElementById('ativoc'+z).className = '';
        }       
      }  
      
   }

   </script>

   <script type="text/javascript">

    function regist_help() {
     
      var strURL = '/registoHelp';

      $.ajax({type: 'POST', url: strURL, data: $('#form_registhelp').serialize()
          }).done(function(r) {
              document.getElementById(alert).style.display = 'none';              
              $('#mnsconfr').html('<div data-alert class="alert-box success radius">Gravado com sucesso!<a href="#" class="close">&times;</a></div>');
               alert(r);
          }).fail(function(r) {
              alert('False');
          });
      /**/
    }

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
