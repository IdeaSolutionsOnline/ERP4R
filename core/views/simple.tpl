% #print('Im in simple------------------------------------')
<!DOCTYPE html>
<html  class="no-js" lang="pt-PT"><!--manifest="/static/main.manifest"-->
  <head>
    <meta charset="utf-8">
    <title>Plano de Atividades</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Plano de Atividades">
    <meta name="author" content="António Anacleto">

    <!-- Le styles -->
    <link href="/mfptask/static/css/normalize.css" rel="stylesheet">
    <link href="/mfptask/static/css/foundation.min.css" rel="stylesheet">
    <link href="/mfptask/static/css/foundation-icons.css" rel="stylesheet">
    <link href="/mfptask/static/css/erp.css" rel="stylesheet">

    <link rel="shortcut icon" href="/static/favicon.png">

    <!-- HTML5 shim, for IE6-8 support of HTML5 elements -->
    <!--[if lt IE 9]>
      <script src="/static/js/html5.js"></script>
    <![endif]-->

    <script src="/mfptask/static/js/modernizr.js"></script>

    <script src="/mfptask/static/ckeditor/ckeditor.js"></script>

  </head>

  <body>

<div id='loadingDiv' class='overlay' style='display:flex; vertical-align:middle; text-align:center; background: #fff; filter:alpha(opacity=55); opacity:.55;
   color: #000;'>
   <div style="display:block; margin:auto;">
    Aguarde ...  <br><br>
    <img src='/mfptask/static/images/RunningWoman.gif'/>
    </div>
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
    <form id="popupForm" method="post">
      <fieldset>
        <div id="popupContent">
        </div>
<!--<a href="#" data-reveal-id="popup" data-reveal>Click Me For A Modal</a>-->
      </fieldset>
    </form>
  <a class="close-reveal-modal" id="close_popup">&#215;</a>
</div>

<div class="off-canvas-wrap">
<div class="inner-wrap">
<div class="">
  <div class="main-section">

    <form id="mainForm" method="post">
        <fieldset id="content">
          %#print ('before form')
            {{!form}}
          %#print ('after form')
    </fieldset>
        </form>
  </div>

      <footer>
        <p>&copy; <small>DGRSI@Ministério das Finanças de Cabo Verde (2014)</small></p>
      </footer>

    </div><!--/.fluid-container-->

    <!-- javascript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="/mfptask/static/js/jquery.min.js"></script>
    <script src="/mfptask/static/js/fastclick.js"></script>
    <script src="/mfptask/static/js/foundation.min.js"></script>
    <script src="/mfptask/static/js/erp.js"></script>

    <script>
      $(document).foundation();

      $( document ).ajaxStart(function() {
          $( "#loadingDiv" ).show();
      });

      $( document ).ajaxStop(function() {
          $( "#loadingDiv" ).hide();
      });

      function dummy(){
        $('#message').html('');
        var strURL = '/mfptask/dummy/';
        $.ajax({type: 'GET', url: strURL
            }).done(function(r) {
                if (r != 'None'){
                  alert(r);
                }
            }).fail(function(r) {
                showMessage('alert', r.responseText, $('#popup_message'), $('#popup_message_container'));
            });
        };

        Foundation.utils.debounce(dummy(), 300, true);

      <!--permite que quando o modal fecha o window_status retorne a edit-->
      $(document).on('closed', '#popup[data-reveal]', function () {
        var strURL = '/popup_close/' + window.name;
        $.ajax({type: 'POST', url: strURL
            });
      });

    </script>
  </body>
</html>
