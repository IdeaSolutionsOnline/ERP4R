% setdefault('menu', '')
% setdefault('enterprise', '')
% setdefault('favicon', '')
% setdefault('user_name', '')
% setdefault('title', '')
% setdefault('form', '')
% setdefault('side_bar', '')
% setdefault('use_logotipo',False)
% #print('Im in base------------------------------------')
<!DOCTYPE html>
<html  class="no-js" lang="pt-PT"><!--manifest="/static/main.manifest"-->
  <head>
    <meta charset="utf-8">
    <title>{{!title}}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="ERP +">
    <meta name="author" content="António Anacleto">

    <!-- Le styles -->
    <link href="/static/css/normalize.css" rel="stylesheet">
    <link href="/static/css/foundation.min.css" rel="stylesheet">
    <link href="/static/css/foundation-icons.css" rel="stylesheet">
    <link href="/static/css/erp.css" rel="stylesheet">
    <link rel="shortcut icon" href="/static/{{favicon}}">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="/static/js/html5.js"></script>
    <![endif]-->

    <style type="text/css">
      td {
        border-right: 1px solid #ccc !important;
        border-bottom: 1px solid #ccc !important;
        padding: 5px !important;
      }

    </style>
    <script type="text/javascript">
      function Ocultar(){
          var ref_select = document.getElementById('tipo_c');
          var ref_input1 = document.getElementById('data_inicio');
          var ref_input2 = document.getElementById('data_limit_esclar');
          var ref_input3 = document.getElementById('data_ente_doc');
          var ref_input4 = document.getElementById('hora_ente_doc');
          var ref_input5 = document.getElementById('data_acto_publico');
          var ref_input6 = document.getElementById('hora_acto_publico');
          
          for( i = 0;i < ref_select.length;i++){ 
            if(ref_select.options[i].selected == true){
              var var_id =ref_select.options[ref_select.selectedIndex].value;  
              var indc=i;
            }    
          } 

          if(indc==1 || indc==2 || indc==3){
            ref_input1.disabled = false;
            ref_input2.disabled = false;
            ref_input3.disabled = false;
            ref_input4.disabled = false;
            ref_input5.disabled = false;
            ref_input6.disabled = false;
          }else{
            ref_input1.disabled = true;
            ref_input2.disabled = true;
            ref_input3.disabled = true;
            ref_input4.disabled = true;
            ref_input5.disabled = true;
            ref_input6.disabled = true;
          }
          
      }
    </script>

    <script src="/static/js/modernizr.js"></script>

  </head>

  <body>

<div id='loadingDiv' style='position:absolute; top:0px; left:0px; z-index: 100; height: 100%; width: 100%; display:flex; vertical-align:middle; text-align:center; background: #fff; filter:alpha(opacity=55); opacity:.55;
   color: #000;'>
   <div style="display:block; margin:auto;">
    Aguarde ...  <br><br>
    <img src='/static/images/RunningWoman.gif'/>
    </div>
 </div>

<div class="fixed">

<nav class="top-bar" data-topbar data-options="is_hover: false">

  <ul class="title-area">
    <li class="name">
      %if use_logotipo == True:
          <a href="#"><img src='/static/{{!logotipo}}'/></a>
      %else:
          <h2><a href="#">{{!enterprise}}</a></h2>
      %end
    </li>
  </ul>

  <section class="top-bar-section">
    <!-- Left Nav Section -->
      {{!menu}}
    <!-- Right Nav Section -->
    <ul class="right">
      <li class="active radius"><a href="{{url}}"> <i class="fi-power"></i> &nbsp; {{!user_name}}</a></li>
    </ul>
  </section>
</nav>
</div>

<div data-alert  id="message_container" style="display:none" class="alert-box info radius">
  <div id="message" style="color:black;"></div>
  <a href="#" class="close">&times;</a>
</div>

<!-- Modal -->

<div id="popup" class="reveal-modal" data-reveal>
<div data-alert  id="popup_message_container" style="display:none" class="alert-box info radius">
  <div id="popup_message"></div>
  <a href="#" class="close">&times;</a>
