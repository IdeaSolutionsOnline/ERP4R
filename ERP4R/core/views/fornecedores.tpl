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
    <link href="/static/slick/slick/slick.css"  rel="stylesheet" type="text/css"/>
    <link href="/static/slick/slick/slick-theme.css" rel="stylesheet" type="text/css"/>

  </head>
  <body>         
    <nav class="top-bar" data-topbar role="navigation">
      <ul class="title-area">
        <li class="name">
          <a href="#"><img src="/static/images/LogoMFP.png" alt="Loga" /></a>
        </li>
        <li class="toggle-topbar menu-icon"><a href="#"><span>Menu</span></a></li>
      </ul>
      
      <div class="middle tab-bar-section"> 
        <h1 class="titulo">Compras Públicas</h1>
      </div>
      
      <section class="top-bar-section">
        <ul class="right" style="margin-right:50px;">
          <li><a href="#">Contatos</a></li> <li class="divider"></li>
          <li><a href="/login" target="_blank" >Entrar</a></li>          
        </ul>
      </section>
    </nav>

    <nav>
      <div class="twelve columns header_nav">
        <div class="row">      
          <ul id="menu-header" class="nav-bar horizontal">             
            <li class=""><a href="/cms">Início</a></li>
            <li class="active"><a href="/Fornecedores">Fornecedores</a></li>
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
            <li class="current"><a href="#">Fornecedor </a></li>
          </ul>
        </div>
      </div>
    </div>


    <div class="row">
      <div class="large-12 columns">
        <div class="row">     
          <div class="row">
            <div class="large-12 columns">
              <h2>Fornecedores </h2>              
            </div>
          </div>
          <div class="row">            
            <div class="medium-7 large-7 columns">
              <p style="text-align: justify;" >Prezados fornecedores o Portal de Contratação Pública surge como importante instrumento de governação eletrónica que visa não só o cumprimento das regras de Contratação Pública fundamentadas nos princípios do interesse público, da transparência e publicidade, mas também, garantir maior agilidade e facilidade na tramitação dos procedimentos.</p>
              <p style="text-align: justify;">Neste contexto, o Portal de Contratação Pública – <a href="/">www.compraspúblicas.cv</a>, assegura a publicitação dos planos anuais de aquisições, de todos os concursos públicos, do registo de todos os contratos celebrados pelo Estado ao abrigo do Código da Contratação Pública, o pedido e recebimento de esclarecimentos relativos aos concursos públicos, e ainda o cadastro de todos operadores económicos com interesse em fornecer a todas entidades adjudicantes previstas no artigo 5º do Código de Contratação Publica.</p>
           
              <h3>Cadastro de Fornecedores</h3>
              <p style="text-align: justify;">O Estado reconhece, entre outros, o papel da contratação pública na dinamização de mercado e desenvolvimento económico, social e ambiental do país, assim, com o cadastro pretende-se dar visibilidade e publicidade aos potenciais e efetivos fornecedores do Estado de Cabo Verde. Visibilidade essa que servirá especialmente às entidades adjudicantes, mas também, a todos os potenciais consumidores, nacionais e internacionais.</p>
              <p style="text-align: justify;">Assim, o cadastro é obrigatório, devendo ser feito pelo fornecedor ou pelas entidades responsáveis pela condução de procedimentos de contratação pública, quando o concorrente a um determinado procedimento não tiver ainda feito o cadastro da sua empresa.</p>
                                     
            </div>
           
            <div class="medium-5 large-5 columns text-center">
              <div id="mnsconfr">

              </div>
              <div class="panel">
                <form action="#" id="form_registForncd">
                  <div class="row collapse">
                    <div class="large-2 columns">
                      <label class="inline">NIF</label>
                    </div>                     
                    <div class="large-8 columns">
                      <input type="text" id="fornecNif" name="fornecNif" placeholder="nif"/>
                    </div>
                    <div class="large-2 small-3 columns">
                      <a class="postfix button expand" style="font-size:1.275rem !important" onClick="get_dados();">
                        <i class="fi-eye medium"></i>
                      </a>
                    </div>
                  </div>

                  <div class="row collapse">
                    <div class="large-2 columns">
                      <label class="inline">Nome</label>
                    </div><br>
                    <div class="large-10 columns">
                      <input type="text" id="fornecName" name="fornecName" placeholder="Nome empresa" disabled="disabled">
                    </div>
                  </div>
                  <div class="row collapse">
                    <div class="large-2 columns">
                      <label class="inline">Email</label>
                    </div><br>
                    <div class="large-10 columns">
                      <input type="email" id="fornecEmail" name="fornecEmail" placeholder="empresa@email.com" disabled="disabled">
                    </div>
                  </div>
                  <div class="row collapse">
                    <div class="large-4 columns">
                      <label class="inline">Tipo de Empresa</label>
                    </div><br>
                    <div class="large-8 columns">
                      <select id="tipo_empresa" name="tipo_empresa">
                        <option value="Microempresa">Microempresa</option>
                        <option value="Pequena Empresa">Pequena Empresa</option>
                        <option value="Media Empresa">Média Empresa</option>
                        <option value="Grande Empresa">Grande Empresa</option>
                      </select>
                    </div>
                  </div> 
                  <div class="row collapse">
                    <div class="large-4 columns">
                      <label class="inline">Actividade económica</label>
                    </div><br>
                    <div class="large-8 columns">
                      <input type="text" id="area_servico" name="area_servico" placeholder="Actividade económica" disabled="disabled">
                    </div>
                  </div>  
                    
                  <div class="row collapse">
                    <div class="large-4 columns">
                      <label class="inline">Localização</label>
                    </div><br>
                    <div class="large-8 columns">
                      <input type="text" id="fornecLocalizacao" name="fornecLocalizacao" placeholder="Localização da empresa"disabled="disabled">
                    </div>
                  </div>             
                  <div class="row collapse">
                    <div class="large-4 columns">
                      <label class="inline">Nacionalidade</label>
                    </div><br>
                    <div class="large-8 columns">
                      <input type="text" id="pais_empresa" name="pais_empresa" placeholder="Nacionalidade" disabled="disabled" >
                    </div>                    
                  </div> 
                  <!--
                  <input type="submit" value="Registar" class="radius button" style="margin-top:15px" onClick="regist_forneced();"/> <br />
                  -->
                  <span class="radius button" style="margin-top:15px" onClick="regist_forneced();">Registar</span>
                </form>
              </div>
            </div>
            
            <div class="medium-12 large-12 columns">
            
            <p style="text-align: justify;">Com a introdução do NIF um conjunto de informações são carregadas a partir da base de dados da Direção Nacional das Receitas do Estado e cabe ao fornecedor apenas a introdução do tipo de empresa e a atividade comercial. No caso de desatualização dos dados, o fornecedor deverá dirigir-se à entidade responsável pelo registo de contribuintes.</p>
              <p style="text-align: justify;">O fornecedor poderá enviar o logotipo da sua empresa para o email <span>ums-suporte@minfin.gov.cv</span> e o mesmo será introduzido e constará do espaço dedicado aos cadastrados do presente ecrã.</p>
              
              <h3>Esclarecimentos e Formação</h3>
              <p style="text-align: justify;">Os esclarecimentos necessários à boa compreensão de documentos de um determinado concurso público devem ser solicitados na área do site dedicada ao procedimento em causa.</p>
              <p style="text-align: justify;">Relativamente aos esclarecimentos dos documentos dos concursos públicos, os mesmos devem ser solicitados as respetivas entidades responsáveis pela condução dos procedimentos dentro do prazo estabelecido nos documentos do procedimento.</p>
              <p style="text-align: justify;">Para a devida utilização do site os fornecedores deverão solicitar esclarecimentos através dos contatos, telefónico e eletrónico, constantes do final dos ecrãs do presente site.</p>
              <p style="text-align: justify;">Os fornecedores interessados em receber formação no âmbito da contratação publica deverão manifestar o seu interesse através do email ums-suporte@minfin.gov.cv que a Direção Geral do Património e da Contratação Publica e os seus parceiros, mediante o registo do numero suficiente de interessados, diligenciarão a organização de sessões de formação.</p>
              <p></p>
              
              </div>
          </div>
          <br>

          <div class="row">
            <div class="large-12 columns">
              <div class="radius panel">
                <form class="search">
                  <div class="row collapse">
                    <div class="large-10 small-8 columns">
                      <input type="text" />
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

                    
          <!--/////////////////////////////////////////////////////////////////////////////////////////-->
            <script>

          +function(e,f,b,j,c,i,k){/*! Jssor */
          new(function(){});var d=e.$JssorEasing$={Jc:function(a){return-b.cos(a*b.PI)/2+.5},dd:function(a){return a},Jf:function(a){return a*a},jd:function(a){return-a*(a-2)},If:function(a){return(a*=2)<1?1/2*a*a:-1/2*(--a*(a-2)-1)},Hf:function(a){return a*a*a},Gf:function(a){return(a-=1)*a*a+1},Ff:function(a){return(a*=2)<1?1/2*a*a*a:1/2*((a-=2)*a*a+2)},Lf:function(a){return a*a*a*a},Ef:function(a){return-((a-=1)*a*a*a-1)},Cf:function(a){return(a*=2)<1?1/2*a*a*a*a:-1/2*((a-=2)*a*a*a-2)},Bf:function(a){return a*a*a*a*a},Af:function(a){return(a-=1)*a*a*a*a+1},zf:function(a){return(a*=2)<1?1/2*a*a*a*a*a:1/2*((a-=2)*a*a*a*a+2)},yf:function(a){return 1-b.cos(a*b.PI/2)},xf:function(a){return b.sin(a*b.PI/2)},Df:function(a){return-1/2*(b.cos(b.PI*a)-1)},Nf:function(a){return a==0?0:b.pow(2,10*(a-1))},Vf:function(a){return a==1?1:-b.pow(2,-10*a)+1},Of:function(a){return a==0||a==1?a:(a*=2)<1?1/2*b.pow(2,10*(a-1)):1/2*(-b.pow(2,-10*--a)+2)},cg:function(a){return-(b.sqrt(1-a*a)-1)},bg:function(a){return b.sqrt(1-(a-=1)*a)},ag:function(a){return(a*=2)<1?-1/2*(b.sqrt(1-a*a)-1):1/2*(b.sqrt(1-(a-=2)*a)+1)},Zf:function(a){if(!a||a==1)return a;var c=.3,d=.075;return-(b.pow(2,10*(a-=1))*b.sin((a-d)*2*b.PI/c))},Yf:function(a){if(!a||a==1)return a;var c=.3,d=.075;return b.pow(2,-10*a)*b.sin((a-d)*2*b.PI/c)+1},Xf:function(a){if(!a||a==1)return a;var c=.45,d=.1125;return(a*=2)<1?-.5*b.pow(2,10*(a-=1))*b.sin((a-d)*2*b.PI/c):b.pow(2,-10*(a-=1))*b.sin((a-d)*2*b.PI/c)*.5+1},dg:function(a){var b=1.70158;return a*a*((b+1)*a-b)},Wf:function(a){var b=1.70158;return(a-=1)*a*((b+1)*a+b)+1},Uf:function(a){var b=1.70158;return(a*=2)<1?1/2*a*a*(((b*=1.525)+1)*a-b):1/2*((a-=2)*a*(((b*=1.525)+1)*a+b)+2)},cd:function(a){return 1-d.vc(1-a)},vc:function(a){return a<1/2.75?7.5625*a*a:a<2/2.75?7.5625*(a-=1.5/2.75)*a+.75:a<2.5/2.75?7.5625*(a-=2.25/2.75)*a+.9375:7.5625*(a-=2.625/2.75)*a+.984375},Tf:function(a){return a<1/2?d.cd(a*2)*.5:d.vc(a*2-1)*.5+.5},Sf:function(){return 1-b.abs(1)},Rf:function(a){return 1-b.cos(a*b.PI*2)},Qf:function(a){return b.sin(a*b.PI*2)},Pf:function(a){return 1-((a*=2)<1?(a=1-a)*a*a:(a-=1)*a*a)},wf:function(a){return(a*=2)<1?a*a*a:(a=2-a)*a*a}},g=e.$Jease$={vf:d.Jc,uf:d.dd,lf:d.Jf,Ne:d.jd,Oe:d.If,Pe:d.Hf,Qe:d.Gf,Re:d.Ff,Se:d.Lf,Te:d.Ef,Ue:d.Cf,Ve:d.Bf,We:d.Af,Xe:d.zf,Ye:d.yf,Ze:d.xf,af:d.Df,bf:d.Nf,cf:d.Vf,df:d.Of,sf:d.cg,rf:d.bg,qf:d.ag,pf:d.Zf,of:d.Yf,nf:d.Xf,tf:d.dg,mf:d.Wf,kf:d.Uf,jf:d.cd,hf:d.vc,gf:d.Tf,fg:d.Sf,ef:d.Rf,Mf:d.Qf,eg:d.Pf,vg:d.wf};e.$JssorDirection$={};var a=e.$Jssor$=new function(){var g=this,Ab=/\S+/g,S=1,tb=2,Z=3,wb=4,db=5,I,s=0,l=0,q=0,J=0,C=0,B=navigator,ib=B.appName,n=B.userAgent;function Jb(){if(!I){I={Qg:"ontouchstart"in e||"createTouch"in f};var a;if(B.pointerEnabled||(a=B.msPointerEnabled))I.vd=a?"msTouchAction":"touchAction"}return I}function t(i){if(!s){s=-1;if(ib=="Microsoft Internet Explorer"&&!!e.attachEvent&&!!e.ActiveXObject){var g=n.indexOf("MSIE");s=S;q=o(n.substring(g+5,n.indexOf(";",g)));/*@cc_on J=@_jscript_version@*/;l=f.documentMode||q}else if(ib=="Netscape"&&!!e.addEventListener){var d=n.indexOf("Firefox"),b=n.indexOf("Safari"),h=n.indexOf("Chrome"),c=n.indexOf("AppleWebKit");if(d>=0){s=tb;l=o(n.substring(d+8))}else if(b>=0){var j=n.substring(0,b).lastIndexOf("/");s=h>=0?wb:Z;l=o(n.substring(j+1,b))}else{var a=/Trident\/.*rv:([0-9]{1,}[\.0-9]{0,})/i.exec(n);if(a){s=S;l=q=o(a[1])}}if(c>=0)C=o(n.substring(c+12))}else{var a=/(opera)(?:.*version|)[ \/]([\w.]+)/i.exec(n);if(a){s=db;l=o(a[2])}}}return i==s}function p(){return t(S)}function N(){return p()&&(l<6||f.compatMode=="BackCompat")}function vb(){return t(Z)}function cb(){return t(db)}function ob(){return vb()&&C>534&&C<535}function L(){return p()&&l<9}function qb(a){var b;return function(d){if(!b){b=a;var c=a.substr(0,1).toUpperCase()+a.substr(1);m([a].concat(["WebKit","ms","Moz","O","webkit"]),function(g,f){var e=a;if(f)e=g+c;if(d.style[e]!=k)return b=e})}return b}}var pb=qb("transform");function hb(a){return{}.toString.call(a)}var H;function Gb(){if(!H){H={};m(["Boolean","Number","String","Function","Array","Date","RegExp","Object"],function(a){H["[object "+a+"]"]=a.toLowerCase()})}return H}function m(a,d){if(hb(a)=="[object Array]"){for(var b=0;b<a.length;b++)if(d(a[b],b,a))return c}else for(var e in a)if(d(a[e],e,a))return c}function z(a){return a==j?String(a):Gb()[hb(a)]||"object"}function fb(a){for(var b in a)return c}function x(a){try{return z(a)=="object"&&!a.nodeType&&a!=a.window&&(!a.constructor||{}.hasOwnProperty.call(a.constructor.prototype,"isPrototypeOf"))}catch(b){}}function w(a,b){return{x:a,y:b}}function lb(b,a){setTimeout(b,a||0)}function F(b,d,c){var a=!b||b=="inherit"?"":b;m(d,function(c){var b=c.exec(a);if(b){var d=a.substr(0,b.index),e=a.substr(b.lastIndex+1,a.length-(b.lastIndex+1));a=d+e}});a=c+(a.indexOf(" ")!=0?" ":"")+a;return a}function sb(b,a){if(l<9)b.style.filter=a}function Cb(f,a,i){if(!J||J<9){var d=a.jb,e=a.kb,j=(a.r||0)%360,h="";if(j||d!=k||e!=k){if(d==k)d=1;if(e==k)e=1;var c=g.Rg(j/180*b.PI,d||1,e||1),i=g.Sg(c,a.Y,a.X);g.Bg(f,i.y);g.Jg(f,i.x);h="progid:DXImageTransform.Microsoft.Matrix(M11="+c[0][0]+", M12="+c[0][1]+", M21="+c[1][0]+", M22="+c[1][1]+", SizingMethod='auto expand')"}var m=f.style.filter,n=new RegExp(/[\s]*progid:DXImageTransform\.Microsoft\.Matrix\([^\)]*\)/g),l=F(m,[n],h);sb(f,l)}}g.Ag=Jb;g.Md=p;g.gg=vb;g.sc=cb;g.T=L;g.wd=function(){return l};g.kg=function(){t();return C};g.K=lb;function V(a){a.constructor===V.caller&&a.Bd&&a.Bd.apply(a,V.caller.arguments)}g.Bd=V;g.qb=function(a){if(g.Dd(a))a=f.getElementById(a);return a};function r(a){return a||e.event}g.Od=r;g.xc=function(a){a=r(a);return a.target||a.srcElement||f};g.Fd=function(a){a=r(a);return{x:a.pageX||a.clientX||0,y:a.pageY||a.clientY||0}};function A(c,d,a){if(a!==k)c.style[d]=a==k?"":a;else{var b=c.currentStyle||c.style;a=b[d];if(a==""&&e.getComputedStyle){b=c.ownerDocument.defaultView.getComputedStyle(c,j);b&&(a=b.getPropertyValue(d)||b[d])}return a}}function X(b,c,a,d){if(a!==k){if(a==j)a="";else d&&(a+="px");A(b,c,a)}else return o(A(b,c))}function h(c,a){var d=a?X:A,b;if(a&4)b=qb(c);return function(e,f){return d(e,b?b(e):c,f,a&2)}}function Db(b){if(p()&&q<9){var a=/opacity=([^)]*)/.exec(b.style.filter||"");return a?o(a[1])/100:1}else return o(b.style.opacity||"1")}function Fb(c,a,f){if(p()&&q<9){var h=c.style.filter||"",i=new RegExp(/[\s]*alpha\([^\)]*\)/g),e=b.round(100*a),d="";if(e<100||f)d="alpha(opacity="+e+") ";var g=F(h,[i],d);sb(c,g)}else c.style.opacity=a==1?"":b.round(a*100)/100}var yb={r:["rotate"],Hb:["rotateX"],Gb:["rotateY"],jb:["scaleX",2],kb:["scaleY",2],Nb:["translateX",1],Mb:["translateY",1],Lb:["translateZ",1],Jb:["skewX"],Zb:["skewY"]};function nb(e,c){if(p()&&l&&l<10){delete c.Hb;delete c.Gb}var d=pb(e);if(d){var b="";a.c(c,function(e,c){var a=yb[c];if(a){var d=a[1]||0;b+=(b?" ":"")+a[0]+"("+e+(["deg","px",""])[d]+")"}});e.style[d]=b}}g.qg=function(b,a){if(ob())lb(g.D(j,nb,b,a));else(L()?Cb:nb)(b,a)};g.nd=h("transformOrigin",4);g.rg=h("backfaceVisibility",4);g.sg=h("transformStyle",4);g.tg=h("perspective",6);g.ug=h("perspectiveOrigin",4);g.xg=function(a,c){if(p()&&q<9||q<10&&N())a.style.zoom=c==1?"":c;else{var b=pb(a);if(b){var f="scale("+c+")",e=a.style[b],g=new RegExp(/[\s]*scale\(.*?\)/g),d=F(e,[g],f);a.style[b]=d}}};var bb=0,ub=0;g.zg=function(b,a){return L()?function(){var g=c,d=N()?b.document.body:b.document.documentElement;if(d){var f=d.offsetWidth-bb,e=d.offsetHeight-ub;if(f||e){bb+=f;ub+=e}else g=i}g&&a()}:a};g.Ib=function(b,a){return function(c){c=r(c);var e=c.type,d=c.relatedTarget||(e=="mouseout"?c.toElement:c.fromElement);(!d||d!==a&&!g.Ug(a,d))&&b(c)}};g.e=function(a,d,b,c){a=g.qb(a);if(a.addEventListener){d=="mousewheel"&&a.addEventListener("DOMMouseScroll",b,c);a.addEventListener(d,b,c)}else if(a.attachEvent){a.attachEvent("on"+d,b);c&&a.setCapture&&a.setCapture()}};g.M=function(a,c,d,b){a=g.qb(a);if(a.removeEventListener){c=="mousewheel"&&a.removeEventListener("DOMMouseScroll",d,b);a.removeEventListener(c,d,b)}else if(a.detachEvent){a.detachEvent("on"+c,d);b&&a.releaseCapture&&a.releaseCapture()}};g.Rb=function(a){a=r(a);a.preventDefault&&a.preventDefault();a.cancel=c;a.returnValue=i};g.mg=function(a){a=r(a);a.stopPropagation&&a.stopPropagation();a.cancelBubble=c};g.D=function(d,c){var a=[].slice.call(arguments,2),b=function(){var b=a.concat([].slice.call(arguments,0));return c.apply(d,b)};return b};g.Kg=function(a,b){if(b==k)return a.textContent||a.innerText;var c=f.createTextNode(b);g.tc(a);a.appendChild(c)};g.N=function(d,c){for(var b=[],a=d.firstChild;a;a=a.nextSibling)(c||a.nodeType==1)&&b.push(a);return b};function gb(a,c,e,b){b=b||"u";for(a=a?a.firstChild:j;a;a=a.nextSibling)if(a.nodeType==1){if(R(a,b)==c)return a;if(!e){var d=gb(a,c,e,b);if(d)return d}}}g.C=gb;function P(a,d,f,b){b=b||"u";var c=[];for(a=a?a.firstChild:j;a;a=a.nextSibling)if(a.nodeType==1){R(a,b)==d&&c.push(a);if(!f){var e=P(a,d,f,b);if(e.length)c=c.concat(e)}}return c}function ab(a,c,d){for(a=a?a.firstChild:j;a;a=a.nextSibling)if(a.nodeType==1){if(a.tagName==c)return a;if(!d){var b=ab(a,c,d);if(b)return b}}}g.Dg=ab;function rb(a,c,e){var b=[];for(a=a?a.firstChild:j;a;a=a.nextSibling)if(a.nodeType==1){(!c||a.tagName==c)&&b.push(a);if(!e){var d=rb(a,c,e);if(d.length)b=b.concat(d)}}return b}g.Eg=rb;g.Gg=function(b,a){return b.getElementsByTagName(a)};function y(){var e=arguments,d,c,b,a,g=1&e[0],f=1+g;d=e[f-1]||{};for(;f<e.length;f++)if(c=e[f])for(b in c){a=c[b];if(a!==k){a=c[b];var h=d[b];d[b]=g&&(x(h)||x(a))?y(g,{},h,a):a}}return d}g.n=y;function W(f,g){var d={},c,a,b;for(c in f){a=f[c];b=g[c];if(a!==b){var e;if(x(a)&&x(b)){a=W(a,b);e=!fb(a)}!e&&(d[c]=a)}}return d}g.kd=function(a){return z(a)=="function"};g.rc=function(a){return z(a)=="array"};g.Dd=function(a){return z(a)=="string"};g.Xb=function(a){return!isNaN(o(a))&&isFinite(a)};g.c=m;g.wg=x;function O(a){return f.createElement(a)}g.sb=function(){return O("DIV")};g.ng=function(){return O("SPAN")};g.Xc=function(){};function T(b,c,a){if(a==k)return b.getAttribute(c);b.setAttribute(c,a)}function R(a,b){return T(a,b)||T(a,"data-"+b)}g.B=T;g.i=R;function u(b,a){if(a==k)return b.className;b.className=a}g.ed=u;function kb(b){var a={};m(b,function(b){a[b]=b});return a}function mb(b,a){return b.match(a||Ab)}function M(b,a){return kb(mb(b||"",a))}g.lg=mb;function Y(b,c){var a="";m(c,function(c){a&&(a+=b);a+=c});return a}function E(a,c,b){u(a,Y(" ",y(W(M(u(a)),M(c)),M(b))))}g.bd=function(a){return a.parentNode};g.Q=function(a){g.mb(a,"none")};g.z=function(a,b){g.mb(a,b?"none":"")};g.hg=function(b,a){b.removeAttribute(a)};g.Ng=function(){return p()&&l<10};g.Cg=function(d,c){if(c)d.style.clip="rect("+b.round(c.g)+"px "+b.round(c.o)+"px "+b.round(c.p)+"px "+b.round(c.f)+"px)";else{var g=d.style.cssText,f=[new RegExp(/[\s]*clip: rect\(.*?\)[;]?/i),new RegExp(/[\s]*cliptop: .*?[;]?/i),new RegExp(/[\s]*clipright: .*?[;]?/i),new RegExp(/[\s]*clipbottom: .*?[;]?/i),new RegExp(/[\s]*clipleft: .*?[;]?/i)],e=F(g,f,"");a.Ub(d,e)}};g.db=function(){return+new Date};g.J=function(b,a){b.appendChild(a)};g.Ob=function(b,a,c){(c||a.parentNode).insertBefore(b,a)};g.ub=function(a,b){(b||a.parentNode).removeChild(a)};g.ce=function(a,b){m(a,function(a){g.ub(a,b)})};g.tc=function(a){g.ce(g.N(a,c),a)};g.Wd=function(a,b){var c=g.bd(a);b&1&&g.I(a,(g.k(c)-g.k(a))/2);b&2&&g.G(a,(g.l(c)-g.l(a))/2)};g.Wb=function(b,a){return parseInt(b,a||10)};var o=parseFloat;g.mc=o;g.Ug=function(b,a){var c=f.body;while(a&&b!==a&&c!==a)try{a=a.parentNode}catch(d){return i}return b===a};function U(d,c,b){var a=d.cloneNode(!c);!b&&g.hg(a,"id");return a}g.hb=U;g.Fb=function(e,f){var a=new Image;function b(e,c){g.M(a,"load",b);g.M(a,"abort",d);g.M(a,"error",d);f&&f(a,c)}function d(a){b(a,c)}if(cb()&&l<11.6||!e)b(!e);else{g.e(a,"load",b);g.e(a,"abort",d);g.e(a,"error",d);a.src=e}};g.ge=function(d,a,e){var c=d.length+1;function b(b){c--;if(a&&b&&b.src==a.src)a=b;!c&&e&&e(a)}m(d,function(a){g.Fb(a.src,b)});b()};g.ld=function(b,g,i,h){if(h)b=U(b);var c=P(b,g);if(!c.length)c=a.Gg(b,g);for(var f=c.length-1;f>-1;f--){var d=c[f],e=U(i);u(e,u(d));a.Ub(e,d.style.cssText);a.Ob(e,d);a.ub(d)}return b};function Hb(b){var l=this,p="",r=["av","pv","ds","dn"],e=[],q,j=0,h=0,d=0;function i(){E(b,q,e[d||j||h&2||h]);a.fb(b,"pointer-events",d?"none":"")}function c(){j=0;i();g.M(f,"mouseup",c);g.M(f,"touchend",c);g.M(f,"touchcancel",c)}function o(a){if(d)g.Rb(a);else{j=4;i();g.e(f,"mouseup",c);g.e(f,"touchend",c);g.e(f,"touchcancel",c)}}l.hd=function(a){if(a===k)return h;h=a&2||a&1;i()};l.gd=function(a){if(a===k)return!d;d=a?0:3;i()};l.L=b=g.qb(b);var n=a.lg(u(b));if(n)p=n.shift();m(r,function(a){e.push(p+a)});q=Y(" ",e);e.unshift("");g.e(b,"mousedown",o);g.e(b,"touchstart",o)}g.Yb=function(a){return new Hb(a)};g.fb=A;g.tb=h("overflow");g.G=h("top",2);g.I=h("left",2);g.k=h("width",2);g.l=h("height",2);g.Jg=h("marginLeft",2);g.Bg=h("marginTop",2);g.A=h("position");g.mb=h("display");g.H=h("zIndex",1);g.vb=function(b,a,c){if(a!=k)Fb(b,a,c);else return Db(b)};g.Ub=function(a,b){if(b!=k)a.style.cssText=b;else return a.style.cssText};var Q={s:g.vb,g:g.G,f:g.I,P:g.k,O:g.l,Eb:g.A,S:g.H},K;function G(){if(!K)K=y({a:g.Cg,v:g.qg},Q);return K}function eb(){var a={};a.v=a.v;a.v=a.r;a.v=a.Hb;a.v=a.Gb;a.v=a.Jb;a.v=a.Zb;a.v=a.Nb;a.v=a.Mb;a.v=a.Lb;return G()}g.le=G;g.Tc=eb;g.ke=function(c,b){G();var a={};m(b,function(d,b){if(Q[b])a[b]=Q[b](c)});return a};g.ab=function(c,b){var a=G();m(b,function(d,b){a[b]&&a[b](c,d)})};g.oe=function(b,a){eb();g.ab(b,a)};var D=new function(){var a=this;function b(d,g){for(var j=d[0].length,i=d.length,h=g[0].length,f=[],c=0;c<i;c++)for(var k=f[c]=[],b=0;b<h;b++){for(var e=0,a=0;a<j;a++)e+=d[c][a]*g[a][b];k[b]=e}return f}a.jb=function(b,c){return a.Nd(b,c,0)};a.kb=function(b,c){return a.Nd(b,0,c)};a.Nd=function(a,c,d){return b(a,[[c,0],[0,d]])};a.Sb=function(d,c){var a=b(d,[[c.x],[c.y]]);return w(a[0][0],a[1][0])}};g.Rg=function(d,a,c){var e=b.cos(d),f=b.sin(d);return[[e*a,-f*c],[f*a,e*c]]};g.Sg=function(d,c,a){var e=D.Sb(d,w(-c/2,-a/2)),f=D.Sb(d,w(c/2,-a/2)),g=D.Sb(d,w(c/2,a/2)),h=D.Sb(d,w(-c/2,a/2));return w(b.min(e.x,f.x,g.x,h.x)+c/2,b.min(e.y,f.y,g.y,h.y)+a/2)};var zb={j:1,jb:1,kb:1,r:0,Hb:0,Gb:0,Nb:0,Mb:0,Lb:0,Jb:0,Zb:0};g.Bc=function(b){var c=b||{};if(b)if(a.kd(b))c={nb:c};else if(a.kd(b.a))c.a={nb:b.a};return c};function jb(c,a){var b={};m(c,function(c,d){var e=c;if(a[d]!=k)if(g.Xb(c))e=c+a[d];else e=jb(c,a[d]);b[d]=e});return b}g.He=jb;g.rd=function(h,i,w,n,y,z,o){var c=i;if(h){c={};for(var g in i){var A=z[g]||1,v=y[g]||[0,1],e=(w-v[0])/v[1];e=b.min(b.max(e,0),1);e=e*A;var u=b.floor(e);if(e!=u)e-=u;var l=n.nb||d.Jc,m,B=h[g],q=i[g];if(a.Xb(q)){l=n[g]||l;var x=l(e);m=B+q*x}else{m=a.n({Db:{}},h[g]);a.c(q.Db||q,function(d,a){if(n.a)l=n.a[a]||n.a.nb||l;var c=l(e),b=d*c;m.Db[a]=b;m[a]+=b})}c[g]=m}var t,f={Y:o.Y,X:o.X};a.c(zb,function(d,a){t=t||i[a];var b=c[a];if(b!=k){if(b!=d)f[a]=b;delete c[a]}else if(h[a]!=k&&h[a]!=d)f[a]=h[a]});if(i.j&&f.j){f.jb=f.j;f.kb=f.j}c.v=f}if(i.a&&o.V){var p=c.a.Db,s=(p.g||0)+(p.p||0),r=(p.f||0)+(p.o||0);c.f=(c.f||0)+r;c.g=(c.g||0)+s;c.a.f-=r;c.a.o-=r;c.a.g-=s;c.a.p-=s}if(c.a&&a.Ng()&&!c.a.g&&!c.a.f&&c.a.o==o.Y&&c.a.p==o.X)c.a=j;return c}};function m(){var b=this,d=[];function i(a,b){d.push({oc:a,pc:b})}function h(b,c){a.c(d,function(a,e){a.oc==b&&a.pc===c&&d.splice(e,1)})}b.yb=b.addEventListener=i;b.removeEventListener=h;b.m=function(b){var c=[].slice.call(arguments,1);a.c(d,function(a){a.oc==b&&a.pc.apply(e,c)})}}var l=e.$JssorAnimator$=function(y,C,k,O,L,K){y=y||0;var d=this,q,n,o,u,z=0,G,H,F,B,x=0,h=0,m=0,D,l,g,f,p,w=[],A;function N(a){g+=a;f+=a;l+=a;h+=a;m+=a;x+=a}function t(n){var e=n;if(p&&(e>=f||e<=g))e=((e-g)%p+p)%p+g;if(!D||u||h!=e){var i=b.min(e,f);i=b.max(i,g);if(!D||u||i!=m){if(K){var j=(i-l)/(C||1);if(k.Hc)j=1-j;var o=a.rd(L,K,j,G,F,H,k);a.c(o,function(b,a){A[a]&&A[a](O,b)})}d.Gc(m-l,i-l);m=i;a.c(w,function(b,c){var a=n<h?w[w.length-c-1]:b;a.u(m-x)});var r=h,q=m;h=e;D=c;d.Kb(r,q)}}}function E(a,c,d){c&&a.R(f);if(!d){g=b.min(g,a.Fc()+x);f=b.max(f,a.cb()+x)}w.push(a)}var r=e.requestAnimationFrame||e.webkitRequestAnimationFrame||e.mozRequestAnimationFrame||e.msRequestAnimationFrame;if(a.gg()&&a.wd()<7)r=j;r=r||function(b){a.K(b,k.Z)};function I(){if(q){var d=a.db(),e=b.min(d-z,k.Id),c=h+e*o;z=d;if(c*o>=n*o)c=n;t(c);if(!u&&c*o>=n*o)J(B);else r(I)}}function s(e,i,j){if(!q){q=c;u=j;B=i;e=b.max(e,g);e=b.min(e,f);n=e;o=n<h?-1:1;d.Jd();z=a.db();r(I)}}function J(a){if(q){u=q=B=i;d.zd();a&&a()}}d.ud=function(a,b,c){s(a?h+a:f,b,c)};d.td=s;d.lb=J;d.Rd=function(a){s(a)};d.W=function(){return h};d.Ad=function(){return n};d.Cb=function(){return m};d.u=t;d.V=function(a){t(h+a)};d.yd=function(){return q};d.Je=function(a){p=a};d.R=N;d.F=function(a,b){E(a,0,b)};d.zc=function(a){E(a,1)};d.ie=function(a){f+=a};d.Fc=function(){return g};d.cb=function(){return f};d.Kb=d.Jd=d.zd=d.Gc=a.Xc;d.qc=a.db();k=a.n({Z:16,Id:50},k);p=k.qd;A=a.n({},a.le(),k.Mc);g=l=y;f=y+C;H=k.cc||{};F=k.ec||{};G=a.Bc(k.E)};var o=e.$JssorSlideshowFormations$=new function(){var h=this;function g(b,a,c){c.push(a);b[a]=b[a]||[];b[a].push(c)}h.te=function(d){for(var e=[],a,c=0;c<d.U;c++)for(a=0;a<d.q;a++)g(e,b.ceil(1e5*b.random())%13,[c,a]);return e}};e.$JssorSlideshowRunner$=function(n,s,q,t,y){var f=this,u,g,e,x=0,w=t.eh,r,h=8;function k(g,f){var e={Z:f,gc:1,K:0,q:1,U:1,s:0,j:0,a:0,V:i,uc:i,Hc:i,Be:o.te,fd:{Ce:0,Ge:0},E:d.Jc,cc:{},jc:[],ec:{}};a.n(e,g);e.E=a.Bc(e.E);e.Ie=b.ceil(e.gc/e.Z);e.ue=function(b,a){b/=e.q;a/=e.U;var f=b+"x"+a;if(!e.jc[f]){e.jc[f]={P:b,O:a};for(var c=0;c<e.q;c++)for(var d=0;d<e.U;d++)e.jc[f][d+","+c]={g:d*a,o:c*b+b,p:d*a+a,f:c*b}}return e.jc[f]};if(e.nc){e.nc=k(e.nc,f);e.uc=c}return e}function p(A,h,d,v,n,l){var y=this,t,u={},j={},m=[],f,e,r,p=d.fd.Ce||0,q=d.fd.Ge||0,g=d.ue(n,l),o=B(d),C=o.length-1,s=d.gc+d.K*C,w=v+s,k=d.uc,x;w+=50;function B(a){var b=a.Be(a);return a.Hc?b.reverse():b}y.Rc=w;y.ic=function(c){c-=v;var e=c<s;if(e||x){x=e;if(!k)c=s-c;var f=b.ceil(c/d.Z);a.c(j,function(c,e){var d=b.max(f,c.Xd);d=b.min(d,c.length-1);if(c.Vc!=d){if(!c.Vc&&!k)a.z(m[e]);else d==c.Zd&&k&&a.Q(m[e]);c.Vc=d;a.oe(m[e],c[d])}})}};h=a.hb(h);if(a.T()){var D=!h["no-image"],z=a.Eg(h);a.c(z,function(b){(D||b["jssor-slider"])&&a.vb(b,a.vb(b),c)})}a.c(o,function(h,m){a.c(h,function(G){var K=G[0],J=G[1],v=K+","+J,o=i,s=i,x=i;if(p&&J%2){if(p&3)o=!o;if(p&12)s=!s;if(p&16)x=!x}if(q&&K%2){if(q&3)o=!o;if(q&12)s=!s;if(q&16)x=!x}d.g=d.g||d.a&4;d.p=d.p||d.a&8;d.f=d.f||d.a&1;d.o=d.o||d.a&2;var E=s?d.p:d.g,B=s?d.g:d.p,D=o?d.o:d.f,C=o?d.f:d.o;d.a=E||B||D||C;r={};e={g:0,f:0,s:1,P:n,O:l};f=a.n({},e);t=a.n({},g[v]);if(d.s)e.s=2-d.s;if(d.S){e.S=d.S;f.S=0}var I=d.q*d.U>1||d.a;if(d.j||d.r){var H=c;if(a.T())if(d.q*d.U>1)H=i;else I=i;if(H){e.j=d.j?d.j-1:1;f.j=1;if(a.T()||a.sc())e.j=b.min(e.j,2);var N=d.r||0;e.r=N*360*(x?-1:1);f.r=0}}if(I){var h=t.Db={};if(d.a){var w=d.ae||1;if(E&&B){h.g=g.O/2*w;h.p=-h.g}else if(E)h.p=-g.O*w;else if(B)h.g=g.O*w;if(D&&C){h.f=g.P/2*w;h.o=-h.f}else if(D)h.o=-g.P*w;else if(C)h.f=g.P*w}r.a=t;f.a=g[v]}var L=o?1:-1,M=s?1:-1;if(d.x)e.f+=n*d.x*L;if(d.y)e.g+=l*d.y*M;a.c(e,function(b,c){if(a.Xb(b))if(b!=f[c])r[c]=b-f[c]});u[v]=k?f:e;var F=d.Ie,A=b.round(m*d.K/d.Z);j[v]=new Array(A);j[v].Xd=A;j[v].Zd=A+F-1;for(var z=0;z<=F;z++){var y=a.rd(f,r,z/F,d.E,d.ec,d.cc,{V:d.V,Y:n,X:l});y.S=y.S||1;j[v].push(y)}})});o.reverse();a.c(o,function(b){a.c(b,function(c){var f=c[0],e=c[1],d=f+","+e,b=h;if(e||f)b=a.hb(h);a.ab(b,u[d]);a.tb(b,"hidden");a.A(b,"absolute");A.de(b);m[d]=b;a.z(b,!k)})})}function v(){var a=this,b=0;l.call(a,0,u);a.Kb=function(c,a){if(a-b>h){b=a;e&&e.ic(a);g&&g.ic(a)}};a.gb=r}f.Yd=function(){var a=0,c=t.pb,d=c.length;if(w)a=x++%d;else a=b.floor(b.random()*d);c[a]&&(c[a].ob=a);return c[a]};f.ee=function(w,x,j,l,a){r=a;a=k(a,h);var i=l.Uc,d=j.Uc;i["no-image"]=!l.fc;d["no-image"]=!j.fc;var m=i,o=d,v=a,c=a.nc||k({},h);if(!a.uc){m=d;o=i}var t=c.R||0;g=new p(n,o,c,b.max(t-c.Z,0),s,q);e=new p(n,m,v,b.max(c.Z-t,0),s,q);g.ic(0);e.ic(0);u=b.max(g.Rc,e.Rc);f.ob=w};f.Bb=function(){n.Bb();g=j;e=j};f.Vd=function(){var a=j;if(e)a=new v;return a};if(a.T()||a.sc()||y&&a.kg()<537)h=16;m.call(f);l.call(f,-1e7,1e7)};var h=e.$JssorSlider$=function(q,cc){var o=this;function yc(){var a=this;l.call(a,-1e8,2e8);a.Sd=function(){var c=a.Cb(),d=b.floor(c),f=t(d),e=c-b.floor(c);return{ob:f,jg:d,Eb:e}};a.Kb=function(d,a){var e=b.floor(a);if(e!=a&&a>d)e++;Rb(e,c);o.m(h.Le,t(a),t(d),a,d)}}function xc(){var b=this;l.call(b,0,0,{qd:r});a.c(C,function(a){D&1&&a.Je(r);b.zc(a);a.R(ib/Yb)})}function wc(){var a=this,b=Tb.L;l.call(a,-1,2,{E:d.dd,Mc:{Eb:Xb},qd:r},b,{Eb:1},{Eb:-2});a.dc=b}function jc(n,m){var a=this,d,e,f,k,b;l.call(a,-1e8,2e8,{Id:100});a.Jd=function(){M=c;S=j;o.m(h.Ae,t(w.W()),w.W())};a.zd=function(){M=i;k=i;var a=w.Sd();o.m(h.ze,t(w.W()),w.W());!a.Eb&&Ac(a.jg,s)};a.Kb=function(i,h){var a;if(k)a=b;else{a=e;if(f){var c=h/f;a=g.ye(c)*(e-d)+d}}w.u(a)};a.hc=function(b,g,c,h){d=b;e=g;f=c;w.u(b);a.u(0);a.td(c,h)};a.ve=function(d){k=c;b=d;a.ud(d,j,c)};a.se=function(a){b=a};w=new yc;w.F(n);w.F(m)}function lc(){var c=this,b=Vb();a.H(b,0);a.fb(b,"pointerEvents","none");c.L=b;c.de=function(c){a.J(b,c);a.z(b)};c.Bb=function(){a.Q(b);a.tc(b)}}function vc(n,e){var d=this,q,L,v,k,y=[],x,B,W,G,Q,F,f,w,p;l.call(d,-u,u+1,{});function E(b){q&&q.rb();T(n,b,0);F=c;q=new I.bb(n,I,a.mc(a.i(n,"idle"))||ic);q.u(0)}function Z(){q.qc<I.qc&&E()}function M(p,r,n){if(!G){G=c;if(k&&n){var f=n.width,b=n.height,m=f,l=b;if(f&&b&&g.Ab){if(g.Ab&3&&(!(g.Ab&4)||f>K||b>J)){var j=i,q=K/J*b/f;if(g.Ab&1)j=q>1;else if(g.Ab&2)j=q<1;m=j?f*J/b:K;l=j?J:b*K/f}a.k(k,m);a.l(k,l);a.G(k,(J-l)/2);a.I(k,(K-m)/2)}a.A(k,"absolute");o.m(h.re,e)}}a.Q(r);p&&p(d)}function Y(b,c,f,g){if(g==S&&s==e&&N)if(!zc){var a=t(b);A.ee(a,e,c,d,f);c.qe();U.R(a-U.Fc()-1);U.u(a);z.hc(b,b,0)}}function cb(b){if(b==S&&s==e){if(!f){var a=j;if(A)if(A.ob==e)a=A.Vd();else A.Bb();Z();f=new sc(n,e,a,q);f.Yc(p)}!f.yd()&&f.yc()}}function R(c,h,l){if(c==e){if(c!=h)C[h]&&C[h].me();else!l&&f&&f.je();p&&p.gd();var m=S=a.db();d.Fb(a.D(j,cb,m))}else{var k=b.min(e,c),i=b.max(e,c),o=b.min(i-k,k+r-i),n=u+g.Ke-1;(!Q||o<=n)&&d.Fb()}}function db(){if(s==e&&f){f.lb();p&&p.he();p&&p.xe();f.xd()}}function eb(){s==e&&f&&f.lb()}function ab(a){!P&&o.m(h.Ee,e,a)}function O(){p=w.pInstance;f&&f.Yc(p)}d.Fb=function(d,b){b=b||v;if(y.length&&!G){a.z(b);if(!W){W=c;o.m(h.Fe,e);a.c(y,function(b){if(!a.B(b,"src")){b.src=a.i(b,"src2");a.mb(b,b["display-origin"])}})}a.ge(y,k,a.D(j,M,d,b))}else M(d,b)};d.fe=function(){var h=e;if(g.Dc<0)h-=r;var c=h+g.Dc*qc;if(D&2)c=t(c);if(!(D&1))c=b.max(0,b.min(c,r-u));if(c!=e){if(A){var d=A.Yd(r);if(d){var i=S=a.db(),f=C[t(c)];return f.Fb(a.D(j,Y,c,f,d,i),v)}}bb(c)}};d.Cc=function(){R(e,e,c)};d.me=function(){p&&p.he();p&&p.xe();d.Kd();f&&f.be();f=j;E()};d.qe=function(){a.Q(n)};d.Kd=function(){a.z(n)};d.Ud=function(){p&&p.gd()};function T(b,d,e){if(a.B(b,"jssor-slider"))return;if(!F){if(b.tagName=="IMG"){y.push(b);if(!a.B(b,"src")){Q=c;b["display-origin"]=a.mb(b);a.Q(b)}}a.T()&&a.H(b,(a.H(b)||0)+1)}var f=a.N(b);a.c(f,function(f){var h=f.tagName,j=a.i(f,"u");if(j=="player"&&!w){w=f;if(w.pInstance)O();else a.e(w,"dataavailable",O)}if(j=="caption"){if(d){a.nd(f,a.i(f,"to"));a.rg(f,a.i(f,"bf"));a.sg(f,"preserve-3d")}else if(!a.Md()){var g=a.hb(f,i,c);a.Ob(g,f,b);a.ub(f,b);f=g;d=c}}else if(!F&&!e&&!k){if(h=="A"){if(a.i(f,"u")=="image")k=a.Dg(f,"IMG");else k=a.C(f,"image",c);if(k){x=f;a.mb(x,"block");a.ab(x,V);B=a.hb(x,c);a.A(x,"relative");a.vb(B,0);a.fb(B,"backgroundColor","#000")}}else if(h=="IMG"&&a.i(f,"u")=="image")k=f;if(k){k.border=0;a.ab(k,V)}}T(f,d,e+1)})}d.Gc=function(c,b){var a=u-b;Xb(L,a)};d.ob=e;m.call(d);a.tg(n,a.i(n,"p"));a.ug(n,a.i(n,"po"));var H=a.C(n,"thumb",c);if(H){d.Qd=a.hb(H);a.Q(H)}a.z(n);v=a.hb(fb);a.H(v,1e3);a.e(n,"click",ab);E(c);d.fc=k;d.sd=B;d.Uc=n;d.dc=L=n;a.J(L,v);o.yb(203,R);o.yb(28,eb);o.yb(24,db)}function sc(y,f,p,q){var b=this,m=0,u=0,g,j,e,d,k,t,r,n=C[f];l.call(b,0,0);function v(){a.tc(L);Zb&&k&&n.sd&&a.J(L,n.sd);a.z(L,!k&&n.fc)}function w(){b.yc()}function x(a){r=a;b.lb();b.yc()}b.yc=function(){var a=b.Cb();if(!B&&!M&&!r&&s==f){if(!a){if(g&&!k){k=c;b.xd(c);o.m(h.Td,f,m,u,g,d)}v()}var i,p=h.Wc;if(a!=d)if(a==e)i=d;else if(a==j)i=e;else if(!a)i=j;else i=b.Ad();o.m(p,f,a,m,j,e,d);var l=N&&(!E||F);if(a==d)(e!=d&&!(E&12)||l)&&n.fe();else(l||a!=e)&&b.td(i,w)}};b.je=function(){e==d&&e==b.Cb()&&b.u(j)};b.be=function(){A&&A.ob==f&&A.Bb();var a=b.Cb();a<d&&o.m(h.Wc,f,-a-1,m,j,e,d)};b.xd=function(b){p&&a.tb(jb,b&&p.gb.Yg?"":"hidden")};b.Gc=function(b,a){if(k&&a>=g){k=i;v();n.Kd();A.Bb();o.m(h.pe,f,m,u,g,d)}o.m(h.we,f,a,m,j,e,d)};b.Yc=function(a){if(a&&!t){t=a;a.yb($JssorPlayer$.ne,x)}};p&&b.zc(p);g=b.cb();b.zc(q);j=g+q.Tb;e=g+q.Vb;d=b.cb()}function Xb(g,f){var e=x>0?x:eb,c=zb*f*(e&1),d=Ab*f*(e>>1&1);c=b.round(c);d=b.round(d);a.I(g,c);a.G(g,d)}function Nb(){pb=M;Ib=z.Ad();G=w.W()}function ec(){Nb();if(B||!F&&E&12){z.lb();o.m(h.De)}}function bc(e){if(!B&&(F||!(E&12))&&!z.yd()){var c=w.W(),a=b.ceil(G);if(e&&b.abs(H)>=g.od){a=b.ceil(c);a+=hb}if(!(D&1))a=b.min(r-u,b.max(a,0));var d=b.abs(a-c);d=1-b.pow(1-d,5);if(!P&&pb)z.Rd(Ib);else if(c==a){sb.Ud();sb.Cc()}else z.hc(c,a,d*Sb)}}function Hb(b){!a.i(a.xc(b),"nodrag")&&a.Rb(b)}function oc(a){Wb(a,1)}function Wb(b,d){b=a.Od(b);var k=a.xc(b);if(!O&&!a.i(k,"nodrag")&&pc()&&(!d||b.touches.length==1)){B=c;yb=i;S=j;a.e(f,d?"touchmove":"mousemove",Bb);a.db();P=0;ec();if(!pb)x=0;if(d){var g=b.touches[0];ub=g.clientX;vb=g.clientY}else{var e=a.Fd(b);ub=e.x;vb=e.y}H=0;gb=0;hb=0;o.m(h.ff,t(G),G,b)}}function Bb(e){if(B){e=a.Od(e);var f;if(e.type!="mousemove"){var l=e.touches[0];f={x:l.clientX,y:l.clientY}}else f=a.Fd(e);if(f){var j=f.x-ub,k=f.y-vb;if(b.floor(G)!=G)x=x||eb&O;if((j||k)&&!x){if(O==3)if(b.abs(k)>b.abs(j))x=2;else x=1;else x=O;if(mb&&x==1&&b.abs(k)-b.abs(j)>3)yb=c}if(x){var d=k,i=Ab;if(x==1){d=j;i=zb}if(!(D&1)){if(d>0){var g=i*s,h=d-g;if(h>0)d=g+b.sqrt(h)*5}if(d<0){var g=i*(r-u-s),h=-d-g;if(h>0)d=-g-b.sqrt(h)*5}}if(H-gb<-2)hb=0;else if(H-gb>2)hb=-1;gb=H;H=d;rb=G-H/i/(Y||1);if(H&&x&&!yb){a.Rb(e);if(!M)z.ve(rb);else z.se(rb)}}}}}function ab(){nc();if(B){B=i;a.db();a.M(f,"mousemove",Bb);a.M(f,"touchmove",Bb);P=H;z.lb();var b=w.W();o.m(h.Me,t(b),b,t(G),G);E&12&&Nb();bc(c)}}function fc(c){if(P){a.mg(c);var b=a.xc(c);while(b&&v!==b){b.tagName=="A"&&a.Rb(c);try{b=b.parentNode}catch(d){break}}}}function hc(a){C[s];s=t(a);sb=C[s];Rb(a);return s}function Ac(a,b){x=0;hc(a);o.m(h.og,t(a),b)}function Rb(b,c){wb=b;a.c(T,function(a){a.Ec(t(b),b,c)})}function pc(){var b=h.id||0,a=X;if(mb)a&1&&(a&=1);h.id|=a;return O=a&~b}function nc(){if(O){h.id&=~X;O=0}}function Vb(){var b=a.sb();a.ab(b,V);a.A(b,"absolute");return b}function t(a){return(a%r+r)%r}function gc(a,c){if(c)if(!D){a=b.min(b.max(a+wb,0),r-u);c=i}else if(D&2){a=t(a+wb);c=i}bb(a,g.Qb,c)}function xb(){a.c(T,function(a){a.Qc(a.Pb.Vg<=F)})}function Cc(){if(!F){F=1;xb();if(!B){E&12&&bc();E&3&&C[s].Cc()}}}function Bc(){if(F){F=0;xb();B||!(E&12)||ec()}}function Dc(){V={P:K,O:J,g:0,f:0};a.c(Q,function(b){a.ab(b,V);a.A(b,"absolute");a.tb(b,"hidden");a.Q(b)});a.ab(fb,V)}function ob(b,a){bb(b,a,c)}function bb(f,e,l){if(Pb&&(!B&&(F||!(E&12))||g.md)){M=c;B=i;z.lb();if(e==k)e=Sb;var d=Cb.Cb(),a=f;if(l){a=d+f;if(f>0)a=b.ceil(a);else a=b.floor(a)}if(D&2)a=t(a);if(!(D&1))a=b.max(0,b.min(a,r-u));var j=(a-d)%r;a=d+j;var h=d==a?0:e*b.abs(j);h=b.min(h,e*u*1.5);z.hc(d,a,h||1)}}o.yg=bb;o.ud=function(){if(!N){N=c;C[s]&&C[s].Cc()}};o.pg=function(){return P};function W(){return a.k(y||q)}function lb(){return a.l(y||q)}o.Y=W;o.X=lb;function Eb(c,d){if(c==k)return a.k(q);if(!y){var b=a.sb(f);a.ed(b,a.ed(q));a.Ub(b,a.Ub(q));a.mb(b,"block");a.A(b,"relative");a.G(b,0);a.I(b,0);a.tb(b,"visible");y=a.sb(f);a.A(y,"absolute");a.G(y,0);a.I(y,0);a.k(y,a.k(q));a.l(y,a.l(q));a.nd(y,"0 0");a.J(y,b);var h=a.N(q);a.J(q,y);a.fb(q,"backgroundImage","");a.c(h,function(c){a.J(a.i(c,"noscale")?q:b,c);a.i(c,"autocenter")&&Jb.push(c)})}Y=c/(d?a.l:a.k)(y);a.xg(y,Y);var g=d?Y*W():c,e=d?c:Y*lb();a.k(q,g);a.l(q,e);a.c(Jb,function(b){var c=a.Wb(a.i(b,"autocenter"));a.Wd(b,c)})}o.ig=Eb;o.pd=function(a){var d=b.ceil(t(ib/Yb)),c=t(a-s+d);if(c>u){if(a-s>r/2)a-=r;else if(a-s<=-r/2)a+=r}else a=s+c-d;return a};m.call(o);o.L=q=a.qb(q);var g=a.n({Ab:0,Ke:1,Nc:1,Pc:0,Oc:i,ac:1,md:c,Dc:1,Ed:3e3,Cd:1,Qb:500,ye:d.jd,od:20,Lc:0,q:1,Ld:0,Pg:1,Kc:1,Pd:1},cc);if(g.Og!=k)g.Ed=g.Og;if(g.Ic!=k)g.q=g.Ic;if(g.Mg!=k)g.Ld=g.Mg;var eb=g.Kc&3,qc=(g.Kc&4)/-4||1,kb=g.dh,I=a.n({bb:p,Lg:1,Tg:1},g.ch);I.pb=I.pb||I.bh;var Fb=g.Ig,Z=g.Hg,db=g.ah,R=!g.Pg,y,v=a.C(q,"slides",R),fb=a.C(q,"loading",R)||a.sb(f),Lb=a.C(q,"navigator",R),dc=a.C(q,"arrowleft",R),ac=a.C(q,"arrowright",R),Kb=a.C(q,"thumbnavigator",R),mc=a.k(v),kc=a.l(v),V,Q=[],rc=a.N(v);a.c(rc,function(b){if(b.tagName=="DIV"&&!a.i(b,"u"))Q.push(b);else a.T()&&a.H(b,(a.H(b)||0)+1)});var s=-1,wb,sb,r=Q.length,K=g.Hd||mc,J=g.Fg||kc,Ub=g.Lc,zb=K+Ub,Ab=J+Ub,Yb=eb&1?zb:Ab,u=b.min(g.q,r),jb,x,O,yb,T=[],Ob,Qb,Mb,Zb,zc,N,E=g.Cd,ic=g.Ed,Sb=g.Qb,qb,tb,ib,Pb=u<r,D=Pb?g.ac:0,X,P,F=1,M,B,S,ub=0,vb=0,H,gb,hb,Cb,w,U,z,Tb=new lc,Y,Jb=[];N=g.Oc;o.Pb=cc;Dc();a.B(q,"jssor-slider",c);a.H(v,a.H(v)||0);a.A(v,"absolute");jb=a.hb(v,c);a.Ob(jb,v);if(kb){Zb=kb.Zg;qb=kb.bb;tb=u==1&&r>1&&qb&&(!a.Md()||a.wd()>=8)}ib=tb||u>=r||!(D&1)?0:g.Ld;X=(u>1||ib?eb:-1)&g.Pd;var Gb=v,C=[],A,L,Db=a.Ag(),mb=Db.Qg,G,pb,Ib,rb;Db.vd&&a.fb(Gb,Db.vd,([j,"pan-y","pan-x","none"])[X]||"");U=new wc;if(tb)A=new qb(Tb,K,J,kb,mb);a.J(jb,U.dc);a.tb(v,"hidden");L=Vb();a.fb(L,"backgroundColor","#000");a.vb(L,0);a.Ob(L,Gb.firstChild,Gb);for(var cb=0;cb<Q.length;cb++){var tc=Q[cb],uc=new vc(tc,cb);C.push(uc)}a.Q(fb);Cb=new xc;z=new jc(Cb,U);if(X){a.e(v,"mousedown",Wb);a.e(v,"touchstart",oc);a.e(v,"dragstart",Hb);a.e(v,"selectstart",Hb);a.e(f,"mouseup",ab);a.e(f,"touchend",ab);a.e(f,"touchcancel",ab);a.e(e,"blur",ab)}E&=mb?10:5;if(Lb&&Fb){Ob=new Fb.bb(Lb,Fb,W(),lb());T.push(Ob)}if(Z&&dc&&ac){Z.ac=D;Z.q=u;Qb=new Z.bb(dc,ac,Z,W(),lb());T.push(Qb)}if(Kb&&db){db.Pc=g.Pc;Mb=new db.bb(Kb,db);T.push(Mb)}a.c(T,function(a){a.Ac(r,C,fb);a.yb(n.bc,gc)});a.fb(q,"visibility","visible");Eb(W());a.e(v,"click",fc);a.e(q,"mouseout",a.Ib(Cc,q));a.e(q,"mouseover",a.Ib(Bc,q));xb();g.Nc&&a.e(f,"keydown",function(a){if(a.keyCode==37)ob(-g.Nc);else a.keyCode==39&&ob(g.Nc)});var nb=g.Pc;if(!(D&1))nb=b.max(0,b.min(nb,r-u));z.hc(nb,nb,0)};h.Ee=21;h.ff=22;h.Me=23;h.Ae=24;h.ze=25;h.Fe=26;h.re=27;h.De=28;h.Le=202;h.og=203;h.Td=206;h.pe=207;h.we=208;h.Wc=209;var n={bc:1},q=e.$JssorBulletNavigator$=function(e,C){var f=this;m.call(f);e=a.qb(e);var s,A,z,r,l=0,d,o,k,w,x,h,g,q,p,B=[],y=[];function v(a){a!=-1&&y[a].hd(a==l)}function t(a){f.m(n.bc,a*o)}f.L=e;f.Ec=function(a){if(a!=r){var d=l,c=b.floor(a/o);l=c;r=a;v(d);v(c)}};f.Qc=function(b){a.z(e,b)};var u;f.Ac=function(D){if(!u){s=b.ceil(D/o);l=0;var n=q+w,r=p+x,m=b.ceil(s/k)-1;A=q+n*(!h?m:k-1);z=p+r*(h?m:k-1);a.k(e,A);a.l(e,z);for(var f=0;f<s;f++){var C=a.ng();a.Kg(C,f+1);var i=a.ld(g,"numbertemplate",C,c);a.A(i,"absolute");var v=f%(m+1);a.I(i,!h?n*v:f%k*n);a.G(i,h?r*v:b.floor(f/(m+1))*r);a.J(e,i);B[f]=i;d.wb&1&&a.e(i,"click",a.D(j,t,f));d.wb&2&&a.e(i,"mouseover",a.Ib(a.D(j,t,f),i));y[f]=a.Yb(i)}u=c}};f.Pb=d=a.n({lc:10,kc:10,zb:1,wb:1},C);g=a.C(e,"prototype");q=a.k(g);p=a.l(g);a.ub(g,e);o=d.wc||1;k=d.ad||1;w=d.lc;x=d.kc;h=d.zb-1;d.Zc==i&&a.B(e,"noscale",c);d.eb&&a.B(e,"autocenter",d.eb)},r=e.$JssorArrowNavigator$=function(b,g,h){var d=this;m.call(d);var r,q,e,f,k;a.k(b);a.l(b);function l(a){d.m(n.bc,a,c)}function p(c){a.z(b,c||!h.ac&&e==0);a.z(g,c||!h.ac&&e>=q-h.q);r=c}d.Ec=function(b,a,c){if(c)e=a;else{e=b;p(r)}};d.Qc=p;var o;d.Ac=function(d){q=d;e=0;if(!o){a.e(b,"click",a.D(j,l,-k));a.e(g,"click",a.D(j,l,k));a.Yb(b);a.Yb(g);o=c}};d.Pb=f=a.n({wc:1},h);k=f.wc;if(f.Zc==i){a.B(b,"noscale",c);a.B(g,"noscale",c)}if(f.eb){a.B(b,"autocenter",f.eb);a.B(g,"autocenter",f.eb)}};e.$JssorThumbnailNavigator$=function(g,C){var l=this,A,q,d,w=[],y,x,e,r,s,v,u,p,t,f,o;m.call(l);g=a.qb(g);function B(m,f){var g=this,b,k,i;function p(){k.hd(q==f)}function h(d){if(d||!t.pg()){var a=e-f%e,b=t.pd((f+a)/e-1),c=b*e+e-a;l.m(n.bc,c)}}g.ob=f;g.Sc=p;i=m.Qd||m.fc||a.sb();g.dc=b=a.ld(o,"thumbnailtemplate",i,c);k=a.Yb(b);d.wb&1&&a.e(b,"click",a.D(j,h,0));d.wb&2&&a.e(b,"mouseover",a.Ib(a.D(j,h,1),b))}l.Ec=function(c,d,f){var a=q;q=c;a!=-1&&w[a].Sc();w[c].Sc();!f&&t.yg(t.pd(b.floor(d/e)))};l.Qc=function(b){a.z(g,b)};var z;l.Ac=function(D,C){if(!z){A=D;b.ceil(A/e);q=-1;p=b.min(p,C.length);var j=d.zb&1,m=v+(v+r)*(e-1)*(1-j),l=u+(u+s)*(e-1)*j,o=m+(m+r)*(p-1)*j,n=l+(l+s)*(p-1)*(1-j);a.A(f,"absolute");a.tb(f,"hidden");d.eb&1&&a.I(f,(y-o)/2);d.eb&2&&a.G(f,(x-n)/2);a.k(f,o);a.l(f,n);var k=[];a.c(C,function(l,g){var h=new B(l,g),d=h.dc,c=b.floor(g/e),i=g%e;a.I(d,(v+r)*i*(1-j));a.G(d,(u+s)*i*j);if(!k[c]){k[c]=a.sb();a.J(f,k[c])}a.J(k[c],d);w.push(h)});var E=a.n({Oc:i,md:i,Hd:m,Fg:l,Lc:r*j+s*(1-j),od:12,Qb:200,Cd:1,Kc:d.zb,Pd:d.Wg||d.Xg?0:d.zb},d);t=new h(g,E);z=c}};l.Pb=d=a.n({lc:0,kc:0,q:1,zb:1,eb:3,wb:1},C);if(d.Ic!=k)d.q=d.Ic;if(d.U!=k)d.ad=d.U;y=a.k(g);x=a.l(g);f=a.C(g,"slides",c);o=a.C(f,"prototype");v=a.k(o);u=a.l(o);a.ub(o,f);e=d.ad||1;r=d.lc;s=d.kc;p=d.q;d.Zc==i&&a.B(g,"noscale",c)};function p(e,d,c){var b=this;l.call(b,0,c);b.rb=a.Xc;b.Tb=0;b.Vb=c}e.$JssorCaptionSlider$=function(h,f,i){var c=this;l.call(c,0,0);var e,d;function g(p,h,f){var c=this,g,n=f?h.Lg:h.Tg,e=h.pb,o={gb:"t",K:"d",gc:"du",x:"x",y:"y",r:"r",j:"z",s:"f",xb:"b"},d={nb:function(b,a){if(!isNaN(a.ib))b=a.ib;else b*=a.Kf;return b},s:function(b,a){return this.nb(b-1,a)}};d.j=d.s;l.call(c,0,0);function j(r,m){var l=[],i,k=[],c=[];function h(c,d){var b={};a.c(o,function(g,h){var e=a.i(c,g+(d||""));if(e){var f={};if(g=="t")f.ib=e;else if(e.indexOf("%")+1)f.Kf=a.mc(e)/100;else f.ib=a.mc(e);b[h]=f}});return b}function p(){return e[b.floor(b.random()*e.length)]}function g(f){var h;if(f=="*")h=p();else if(f){var d=e[a.Wb(f)]||e[f];if(a.rc(d)){if(f!=i){i=f;c[f]=0;k[f]=d[b.floor(b.random()*d.length)]}else c[f]++;d=k[f];if(a.rc(d)){d=d.length&&d[c[f]%d.length];if(a.rc(d))d=d[b.floor(b.random()*d.length)]}}h=d;if(a.Dd(h))h=g(h)}return h}var q=a.N(r);a.c(q,function(b){var c=[];c.L=b;var e=a.i(b,"u")=="caption";a.c(f?[0,3]:[2],function(l,o){if(e){var k,f;if(l!=2||!a.i(b,"t3")){f=h(b,l);if(l==2&&!f.gb){f.K=f.K||{ib:0};f=a.n(h(b,0),f)}}if(f&&f.gb){k=g(f.gb.ib);if(k){var i=a.n({K:0},k);a.c(f,function(c,a){var b=(d[a]||d.nb).apply(d,[i[a],f[a]]);if(!isNaN(b))i[a]=b});if(!o)if(f.xb)i.xb=f.xb.ib||0;else if(n&2)i.xb=0}}c.push(i)}if(m%2&&!o)c.N=j(b,m+1)});l.push(c)});return l}function m(w,c,z){var g={E:c.E,cc:c.cc,ec:c.ec,Hc:f&&!z},m=w,r=a.bd(w),k=a.k(m),j=a.l(m),y=a.k(r),x=a.l(r),h={},e={},i=c.ae||1;if(c.s)e.s=1-c.s;g.Y=k;g.X=j;if(c.j||c.r){e.j=(c.j||2)-2;if(a.T()||a.sc())e.j=b.min(e.j,1);h.j=1;var B=c.r||0;e.r=B*360;h.r=0}else if(c.a){var s={g:0,o:k,p:j,f:0},v=a.n({},s),d=v.Db={},u=c.a&4,p=c.a&8,t=c.a&1,q=c.a&2;if(u&&p){d.g=j/2*i;d.p=-d.g}else if(u)d.p=-j*i;else if(p)d.g=j*i;if(t&&q){d.f=k/2*i;d.o=-d.f}else if(t)d.o=-k*i;else if(q)d.f=k*i;g.V=c.V;e.a=v;h.a=s}var n=0,o=0;if(c.x)n-=y*c.x;if(c.y)o-=x*c.y;if(n||o||g.V){e.f=n;e.g=o}var A=c.gc;h=a.n(h,a.ke(m,e));g.Mc=a.Tc();return new l(c.K,A,g,m,h,e)}function i(b,d){a.c(d,function(d){var a,h=d.L,f=d[0],j=d[1];if(f){a=m(h,f);f.xb==k&&a.R(b);b=a.cb()}b=i(b,d.N);if(j){var e=m(h,j,1);e.R(b);c.F(e);g.F(e)}a&&c.F(a)});return b}c.rb=function(){c.u(c.cb()*(f||0));g.u(0)};g=new l(0,0);i(0,n?j(p,1):[])}c.rb=function(){d.rb();e.rb()};e=new g(h,f,1);c.Tb=e.cb();c.Vb=c.Tb+i;d=new g(h,f);d.R(c.Vb);c.F(d);c.F(e)};e.$JssorCaptionSlideo$=function(n,f,m){var b=this,o,h={},i=f.pb,d=new l(0,0);l.call(b,0,0);function j(d,c){var b={};a.c(d,function(d,f){var e=h[f];if(e){if(a.wg(d))d=j(d,c||f=="e");else if(c)if(a.Xb(d))d=o[d];b[e]=d}});return b}function k(e,c){var b=[],d=a.N(e);a.c(d,function(d){var h=a.i(d,"u")=="caption";if(h){var e=a.i(d,"t"),g=i[a.Wb(e)]||i[e],f={L:d,gb:g};b.push(f)}if(c<5)b=b.concat(k(d,c+1))});return b}function r(c,e,b){a.c(e,function(f){var e=j(f),h={E:a.Bc(e.E),Mc:a.Tc(),Y:b.P,X:b.O},g=new l(f.b,f.d,h,c,b,e);d.F(g);b=a.He(b,e)});return b}function q(b){a.c(b,function(c){var b=c.L,e=a.k(b),d=a.l(b),f={f:a.I(b),g:a.G(b),s:1,S:a.H(b)||0,r:0,Hb:0,Gb:0,jb:1,kb:1,Nb:0,Mb:0,Lb:0,Jb:0,Zb:0,P:e,O:d,a:{g:0,o:e,p:d,f:0}};r(b,c.gb,f)})}function t(g,f,h){var e=g.b-f;if(e){var a=new l(f,e);a.F(d,c);a.R(h);b.F(a)}b.ie(g.d);return e}function s(f){var c=d.Fc(),e=0;a.c(f,function(d,f){d=a.n({d:m},d);t(d,c,e);c=d.b;e+=d.d;if(!f||d.t==2){b.Tb=c;b.Vb=c+d.d}})}b.rb=function(){b.u(-1,c)};o=[g.vf,g.uf,g.lf,g.Ne,g.Oe,g.Pe,g.Qe,g.Re,g.Se,g.Te,g.Ue,g.Ve,g.We,g.Xe,g.Ye,g.Ze,g.af,g.bf,g.cf,g.df,g.sf,g.rf,g.qf,g.pf,g.of,g.nf,g.tf,g.mf,g.kf,g.jf,g.hf,g.gf,g.fg,g.ef,g.Mf,g.eg,g.vg];var u={g:"y",f:"x",p:"m",o:"t",r:"r",Hb:"rX",Gb:"rY",jb:"sX",kb:"sY",Nb:"tX",Mb:"tY",Lb:"tZ",Jb:"kX",Zb:"kY",s:"o",E:"e",S:"i",a:"c"};a.c(u,function(b,a){h[b]=a});q(k(n,1));d.u(-1);var p=f.fh||[],e=[].concat(p[a.Wb(a.i(n,"b"))]||[]);e.push({b:d.cb(),d:e.length?0:m});s(e);b.u(-1)};jssor_1_slider_init=function(){var g={Oc:c,Dc:4,Qb:160,Hd:200,Lc:3,q:4,Hg:{bb:r,wc:4},Ig:{bb:q,lc:1,kc:1}},f=new h("jssor_1",g);function d(){var a=f.L.parentNode.clientWidth;if(a){a=b.min(a,809);f.ig(a)}else e.setTimeout(d,30)}d();a.e(e,"load",d);a.e(e,"resize",a.zg(e,d));a.e(e,"orientationchange",d)}}(window,document,Math,null,true,false)

          </script>

          <style>

          .jssorb03{position:absolute}.jssorb03 div,.jssorb03 div:hover,.jssorb03 .av{position:absolute;width:21px;height:21px;text-align:center;line-height:21px;color:#fff;font-size:12px;background:url('static/images/img/b03.png') no-repeat;overflow:hidden;cursor:pointer}.jssorb03 div{background-position:-5px -4px}.jssorb03 div:hover,.jssorb03 .av:hover{background-position:-35px -4px}.jssorb03 .av{background-position:-65px -4px}.jssorb03 .dn,.jssorb03 .dn:hover{background-position:-95px -4px}.jssora03l,.jssora03r{display:block;position:absolute;width:55px;height:55px;cursor:pointer;background:url('static/images/img/a03.png') no-repeat;overflow:hidden}.jssora03l{background-position:-3px -33px}.jssora03r{background-position:-63px -33px}.jssora03l:hover{background-position:-123px -33px}.jssora03r:hover{background-position:-183px -33px}.jssora03l.jssora03ldn{background-position:-243px -33px}.jssora03r.jssora03rdn{background-position:-303px -33px}

          </style>


          <div id="jssor_1" style="position: relative; margin: 0 auto; top: 0px; left: 0px; width: 809px; height: 200px; overflow: hidden; visibility: hidden;">
            <!-- Loading Screen -->
            <div data-u="loading" style="position: absolute; top: 0px; left: 0px;">
              <div style="filter: alpha(opacity=70); opacity: 0.7; position: absolute; display: block; top: 0px; left: 0px; width: 100%; height: 100%;"></div>
              <div style="position:absolute;display:block;background:url('img/loading.gif') no-repeat center center;top:0px;left:0px;width:100%;height:100%;"></div>
            </div>
            <div data-u="slides" style="cursor: default; position: relative; top: 0px; left: 0px; width: 809px; height: 200px; overflow: hidden;">
                  % for d in dados:
                  
                    <div id="grop" class="large-3 small-6 columns" style="margin: 0 !important;" data-reveal-id="myModal{{d['id']}}">
                      <img src="/static/images/1000x400&text=Slide Image.png">
                      <div class="panel">
                        <p style="margin: 4px auto !important;">{{d['nome']}}</p>
                        <!--
                        <p style="margin: 4px auto !important;">ativedd_economica</p>
                        <p style="margin: 4px auto !important;">localizacao</p>
                        -->
                      </div>
                    </div>  
                                              
                  % end                  
            </div>

            % for d2 in dados:
              <div id="myModal{{d2['id']}}" class="reveal-modal" data-reveal aria-labelledby="modalTitle" aria-hidden="true" role="dialog">
                    <div class="row">
                      <div class="large-12 small-5 columns">
                        <img src="/static/images/1000x400&text=Slide Image.png" style="height: 200px !important; width: 100% !important;">
                      </div>
                    </div>

                    <div class="row">
                      <div class="large-5 small-5 columns" style="background-color: #EEEEEE;">
                          <h5 style="float: right; font-weight: bold !important;">1. Nome:</h5>
                      </div>
                      <div class="large-7 small-7 columns">
                          <h6>{{d2['nome']}}</h6>
                      </div>
                    </div>

                    <div class="row">
                      <div class="large-5 small-5 columns" style="background-color: #EEEEEE;">
                          <h5 style="float: right; font-weight: bold !important;">2. Email:</h5>
                      </div>
                      <div class="large-7 small-7 columns">
                          <h6>{{d2['email']}}</h6>
                      </div>
                    </div>

                    <div class="row">
                      <div class="large-5 small-5 columns" style="background-color: #EEEEEE;">
                          <h5 style="float: right; font-weight: bold !important;">3. Freguesias:</h5>
                      </div>
                      <div class="large-7 small-7 columns">
                          <h6>{{d2['pais']}}</h6>
                      </div>
                    </div>

                    <div class="row">
                      <div class="large-5 small-5 columns" style="background-color: #EEEEEE;">
                          <h5 style="float: right; font-weight: bold !important;">4. Localização:</h5>
                      </div>
                      <div class="large-7 small-7 columns">
                          <h6>{{d2['localizacao']}}</h6>
                      </div>
                    </div>

                    <div class="row">
                      <div class="large-5 small-5 columns" style="background-color: #EEEEEE;">
                          <h5 style="float: right; font-weight: bold !important;">5. Tipo de Empresa:</h5>
                      </div>
                      <div class="large-7 small-7 columns">
                          <h6>{{d2['tipo']}}</h6>
                      </div>
                    </div>

                    <div class="row">
                      <div class="large-5 small-5 columns" style="background-color: #EEEEEE;">
                          <h5 style="float: right; font-weight: bold !important;">6. Actividade económica:</h5>
                      </div>
                      <div class="large-7 small-7 columns">
                          <h6>{{d2['ativedd_economica']}}</h6>
                      </div>
                    </div>

                    <a class="close-reveal-modal" aria-label="Close">&#215;</a>
                  </div>    
            % end

            <!-- Bullet Navigator -->
            <div data-u="navigator" class="jssorb03" style="bottom:10px;right:10px;">
              <!-- bullet navigator item prototype -->
              <div data-u="prototype" style="width:21px;height:21px;">
                <div data-u="numbertemplate"></div>
              </div>
            </div>
            <!-- Arrow Navigator -->
            <span data-u="arrowleft" class="jssora03l" style="top:0px;left:0px;width:55px;height:55px;" data-autocenter="2"></span>
            <span data-u="arrowright" class="jssora03r" style="top:0px;right:0px;width:55px;height:55px;" data-autocenter="2"></span>
          </div>
          <script>
          jssor_1_slider_init();
          </script>
          <!--/////////////////////////////////////////////////////////////////////////////////////////-->
              
          <br/> 
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

  <script src="/static/js/cp.js" type="text/javascript"></script>  

  <script type="text/javascript" src="code.jquery.com/jquery-1.11.0.min.js"></script>
  <script type="text/javascript" src="code.jquery.com/jquery-migrate-1.2.1.min.js"></script>
  <script type="text/javascript" src="/static/slick/slick/slick.min.js"></script>

  <script type="text/javascript">
    $(document).ready(function(){
      $('.your-class').slick({
        setting-name: setting-value
      });
    });
  </script>

  <script type="text/javascript">
    function regist_forneced(){
      
      var strURL = '/registFornecd';
      var nomeForn = '';
      var nomeForn = nomeForn+$('#fornecName').val();

      var myform = $('#form_registForncd');
      var disabled = myform.find(':input:disabled').removeAttr('disabled');
      var serialized = myform.serialize();

      disabled.attr('disabled','disabled');
      //alert(String(serialized));

      if(nomeForn !== ''){
          $.ajax({type: 'POST', url: strURL, data: serialized
          }).done(function(r) {
              $('#mnsconfr').html('<div data-alert class="alert-box success radius">Gravado com sucesso!<a href="#" class="close">&times;</a></div>'); 
                document.getElementById("form_registForncd").reset(); 
              //$('#form_registForncd').resetForm();            
              //alert(r);             
          }).fail(function(r) {
              $('#mnsconfr').html('<div data-alert class="alert-box alert round">This is an alert - alert that is rounded.<a href="#" class="close">&times;</a></div>');
               //alert('False');
          });
      }else{
          $('#mnsconfr').html('<div data-alert class="alert-box alert round">Por favor verifica o seu NIF no ícone de pesquisa! <a href="#" class="close">&times;</a></div>');
      }
      
    }

    function get_dados(){
      $('#mnsconfr').html(' ');
      var nifForn = $('#fornecNif').val();
      var strURL = '/getdadosFornecd/'+nifForn;
      
      $.ajax({type: 'GET', url: strURL
          }).done(function(r) {
              var arrayOfObjects = JSON.parse(r);
              var fornecName = arrayOfObjects.dadosFornec[0].nome;
              var fornecEmail = arrayOfObjects.dadosFornec[0].email;
              var area_servico = arrayOfObjects.dadosFornec[0].actividade_economica;
              var fornecLocalizacao = arrayOfObjects.dadosFornec[0].localizacao;
              var pais_empresa = arrayOfObjects.dadosFornec[0].freguesia;

              $('#fornecName').val(fornecName);
              $('#fornecEmail').val(fornecEmail);
              $('#area_servico').val(area_servico);
              $('#fornecLocalizacao').val(fornecLocalizacao);
              $('#pais_empresa').val(pais_empresa);

          }).fail(function(r) {
               $('#mnsconfr').html('<div data-alert class="alert-box alert round">Problemas ao identificar NIF!<br /> Por favor verifica o seu NIF.<a href="#" class="close">&times;</a></div>');
          });

    } 

    function callPage(page,pagelimit){     
      /*var maxnumpage = pagelimit / 4;*/
      var maxnumpage = parseInt(pagelimit / 4) + 1;
      for(i=1;i<=maxnumpage;i++){
        if(i==page){
          document.getElementById('ativo'+page).className = 'current';
        }else{
          document.getElementById('ativo'+i).className = '';
        }
        
      }  
      
      var strURL = '/get_page/'+page+'/'+pagelimit ;
      $.ajax({type: 'GET', url: strURL
          }).done(function(r) {
              $('#pagup').html(r);
          }).fail(function(r) {
              $('#pagup').html('Erro');
          });
      $('#message').html('');
      
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