</div>
  <h2 id="popupLabel"></h2>
    <form data-abide id="popupForm" method="post">
      <fieldset>
      <input name="window_id" type="hidden" id="popup_window_id" value="{{window_id}}"></input>
      <div id="popupContent">
<!--<a href="#" data-reveal-id="popup" data-reveal>Click Me For A Modal</a>-->
      </div>
      </fieldset>
    </form>
  <a class="close-reveal-modal">&#215;</a>
</div>

<div class="off-canvas-wrap">
<div class="inner-wrap">
<div class="">
  <section class="right-small" style="background:black;">
    <a class="right-off-canvas-toggle menu-icon" ><span></span></a>
  </section>
  <div class="main-section">
    <form data-abide id="erpForm" method="post">
      <fieldset>
      <input name="window_id" type="hidden" id="window_id" value="{{window_id}}"></input><!---->
    	<div id="content">
<!--<a href="#" data-reveal-id="popup" data-reveal>Click Me For A Modal</a>-->
          %#print ('before form')
      		{{!form}}
          %#print ('after form')
    </div>
    </fieldset>
		</form>
  </div>

  <aside class="right-off-canvas-menu" id="SideBarContent">
    <form data-abide id="sidebar" method="post">
    <ul class="off-canvas-list">
      <li><label>Acções e Relatórios</label></li>
      <li>
        <div id="calculator">
          <label>Calculadora</label>
          <div class="small-9 columns">
            <input name="calc" placeholder="Calculadora (+ - * /)" size="15mm" id="calc_input" tabindex=-1 onkeypress="handleEnter( event, 'calc', '', '');"></input>
          </div>
          <div class="small-3 columns">
            <a href="#" class="postfix button tiny" onclick="run_calc();">
              <i class="fi-dollar"></i>
            </a>
          </div>
        <div id="calc" style="width:100%; border-style:solid; border-color:white; color:white; text-align:center;">0</div>
        </div>
      </li>
      <li><div class="fileinputs">
        <label>Importar</label>
        <input size="15mm" type="file" name="fileCSV" class="file" id="file" onchange="$(choose).update($(file).value)"></input>
        <div class="fakefile" size="15mm" >
          <div size="15mm" id="choose" style="color:white;">Escolher CSV!</div>
        </div>
        <div class="import_button" onclick="importCSV('{{name}}');" style="color:white;">Importar</div><p>
        <input type=submit id='fake_submit' hidden>
      </div></li>
        <li><div id="sidebar_contents">
          <label>Outros</label>
          %#print ('before side_bar')
          {{!side_bar}}
          %#print ('after side_bar')
        </div></li>
      </ul>
      <form>
    </aside>
      <footer id="erpFooter">
        <p>&copy; ERP+ 2015</p>
      </footer>

    </div>
    <!--/.fluid-container-->

    <!-- javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/static/js/jquery.min.js"></script>
    <script src="/static/js/fastclick.js"></script>
    <script src="/static/js/foundation.min.js"></script>
    <script src="/static/js/erp.js" charset="UTF-8"></script>

    <script>
      $(document).foundation();

      $( document ).ajaxStart(function() {
          $( "#loadingDiv" ).show();
      });

      $( document ).ajaxStop(function() {
          $( "#loadingDiv" ).hide();
      });

      function get_new_window_id(){
        $('#message').html('');
        var strURL = '/get_new_window_id/' + window.name + '_' + $('#window_id').val();
        $.ajax({type: 'POST', url: strURL
            }).done(function(r) {
                if (!(window.name)) {
                  window.name = r;
                  $('#window_id').val(r);
                  $('#popup_window_id').val(r);
                };
            }).fail(function(r) {
                $('#message_container').removeClass('success').removeClass('info').addClass('alert');
                $('#message_container').show();
                $('#message').html(r.responseText);
            });
        };

      Foundation.utils.debounce(get_new_window_id(), 300, true);

      $('#window_id').val(window.name);
      $('#popup_window_id').val(window.name);

      <!--permite que quando o modal fecha o window_status retorne a edit-->
      $(document).on('closed', '#popup[data-reveal]', function () {
        var strURL = '/popup_close/' + window.name;
        $.ajax({type: 'POST', url: strURL
            });
      });

    </script>

  </body>
</html>
